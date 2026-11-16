
"""
LoveNotes - Groq AI Provider

Features:
- Text generation
- JSON generation
- Image and handwritten-note analysis
- Multiple image inputs
- Audio transcription
- Compatibility with existing LoveNotes modules
"""

import os
import json
import base64
import logging
import mimetypes

from pathlib import Path
from functools import lru_cache
from typing import Any, Optional

from dotenv import load_dotenv
from groq import Groq


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

logger = logging.getLogger("lovenotes.ai")

GROQ_API_KEY = (os.getenv("GROQ_API_KEY") or "").strip()

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
).strip()

GROQ_VISION_MODEL = os.getenv(
    "GROQ_VISION_MODEL",
    "qwen/qwen3.8-27b"
).strip()

GROQ_AUDIO_MODEL = os.getenv(
    "GROQ_AUDIO_MODEL",
    "whisper-large-v3-turbo"
).strip()

try:
    AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "60"))
except (ValueError, TypeError):
    AI_TIMEOUT = 60

# Ensure enough tokens remain for the actual answer.
MIN_COMPLETION_TOKENS = 8192

DEFAULT_SYSTEM_PROMPT = """
You are LoveNotes AI, an intelligent educational assistant.

Your responsibilities:
- Help students understand and organize their notes.
- Preserve the original meaning and language.
- Never invent information.
- Explain concepts clearly and accurately.
- Return complete answers.
- Follow the requested output format.
"""


# =========================================================
# GROQ CLIENT
# =========================================================

@lru_cache(maxsize=1)
def get_groq_client() -> Groq:

    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your backend .env file."
        )

    return Groq(
        api_key=GROQ_API_KEY,
        timeout=AI_TIMEOUT,
        max_retries=1
    )


# =========================================================
# RESPONSE EXTRACTION
# =========================================================

def _extract_text(response: Any) -> str:

    try:
        choice = response.choices[0]
        message = choice.message
        content = message.content

    except (AttributeError, IndexError, TypeError) as exc:
        raise RuntimeError(
            "Groq returned an unexpected response format."
        ) from exc

    if isinstance(content, str) and content.strip():
        return content.strip()

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, dict):
                value = item.get("text")
            else:
                value = getattr(item, "text", None)

            if value:
                parts.append(str(value))

        result = "\n".join(parts).strip()

        if result:
            return result

    finish_reason = getattr(choice, "finish_reason", None)

    usage = getattr(response, "usage", None)

    completion_tokens = getattr(
        usage,
        "completion_tokens",
        "unknown"
    )

    raise RuntimeError(
        "Groq returned an empty response. "
        f"Finish reason: {finish_reason}. "
        f"Completion tokens: {completion_tokens}. "
        "The response may have exhausted its token budget."
    )


# =========================================================
# IMAGE ENCODING
# =========================================================

def _encode_image(image_path: str) -> dict:

    path = Path(image_path)

    if not path.is_file():
        raise RuntimeError(
            f"Image file not found: {path}"
        )

    mime_type = (
        mimetypes.guess_type(path.name)[0]
        or "image/jpeg"
    )

    if not mime_type.startswith("image/"):
        raise RuntimeError(
            f"Unsupported image type: {mime_type}"
        )

    try:

        with path.open("rb") as image_file:
            encoded = base64.b64encode(
                image_file.read()
            ).decode("ascii")

    except OSError as exc:
        raise RuntimeError(
            f"Unable to read image: {path}"
        ) from exc

    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:{mime_type};base64,{encoded}"
        }
    }


def _build_user_content(
    prompt: str,
    image_paths: Optional[list[str]] = None
):

    if not image_paths:
        return prompt

    content = [
        {
            "type": "text",
            "text": prompt
        }
    ]

    for image_path in image_paths:
        content.append(_encode_image(image_path))

    return content


# =========================================================
# TOKEN HANDLING
# =========================================================

def _completion_limit(requested_tokens: int) -> int:

    try:
        requested_tokens = int(requested_tokens)
    except (ValueError, TypeError):
        requested_tokens = MIN_COMPLETION_TOKENS

    return max(
        requested_tokens,
        MIN_COMPLETION_TOKENS
    )


