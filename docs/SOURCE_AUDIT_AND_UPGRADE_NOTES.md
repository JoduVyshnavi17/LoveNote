# Source audit and upgrade notes (2026-11-14)

## What is already in this uploaded source
- React 18 + Vite app with Student and Professional navigation, login/register, document UI, OCR review, AI generation surfaces, quiz/flashcard/mind-map views, planner/task UI, and admin view.
- FastAPI backend with JWT/Argon2 auth, user-owned documents, PDF/image upload and OCR pipeline, AI routes, exports, revisions, suggestions, task CRUD, meeting audio transcription, and server-side admin checks.
- SQLAlchemy models include users, documents, pages, revisions, suggestions, study materials, and tasks.
- Existing MySQL/PyMySQL support is present in requirements.

## Important limitations found in the source (not silently treated as complete)
- Student and Professional navigation differ, but documents are not fully partitioned by workspace in the database/API.
- Admin area is read-only for user/table browsing; analytics feeds, email error alerts, backup operations and broader system controls are not fully implemented.
- Exports in the API support TXT/PDF/DOCX; XLSX/PPTX are not implemented as complete export workflows.
- Browser reminders require the app to remain open; push delivery while closed is not configured.
- Some Professional pages call generic AI generation routes rather than being independent editable report/proposal/chart builders.
- Favorites and export history are not confirmed as durable server-side features.
- Existing MySQL schema compatibility and existing password-hash compatibility must be tested against a backup before migration or account changes.
- The uploaded source reports no completed end-to-end test or verified production build.

## Changes made in this package
- Added `backend/.env` and refreshed `.env.example` using the supplied configuration choices.
- Secret values are placeholders because the actual DB password, Gemini key and JWT secret were exposed in chat. Rotate them and enter new values locally.
- Made the Pydantic settings config explicitly read `.env` as UTF-8.
- Preserved the uploaded app source and backend routes rather than replacing them with a demo application.
- Did not drop tables, alter existing data, or attempt an unreviewed migration.

## Critical MySQL note
The previously reported `Plugin 'mysql_native_password' is not loaded` is a MySQL server/account authentication configuration issue. This application package cannot fix that by changing `.env`. Diagnose MySQL version and the `lovenotes_app` account plugin before altering the account. Do not drop/recreate the database.

## Run locally
1. Back up the existing `lovenotes` database.
2. Edit `backend/.env` and replace all three placeholders with newly rotated credentials. URL-encode special characters in the DB password.
3. In CMD:
   `cd backend`
   `py -3.11 -m venv .venv`
   `.venv\\Scripts\\activate`
   `python -m pip install -r requirements.txt`
   `python inspect_existing_database.py`
4. Compare the inventory to the ORM models. Stop if columns/types differ; `create_all()` only creates missing tables and is not a schema migration.
5. Start backend using `START_BACKEND.cmd`.
6. In a second CMD, run `cd frontend`, `npm install`, `npm run build`, then `npm run dev`.
7. Test `/health`, login, upload, OCR, AI, tasks and admin with a test account/database backup before using production data.
