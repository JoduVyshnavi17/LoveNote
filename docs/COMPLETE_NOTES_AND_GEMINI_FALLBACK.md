# Complete-notes and Gemini recovery update

## Why the 503 happened
HTTP 503 UNAVAILABLE with Google's "model currently experiencing high demand" message is a provider-side temporary capacity/overload response. It is not proof that the uploaded image or PDF is invalid, and it is not fixed by changing the frontend. Google recommends retry with backoff for transient 503/429 responses.

## What changed
- The configured primary Gemini model is tried first.
- If `GEMINI_FALLBACK_MODELS` is empty, the backend now automatically tries stable Flash-family fallbacks `gemini-3.7-flash` and `gemini-3.5-flash-lite` after transient overloads.
- A non-empty `GEMINI_FALLBACK_MODELS` value in `.env` overrides the built-in fallback list.
- OCR results are committed after each successful page batch. A later 503 no longer discards earlier completed pages.
- The upload workflow requests complete-notes formatting after transcription.
- Complete notes are generated in one document-level request instead of one enhancement request per page.
- Original transcription (`faithful_text`/`raw_ocr`) remains stored separately from formatted notes (`enhanced_text`).
- The notes editor displays the formatted notes first, then falls back to the faithful transcript.

## Restart and test
1. Stop backend with Ctrl+C.
2. Keep the existing `backend/.env`; do not replace it.
3. Restart backend.
4. Upload one clear 1–2 page handwritten image/PDF.
5. Wait for the completion message. If OCR succeeds but formatting fails, the recognized source text is saved and can be retried.

## Notes
- Fallback model availability depends on the Google AI Studio project/key and current service capacity.
- If all configured Gemini models return 503, no code can force Google's API to accept the request. Configure another provider/key in a future provider-fallback setup if you need independent redundancy.
- This package has been syntax-checked and ZIP-verified, but not live-tested against the user's private API key or database.
