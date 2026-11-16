
from PIL import Image, ImageOps
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import List
import tempfile
import logging

from ..config import settings
from .ai_provider import generate_text

logger = logging.getLogger("lovenotes.ocr")


# ---------------------------------------------------------
# IMAGE PREPROCESSING
# ---------------------------------------------------------

def preprocess(path: str) -> Image.Image:
    """
    Prepare an uploaded image for handwriting recognition.
    Corrects image orientation and resizes large images.
    """
    try:
        image = Image.open(path)
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")

        # Keep enough detail for handwriting recognition.
        image.thumbnail((2000, 2000), Image.Resampling.LANCZOS)

        return image

    except Exception as exc:
        raise RuntimeError(
            f"Unable to preprocess uploaded image: {exc}"
        ) from exc


def _normalized_jpeg(path: str) -> str:
    """
    Convert an uploaded image into an optimized JPEG.
    """
    image = preprocess(path)

    handle = tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    )

    handle.close()

    try:
        image.save(
            handle.name,
            format="JPEG",
            quality=90,
            optimize=True
        )
        return handle.name

    except Exception:
        Path(handle.name).unlink(missing_ok=True)
        raise


# ---------------------------------------------------------
# OCR PROMPTS
# ---------------------------------------------------------

def _ocr_prompt() -> str:
    return """
You are an expert multilingual handwritten notes OCR engine.

Your task is to read the attached notebook image and transcribe
the handwritten content as accurately as possible.

IMPORTANT RULES:

1. Detect and preserve the ORIGINAL language and script.
2. If the page is written in Telugu, return Telugu.
3. If the page is written in Hindi, return Hindi.
4. If the page is written in English, return English.
5. If multiple languages are present, preserve each language.
6. NEVER translate the content into another language.
7. NEVER summarize or explain the content.
8. NEVER invent words or sentences.
9. Do not automatically correct unclear handwriting by guessing.
10. Mark genuinely unreadable words as [unclear].

PRESERVE THE ORIGINAL STRUCTURE:

- Headings and subheadings
- Paragraphs
- Bullet points
- Numbering
- Tables
- Mathematical equations
- Formulas
- Scientific symbols
- Diagrams labels
- Abbreviations
- Examples

HANDWRITING INSTRUCTIONS:

- Carefully inspect every line.
- Read the complete page from top to bottom.
- Pay attention to similar-looking characters.
- Do not skip partially visible text.
- Do not replace handwritten words with more familiar words.
- Preserve the original meaning and wording.

OUTPUT:

Return ONLY the transcription.
Do not include explanations, introductions, markdown code blocks,
or comments about the image.
"""


# ---------------------------------------------------------
# SINGLE IMAGE TRANSCRIPTION
# ---------------------------------------------------------

def transcribe(path: str) -> str:
    """
    Transcribe one handwritten image.

    Supported providers:
    - groq_vision
    - groq
    - gemini_vision
    - openai_vision
    - tesseract
    """

    provider = settings.ocr_provider.lower().strip()

    if not Path(path).exists():
        raise FileNotFoundError(
            f"OCR image does not exist: {path}"
        )

    # -----------------------------------------------------
    # TESSERACT OCR
    # -----------------------------------------------------

    if provider == "tesseract":
        try:
            import pytesseract

            if settings.tesseract_cmd:
                pytesseract.pytesseract.tesseract_cmd = (
                    settings.tesseract_cmd
                )

            image = preprocess(path)

            result = pytesseract.image_to_string(
                image,
                lang=settings.ocr_language
            )

            return result.strip()

        except Exception as exc:
            logger.exception("Tesseract OCR failed")

            raise RuntimeError(
                f"Tesseract OCR failed: {exc}"
            ) from exc

    # -----------------------------------------------------
    # GROQ VISION OCR
    # -----------------------------------------------------

    if provider in {
        "groq",
        "groq_vision",
        "gemini_vision",
        "openai_vision"
    }:

        normalized_path = None

        try:
            normalized_path = _normalized_jpeg(path)

            result = generate_text(
                _ocr_prompt(),
                system=(
                    "You are a highly accurate multilingual "
                    "handwriting transcription engine. "
                    "Your priority is exact source fidelity. "
                    "Never translate or invent content."
                ),
                image_path=normalized_path
            )

            if not result or not result.strip():
                raise RuntimeError(
                    "The OCR provider returned an empty transcription."
                )

            return result.strip()

        except Exception as exc:
            logger.exception("Vision OCR failed")

            raise RuntimeError(
                f"Handwriting OCR failed: {exc}"
            ) from exc

        finally:
            if normalized_path:
                Path(normalized_path).unlink(missing_ok=True)

    # -----------------------------------------------------
    # UNSUPPORTED PROVIDER
    # -----------------------------------------------------

    raise RuntimeError(
        f"Unsupported OCR_PROVIDER: {provider}. "
        "Use groq_vision or tesseract."
    )


# ---------------------------------------------------------
# MULTIPLE IMAGE TRANSCRIPTION
# ---------------------------------------------------------

def transcribe_batch(paths: List[str]) -> List[str]:
    """
    Transcribe multiple notebook pages.

    Each page is sent as an actual image to the vision model.
    Results remain in the same order as the uploaded pages.

    Uses limited parallel execution to reduce waiting time.
    """

    if not paths:
        return []

    provider = settings.ocr_provider.lower().strip()

    # Tesseract processing
    if provider == "tesseract":
        return [
            transcribe(path)
            for path in paths
        ]

    # Vision OCR processing
    if provider in {
        "groq",
        "groq_vision",
        "gemini_vision",
        "openai_vision"
    }:

        results = [""] * len(paths)

        def process_page(index: int, image_path: str):
            logger.info(
                "Starting OCR for page %s",
                index + 1
            )

            text = transcribe(image_path)

            logger.info(
                "Completed OCR for page %s",
                index + 1
            )

            return index, text

        # Limit parallel requests to avoid overwhelming
        # the provider or hitting rate limits.
        max_workers = min(2, len(paths))

        with ThreadPoolExecutor(
            max_workers=max_workers
        ) as executor:

            futures = [
                executor.submit(process_page, index, path)
                for index, path in enumerate(paths)
            ]

            for future in futures:
                index, text = future.result()
                results[index] = text

        return results

    raise RuntimeError(
        f"Unsupported OCR_PROVIDER: {provider}"
    )
