# LoveNotes — Student & Professional AI Workspace

This package combines the original LoveNotes application foundation with the expanded white-and-blue workspace UI, source-grounded AI tools, OCR, document exports, and server-enforced admin database inspection.

## Important: preserve your existing MySQL database

This project is configured to connect to an **existing** MySQL database. It does not include a replacement database and the Docker Compose file that previously started a separate PostgreSQL database has been removed.

1. Make a backup of your existing MySQL database before first run.
2. `backend/.env` is included as a local template. Replace its secret placeholders with newly rotated credentials; do not copy over it.
3. Set `DATABASE_URL` to the exact database you already use, for example:
   `mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/YOUR_EXISTING_DB`
4. Set a new long `JWT_SECRET_KEY`, your Gemini key (if using AI), and `ADMIN_EMAIL`.
5. Do not put `.env` in a ZIP or commit it to Git.
6. Run the read-only schema inventory first:
   ```cmd
   cd backend
   py -3.11 -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python inspect_existing_database.py
   ```
   Review the table/column names against the application schema before starting the API.

`Base.metadata.create_all()` creates only missing tables. It does not drop tables, delete rows, or alter existing columns. It also does not automatically reconcile incompatible columns in an existing table. If the schema inventory reveals differences, stop and reconcile them before using the application. Existing user/document records should remain intact.

## Run on Windows 11

### 1. Configure the backend

Copy `backend/.env.example` to `backend/.env` and enter your existing MySQL connection details. Never paste your real password or API key into source code.

### 2. Start the backend

Double-click `START_BACKEND.cmd`. The API runs at `http://127.0.0.1:8000` and its interactive API documentation is at `http://127.0.0.1:8000/docs`.

### 3. Start the frontend

In a second terminal, double-click `START_FRONTEND.cmd`. Vite normally serves the site at `http://localhost:5173`.

If needed, copy `frontend/.env.example` to `frontend/.env` and set `VITE_API_URL=http://127.0.0.1:8000`.

## Implemented in this package

- Responsive white-and-blue web UI with the LoveNotes logo.
- Landing page, account registration/login, Student and Professional workspace navigation.
- Authenticated document upload for JPG/JPEG/PNG/WEBP/PDF, source-page storage, OCR processing and page preview.
- Faithful OCR text and separately stored enhanced text; source review is required before relying on generated output.
- Source-grounded AI generation endpoints for explanations, summaries, quizzes, flashcards, mind maps, gap review, translation, meeting minutes from pasted transcripts, task extraction, reports, proposals, technical documentation, research briefs and document comparison.
- Ask My Notes endpoint that answers from supplied source text and says when information is absent.
- Saved document edits and revision snapshots.
- PDF, DOCX and TXT export.
- Admin-only overview, user list, live table/column/row viewer and sensitive-field redaction. Admin authorization is enforced by the backend using `ADMIN_EMAIL`.
- User ownership checks for document access and source-page images.
- Read-only database schema inventory script.

## Requires external configuration or further production work

- AI generation and AI OCR require a valid Gemini API key and model access. AI endpoints return a configuration error if no provider key is set.
- The Professional workspace can transcribe supported uploaded audio recordings and generate minutes when a compatible Gemini/OpenAI provider is configured. Calendar and meeting-platform integrations (Zoom/Meet/Teams) are not bundled.
- Email delivery, password-reset emails, scheduled database backups, persistent notification delivery, and production monitoring need provider credentials and deployment configuration.
- Google AdSense areas are placeholders only. They are not live ads; AdSense approval and publisher configuration are separate.
- Study planner/task widgets are currently browser-session UI state, not a multi-device synchronized task-management system.
- The frontend production build could not be verified in this environment because npm dependency installation timed out. Run `npm install` and `npm run build` locally before deployment.

## Security and data handling

- Keep API keys and DB credentials in `backend/.env` only.
- Change the development JWT secret before use outside localhost.
- Use a dedicated least-privilege MySQL account rather than the MySQL root account.
- The admin database viewer is read-only and redacts columns whose names indicate passwords, tokens, secrets or keys.
- Never expose uploaded source files or document content publicly. Deploy behind HTTPS and configure restrictive CORS before production.
- Keep backups outside the application folder and verify restoration before any schema changes.

## API overview

- `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`
- `POST /api/documents/upload`, `GET /api/documents`, `GET /api/documents/{id}`
- `POST /api/documents/{id}/process`, `PATCH /api/documents/{id}/content`
- `POST /api/ai/generate`, `POST /api/ai/ask`, `POST /api/ocr`, `POST /api/export`
- `POST /api/documents/{id}/export`, `GET /api/documents/{id}/revisions`
- `GET /api/admin/overview`, `GET /api/admin/users`, `GET /api/admin/database/tables`, `GET /api/admin/database/table/{table_name}`

For details, start the backend and open `/docs`.


## Fixes for the November 2026 workflow update

If Gemini reports that `gemini-2.5-flash` is unavailable, open `backend/.env` and set:
`GEMINI_MODEL=gemini-3.8-flash`
Then stop and restart the backend. The `.env.example` and backend default have also been updated, but an existing `.env` overrides defaults.

Recent uploads are now refreshed and shown before OCR begins. If OCR fails, the saved document remains in My Documents and can be reopened. The reconstructed-notes screen includes authenticated original-page previews, a Back to My Documents control, Retry processing, and a separate Explain diagrams & images action.

