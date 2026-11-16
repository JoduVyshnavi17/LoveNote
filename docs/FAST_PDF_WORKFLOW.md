# Faster workflow for short PDFs (1–5 pages)

## What is now faster
- On upload, each PDF page is checked for embedded/selectable text using PyMuPDF.
- Pages with a usable text layer are extracted locally and saved directly as faithful text. They do not call Gemini for OCR.
- Scanned/handwritten pages still go through vision OCR, because there is no reliable text layer to extract.
- Original page previews are still generated and kept for review.
- The upload UI returns control after the original document is saved. OCR continues in the background and updates the selected document when finished.
- PDF preview rendering is slightly lighter (1.25x, JPEG quality 82) to reduce local conversion and disk overhead.

## Why this matters
A typed PDF should not need an AI vision request to read text that is already embedded in the file. This path avoids that network round trip entirely. For scanned handwriting, model/provider response time remains a factor.

## Accuracy safeguards
- Text-layer extraction is used only when at least 40 alphanumeric characters are present on a page.
- Pages without a usable text layer remain eligible for AI OCR.
- The original page image is retained for visual checking.
- The OCR route continues to reuse stored page text and does not repeat completed OCR.

## Restart
Stop and restart the backend and frontend after replacing the project files. Keep the existing `backend/.env` and database unchanged.
