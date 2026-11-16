# Project contents

- `frontend/` — React/Vite application, UI components, styling, logo, package manifest and environment example.
- `backend/app/` — FastAPI routes, auth, SQLAlchemy models/database, OCR, AI provider and export services.
- `backend/tests/` — security tests.
- `backend/inspect_existing_database.py` — read-only MySQL schema inventory.
- `backend/verify_environment.py` — read-only DB connection/schema preflight.
- `docs/` — architecture, master requirements, production checklist, feature-status matrix and screenshot-reference note.
- `storage/` — upload/export storage root.
- `START_BACKEND.cmd`, `START_FRONTEND.cmd`, `VERIFY_ENVIRONMENT.cmd` — Windows helper scripts.
- `.env.example` files — credential-free configuration templates.
- `FILE_MANIFEST.json` — file sizes and SHA-256 hashes.

Read `README.md`, `DATA_PRESERVATION.md` and `docs/FEATURE_STATUS.md` before running the app.