# =========================================================
# COMMON GROQ REQUEST
# =========================================================

def _request_text(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 8192,
    image_paths: Optional[list[str]] = None
) -> str:

    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("AI prompt cannot be empty.")

    selected_model = model or GROQ_MODEL

    if not selected_model:
        raise RuntimeError("Groq model name is missing.")

    token_limit = _completion_limit(max_tokens)

    messages = [
        {
            "role": "system",
            "content": system_prompt or DEFAULT_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": _build_user_content(
                prompt,
                image_paths=image_paths
            )
        }
    ]

    request_options = {
        "model": selected_model,
        "messages": messages,
        "temperature": temperature,
        "max_completion_tokens": token_limit
    }

    # GPT-OSS supports reasoning_effort.
    # Low effort leaves more completion budget for the answer.
    if selected_model.startswith("openai/gpt-oss"):
        request_options["reasoning_effort"] = "low"

    response = get_groq_client().chat.completions.create(
        **request_options
    )

    return _extract_text(response)


# =========================================================
# JSON PARSING
# =========================================================

def _parse_json_object(output: str) -> dict:

    if not output or not output.strip():
        raise RuntimeError(
            "Groq returned empty content instead of JSON."
        )

    cleaned = output.strip()

    # Remove Markdown code fences.
    if cleaned.startswith("```"):

        lines = cleaned.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    # Try normal JSON parsing.
    try:

        result = json.loads(cleaned)

        if isinstance(result, dict):
            return result

        raise RuntimeError(
            "Expected a JSON object from Groq."
        )

    except json.JSONDecodeError:
        pass

    # Find JSON object inside surrounding text.
    start = cleaned.find("{")

    if start == -1:
        raise RuntimeError(
            "Groq did not return a JSON object."
        )

    try:

        result, _ = json.JSONDecoder().raw_decode(
            cleaned[start:]
        )

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Groq returned incomplete or invalid JSON."
        ) from exc

    if not isinstance(result, dict):
        raise RuntimeError(
            "Groq returned JSON, but it was not an object."
        )

    return result


# =========================================================
# TEXT GENERATION
# =========================================================

def generate_ai_content(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 8192
) -> str:

    try:

        return _request_text(
            prompt=prompt,
            system_prompt=system_prompt,
            model=GROQ_MODEL,
            temperature=temperature,
            max_tokens=max_tokens
        )

    except Exception as exc:

        logger.exception("Groq text generation failed")

        if isinstance(exc, (ValueError, RuntimeError)):
            raise

        raise RuntimeError(
            f"AI generation failed: {exc}"
        ) from exc


# =========================================================
# JSON GENERATION
# =========================================================

def generate_ai_json(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_tokens: int = 8192
) -> dict:

    json_system = (
        system_prompt
        or "You are LoveNotes AI. Return a valid JSON object only."
    )

    json_system += """

JSON OUTPUT REQUIREMENTS:
1. Return exactly one valid JSON object.
2. Do not use Markdown code fences.
3. Do not add explanations outside the JSON.
4. Use double quotes for all keys and string values.
5. Do not use trailing commas.
6. Include all requested fields.
7. Return complete JSON, not a partial response.
"""

    try:

        output = _request_text(
            prompt=prompt,
            system_prompt=json_system,
            model=GROQ_MODEL,
            temperature=0.1,
            max_tokens=max_tokens
        )

        return _parse_json_object(output)

    except Exception as exc:

        logger.exception("Groq JSON generation failed")

        if isinstance(exc, (ValueError, RuntimeError)):
            raise

        raise RuntimeError(
            f"AI JSON generation failed: {exc}"
        ) from exc


# =========================================================
# LEGACY TEXT FUNCTION
# =========================================================

