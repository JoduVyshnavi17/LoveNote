# Faster document processing update

This update targets the actual delay in the previous implementation:
- The previous processing route made one Gemini vision request for every page, serially.
- A 20-page notebook could therefore require around 20 model calls before finishing.
- PDF pages were rasterized at 2x and normalized to PNG, creating unnecessarily large image payloads.
- Clicking Process again repeated OCR even when page text was already saved.

Changes:
1. Gemini/OpenAI vision requests can now accept multiple images.
2. OCR groups up to 3 consecutive pages into one request and keeps the page order.
3. If a batch response omits a page, only that missing page is retried individually.
4. Existing page OCR is reused on subsequent Process clicks.
5. PDF rasterization is reduced to 1.35x and stored as JPEG quality 84 to reduce payload size.
6. Transient retries are shorter (2 attempts, 0.6-second base delay) so an overloaded model does not hold the user for a long retry chain.

Important:
- This should reduce API round trips substantially for multi-page PDFs, but handwriting quality and provider response times still depend on Gemini availability, page complexity, network, and quota.
- Batch transcription is enabled for Gemini/OpenAI vision. Local Tesseract remains page-by-page.
- The endpoint still waits for the document's processing request to finish; this change does not yet add background job progress/polling.
- Test with a 2–3 page document first and compare source fidelity before using it for a large notebook.