The Study Planner now generates a source-grounded seven-day plan from the selected notebook. The reserved ad areas remain blank; visible ad labels have been removed.

The OCR endpoint processes pages with limited two-worker concurrency to improve multi-page PDF throughput. Actual speed still depends on image quality, page count, provider latency and API quotas.


### Faster OCR and page navigation update
The latest workflow patch reduces large image payloads, removes an expensive preprocessing filter, and processes up to four pages concurrently while preserving page order. The original-page viewer now has Previous/Next arrows and a page counter. Restart both frontend and backend after updating.


### Image viewer and handwriting quality patch
The original-page image now has visible Previous/Next arrow buttons overlaid directly on the image edges. PDF rasterization is higher resolution (2.5×), and OCR preprocessing preserves faint strokes rather than applying aggressive autocontrast. These changes improve source fidelity but cannot guarantee perfect recognition of unclear handwriting; always review uncertain spans against the original.


### Delete saved notes
Use **My Documents → Delete** or open a saved note and choose **Delete Note**. The app asks for confirmation before permanently deleting the document and its uploaded page files. The backend only permits deletion by the document owner. Demo/sample cards are not real saved records and cannot be deleted.


### In-app navigation and 20 GB uploads
LoveNotes now includes Back, Forward and Refresh buttons in its own header. These navigate LoveNotes views; Chrome's actual toolbar is browser UI and cannot be changed by a website.

The default combined upload limit is 20 GB (`MAX_UPLOAD_MB=20480`). **Update your existing `backend/.env`** by adding or changing:
```env
MAX_UPLOAD_MB=20480
```
The upload endpoint streams files to disk in 8 MB chunks instead of holding the entire upload in memory. Make sure the computer has enough free disk space and a stable connection. The PDF processing limit is still 30 pages per PDF, and Gemini processing time depends on page count, image quality, API latency and quotas. A 20 GB upload allowance is not a promise that 20 GB can be processed quickly.


## Final configuration patch
See `docs/FINAL_PATCH_NOTES.md`. This package fixes the duplicate `ArrowRight` import, changes the Gemini model default to `gemini-3.8-flash`, and sets the default upload configuration to 20 GB. Preserve your existing backend `.env` and MySQL database. A 15–20 second processing time is a target and depends on document size and Gemini/network performance.


## Gemini 503 recovery
See `docs/GEMINI_503_AND_SPEED_FIX.md` for automatic retry/backoff, optional fallback models, and safe concurrency settings.
\n\n## Complete notes and Gemini fallback\nSee `docs/COMPLETE_NOTES_AND_GEMINI_FALLBACK.md`. Upload processing now transcribes images, saves completed pages incrementally, and generates structured complete notes in one document-level AI request.\n

## Combined edition
This edition uses the newer LoveNotes interface with the original OCR-first local Tesseract option. Read `docs/OLD_ENGINE_NEW_DESIGN.md` before setup, especially the Tesseract and existing database notes.


## November 2026 maintenance update

### Workspace tasks
- Tasks are stored per authenticated user and tagged Student or Professional.
- The Student workspace labels its planner `Study-Planner`; the Professional workspace labels its task area `TASK`.
- Tasks support due date/time, optional five-minute reminder, completion and deletion.
- Browser notifications run while the app is open and notification permission is granted. Push delivery while the browser is closed is not enabled in this package; it requires a push subscription service and VAPID credentials.

### Administrator access
- Set `ADMIN_EMAIL=joduvyshnavi@gmail.com` in `backend/.env`.
- The Admin navigation entry is only rendered for that signed-in email.
- Backend admin endpoints continue to enforce the same email restriction. Hiding the link is not the security boundary.

### Existing MySQL database
- The `tasks` table is created by SQLAlchemy `create_all()` on backend startup if it is missing.
- This does not alter or drop existing tables. Back up the database before deployment and inspect the new table after startup.
- Keep your real `.env` private; use `.env.example` only as a template.

### AI output
- AI-generated text is rendered as readable paragraphs, headings and lists rather than a raw preformatted block.
- AI accuracy still depends on source quality and provider configuration. Always review OCR against original page images.


## Detailed source audit
See `docs/SOURCE_AUDIT_AND_UPGRADE_NOTES.md` for the verified feature inventory, incomplete areas, security notes and safe upgrade procedure. This package preserves the uploaded application source; it does not claim every requested production feature is complete.


## Final consolidated build notes
This folder is the consolidated LoveNotes source package. Read `docs/FEATURE_STATUS.md` for the full requirement checklist and deployment-dependent items. The package intentionally excludes real `.env` files, API keys, database passwords, uploaded documents and database dumps. Copy your own existing `backend/.env` into the backend folder after extraction; do not replace it with `.env.example`.

### Windows quick start
1. Open PowerShell in `backend`, create/activate a Python 3.11 virtual environment, and run `pip install -r requirements.txt`.
2. Preserve your existing `backend/.env` and MySQL database. If you do not have a local env file, copy `.env.example` and fill in your own credentials.
3. Run `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`.
4. Open a second terminal in `frontend`, run `npm ci`, then `npm run dev`.
5. Open `http://localhost:5173`.

Do not delete or recreate the existing MySQL database. Back up the database and `storage/uploads` before deploying any update.
