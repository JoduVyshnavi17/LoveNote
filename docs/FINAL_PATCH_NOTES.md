# Final patch notes — November 13, 2026

## Applied fixes
- Removed duplicate imported icon identifiers from `frontend/src/App.jsx`, including the duplicate `ArrowRight` reported by Vite.
- Changed the backend default Gemini model from `gemini-2.5-flash` to `gemini-3.8-flash`, matching the replacement model named in the user's Gemini API error.
- Set the default upload-size configuration to 20 GB (`MAX_UPLOAD_MB=20480`).
- Updated `backend/.env.example`. The real `.env` is deliberately not included.

## Important setup
In your existing `backend/.env`, preserve your database URL, API key, JWT secret and admin email. Add/update these two lines:
```env
GEMINI_MODEL=gemini-3.8-flash
MAX_UPLOAD_MB=20480
```
If your backend settings use a different environment-variable name for the Gemini model, follow the field names in `backend/app/config.py`; do not delete your other settings.

## Processing-time expectations
This project is configured to use the faster Flash model, but 15–20 seconds is a target, not a guaranteed SLA. Actual OCR and explanation time depends on page count, image resolution, handwriting clarity, Gemini service latency, quota and network speed. Test with a 1–2 page image/PDF first and measure the result before relying on a speed claim.

## Existing data and secrets
- No real `.env`, API key, database password, or uploaded user content is included in this package.
- Do not drop or recreate your existing MySQL database.
- Keep your existing `.env` and storage/uploads folder when replacing project code.
- This patch does not claim a production load test or a verified 20 GB end-to-end upload test.
