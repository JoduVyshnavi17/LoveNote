# Workflow fixes — November 2026

## Gemini model
- Updated default and `.env.example` to `gemini-3.8-flash`.
- Existing `backend/.env` takes precedence. Set `GEMINI_MODEL=gemini-3.8-flash` there and restart Uvicorn.
- Verify model availability and account access in the Google AI Studio project associated with the configured key.

## Upload and page navigation
- The frontend refreshes the user's document list immediately after the upload API confirms the document is saved.
- OCR runs after the save. If OCR fails, the saved document remains in My Documents and the UI reports the processing failure separately.
- The selected document is refreshed from the server after processing so page IDs, page numbers and OCR text are retained.
- Original uploaded pages render using a token-authenticated preview endpoint.
- Reconstructed Notes provides a Back to My Documents control and Retry processing.

## Image understanding
- Added `/api/documents/{doc_id}/analyze-visuals` to inspect original page images for diagrams, charts, tables, flowcharts, formulas and annotations.
- This is a separate operation from faithful transcription so image descriptions do not overwrite the verbatim OCR text.
- UI action: Explain diagrams & images.

## Study planner
- Added a source-grounded `planner` AI task that produces a practical seven-day plan from the selected notebook.
- It is intentionally not a fixed generic list of placeholder tasks.

## Processing throughput
- Multi-page OCR now uses at most two concurrent page workers and retains original page order.
- Higher concurrency is intentionally avoided to reduce API rate-limit risk. Provider latency and image quality still affect speed.

## Reserved ad areas
- Existing ad placeholders remain in the layout, but their visible label and explanatory copy have been removed.


## November 13 — faster processing and page navigation
- OCR preprocessing now caps very large phone images at 1800×1800 and removes the expensive median-filter pass.
- Multi-page document processing now uses up to four concurrent page requests, preserving original page order. This is a bounded speed improvement; Gemini latency, account quotas and image complexity still affect total time.
- Original uploaded pages now display one at a time in a page viewer with Previous and Next controls above and below the image. The controls disable at the first and last page.
- Reopening a document resets the viewer to page 1.


## November 13 — image-overlay navigation and handwriting quality
- Previous/Next arrow buttons are now overlaid directly on the left and right sides of the displayed original page image (not only placed in a toolbar).
- PDF pages are rasterized at 2.5× instead of 1.6× to retain finer handwriting and diacritic detail.
- OCR image preparation no longer applies aggressive autocontrast, which can erase faint pencil strokes and small marks; it retains up to 2600px resolution.
- The handwriting prompt explicitly asks for multilingual scripts (including Telugu, Hindi and English), faint marginal notes and page-edge text.


## November 13 — delete saved notes
- Added a clearly labeled Delete action on every saved document card in My Documents.
- Added Delete Note beside Back to My Documents in the open document/reconstructed notes view.
- Deletion asks for explicit confirmation, calls the authenticated owner-scoped DELETE endpoint, removes uploaded page files and cascaded document records, refreshes the list, and clears the open document if it was deleted.
- Seed/demo cards cannot be deleted because they are not persisted documents.


## November 13 — in-app navigation and large upload support
- Added Back, Forward and Refresh controls to LoveNotes' own top navigation. These are in-app controls; Chrome's browser toolbar is controlled by Chrome and cannot be modified by a website.
- LoveNotes navigation now records page transitions in browser history, so Back and Forward move between app views.
- Increased the default combined upload limit from 20 MB to 20 GB (20480 MB).
- Reworked document upload to stream files to disk in 8 MB chunks rather than reading the entire upload into RAM. PDFs are opened from disk and rasterized page-by-page.
- Updated the upload screen and `.env.example` to show/configure 20 GB.
- Large uploads require sufficient free disk space, a stable connection and matching `MAX_UPLOAD_MB=20480` in the existing backend `.env`. Existing `.env` values override defaults.
- The AI/OCR stage still depends on Gemini latency and per-page image processing; a 20 GB upload limit does not mean a 20 GB document can be processed quickly. The current per-PDF limit remains 30 pages.
