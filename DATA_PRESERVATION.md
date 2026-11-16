# Existing MySQL data preservation checklist

1. Back up the exact database first (Workbench or `mysqldump`) and verify that the backup can be restored.
2. Copy `backend/.env.example` to `backend/.env`; point `DATABASE_URL` at the existing database. Never include `.env` in a ZIP or commit.
3. Run `python inspect_existing_database.py` from `backend` and review every table and column.
4. Confirm the expected existing tables: `users`, `documents`, `pages`, `revisions`, `study_materials`, `suggestions`.
5. Compare the real schema with `backend/app/models.py`. `Base.metadata.create_all()` creates missing tables only; it does not add or modify existing columns.
6. Do not drop, truncate, rename or recreate tables to force compatibility. Use a reviewed, backed-up migration only if a specific mismatch is confirmed.
7. Check whether existing password hashes are Argon2-compatible before assuming old accounts can sign in.
8. Run `VERIFY_ENVIRONMENT.cmd`, start the backend, and verify `/health`.
9. Confirm old users/documents/pages are visible before uploading or editing anything.

The application code contains no `DROP TABLE` or `TRUNCATE` operation. Schema compatibility is not guaranteed until the read-only inventory is compared with the actual database.
