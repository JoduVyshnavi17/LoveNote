# Image upload and generated-result fixes

- Fixed JPEG and PNG magic-byte checks in the upload endpoint. The prior escaped byte literals compared against backslash characters instead of actual file signatures.
- Frontend file picker now explicitly includes `.jpg`, `.jpeg`, `.png`, `.webp`, and `.pdf` and advertises all supported formats.
- Generation requests now carry a run identifier. Navigating to another page invalidates an in-flight request, clears stale output, and prevents late responses from replacing the current page's result.
- Previous quiz, flashcard, or mind-map output is cleared on page navigation.
- No database schema or user data is changed by these source updates.

## OCR configuration note

The screenshot shows a local Tesseract executable/language-data error. Check `TESSERACT_CMD` and `TESSDATA_PREFIX` if using Tesseract. For handwritten multilingual pages, `OCR_PROVIDER=gemini_vision` uses the configured Gemini vision provider and its batched-page path; this consumes Gemini API quota and is not guaranteed to be faster for every page.
