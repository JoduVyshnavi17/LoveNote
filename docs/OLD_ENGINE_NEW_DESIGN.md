# LoveNotes combined edition: original OCR-first approach + newer interface

This package combines:
- The newer LoveNotes React interface and workspace navigation (student/professional layout, dashboard, document workspace and feature screens).
- The newer FastAPI endpoints and data model required by that interface.
- The original LoveNotes OCR-first processing option: local Tesseract performs image-to-text extraction, rather than sending every source page to Gemini Vision.
- The newer AI notes-generation layer remains available for explanations/organized notes after extraction.

## Why this can feel faster
The original repository supports local Tesseract OCR. With `OCR_PROVIDER=tesseract`, OCR runs on the local computer and does not wait for Gemini Vision capacity for every page. This avoids the specific Gemini 503 bottleneck during transcription.

## Important handwriting limitation
Tesseract is strongest on clean printed text. It may be inaccurate on cursive or complex handwriting. For handwritten pages where local OCR quality is insufficient, switch `OCR_PROVIDER=gemini_vision` in `backend/.env`. Gemini may still experience 503 overloads. Do not assume local OCR and Gemini have equal handwriting accuracy.

## Setup
1. Extract the ZIP.
2. Copy your existing `backend/.env` into this folder. Do not overwrite your database URL, JWT secret, Gemini key, or admin email.
3. Set `OCR_PROVIDER=tesseract` in `backend/.env` to use the local OCR-first mode.
4. Install Tesseract OCR for Windows and ensure `tesseract.exe` is on PATH, or set `TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe`.
5. For Telugu/Hindi handwriting, install the relevant language data and set `OCR_LANGUAGE=eng+tel` or another installed language combination. Local Tesseract may still be weak on handwriting.
6. Restart the backend and frontend.

## Data safety
- This package does not intentionally drop, recreate, or migrate your MySQL database.
- Keep your existing database URL and back up your database before first launch.
- Do not share your `.env` file or API keys.

## What has and has not been verified
- Python source syntax and ZIP integrity are checked.
- This package has not been run against your private MySQL database, local Tesseract installation, or Gemini API key.
- Processing speed depends on machine performance, page quality, language packs and whether the AI generation step is requested.