def generate_text(
    prompt: str,
    system: Optional[str] = None,
    max_output_tokens: int = 8192,
    image_path: Optional[str] = None,
    **kwargs
) -> str:

    system_prompt = (
        kwargs.pop("system_prompt", None)
        or system
    )

    max_tokens = kwargs.pop(
        "max_tokens",
        max_output_tokens
    )

    temperature = kwargs.pop(
        "temperature",
        0.2
    )

    image_paths = kwargs.pop(
        "image_paths",
        None
    )

    if image_path:
        image_paths = [image_path]

    selected_model = (
        GROQ_VISION_MODEL
        if image_paths
        else GROQ_MODEL
    )

    try:

        return _request_text(
            prompt=prompt,
            system_prompt=system_prompt,
            model=selected_model,
            temperature=temperature,
            max_tokens=max_tokens,
            image_paths=image_paths
        )

    except Exception as exc:

        logger.exception(
            "Groq %s generation failed",
            "vision" if image_paths else "text"
        )

        if isinstance(exc, (ValueError, RuntimeError)):
            raise

        raise RuntimeError(
            f"AI generation failed: {exc}"
        ) from exc


# =========================================================
# LEGACY JSON FUNCTION
# =========================================================

def generate_json(
    prompt: str,
    system: Optional[str] = None,
    max_output_tokens: int = 8192,
    **kwargs
) -> dict:

    system_prompt = (
        kwargs.pop("system_prompt", None)
        or system
    )

    max_tokens = kwargs.pop(
        "max_tokens",
        max_output_tokens
    )

    image_paths = kwargs.pop(
        "image_paths",
        None
    )

    # Text-only JSON.
    if not image_paths:

        return generate_ai_json(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens
        )

    # Image-based JSON using Groq Vision.
    json_system = (
        system_prompt
        or "You are LoveNotes AI. Return a valid JSON object only."
    )

    json_system += """

JSON OUTPUT REQUIREMENTS:
- Return one valid JSON object only.
- Do not use Markdown code fences.
- Do not add explanations outside the JSON.
- Use double quotes.
- Do not use trailing commas.
- Include all requested fields.
- Do not return incomplete JSON.
"""

    try:

        output = _request_text(
            prompt=prompt,
            system_prompt=json_system,
            model=GROQ_VISION_MODEL,
            temperature=0.1,
            max_tokens=max_tokens,
            image_paths=image_paths
        )

        return _parse_json_object(output)

    except Exception as exc:

        logger.exception(
            "Groq vision JSON generation failed"
        )

        if isinstance(exc, (ValueError, RuntimeError)):
            raise

        raise RuntimeError(
            f"Vision JSON generation failed: {exc}"
        ) from exc


# =========================================================
# AUDIO TRANSCRIPTION
# =========================================================

def transcribe_audio(
    audio_path: str,
    mime_type: Optional[str] = None
) -> str:

    path = Path(audio_path)

    if not path.is_file():
        raise RuntimeError(
            f"Audio file not found: {path}"
        )

    detected_mime = (
        mime_type
        or mimetypes.guess_type(path.name)[0]
        or "application/octet-stream"
    )

    try:

        with path.open("rb") as audio_file:

            result = get_groq_client().audio.transcriptions.create(
                model=GROQ_AUDIO_MODEL,
                file=(
                    path.name,
                    audio_file,
                    detected_mime
                ),
                response_format="text",
                temperature=0.0
            )

        if isinstance(result, str):
            transcript = result.strip()
        else:
            transcript = (
                getattr(result, "text", "") or ""
            ).strip()

        if not transcript:
            raise RuntimeError(
                "Audio transcription returned empty text."
            )

        return transcript

    except Exception as exc:

        logger.exception("Groq audio transcription failed")

        if isinstance(exc, RuntimeError):
            raise

        raise RuntimeError(
            f"Audio transcription failed: {exc}"
        ) from exc


# =========================================================
# CONNECTION TEST
# =========================================================

def test_ai_connection() -> dict:

    try:

        message = generate_ai_content(
            prompt="Reply with exactly: LoveNotes AI is working.",
            system_prompt=(
                "You are a connection testing assistant. "
                "Follow the instruction exactly."
            ),
            temperature=0.0,
            max_tokens=1024
        )

        return {
            "success": True,
            "provider": "Groq",
            "model": GROQ_MODEL,
            "message": message
        }

    except Exception as exc:

        logger.exception("Groq connection test failed")

        return {
            "success": False,
            "provider": "Groq",
            "model": GROQ_MODEL,
            "error": str(exc)
        }
