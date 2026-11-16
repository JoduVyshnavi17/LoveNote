# LoveNotes final feature checklist

This checklist consolidates the user's requirements from the project conversations. It distinguishes implemented source code from external services that need credentials or deployment configuration.

## Product boundary and note integrity
- [x] LoveNotes remains a handwritten-note reconstruction and completion workspace, not an LMS or student-management platform.
- [x] Keep raw OCR, faithful reconstruction, enhanced notes and accepted AI additions separate.
- [x] Preserve source language; AI must not silently translate.
- [x] Use [unclear] markers rather than inventing handwriting.
- [x] Keep AI additions reviewable and label explicit omissions, potential gaps and optional enrichment.

## Core note workflow
- [x] Secure registration/login with Argon2 password hashing and JWT sessions.
- [x] Confirm-password validation and password visibility control in signup UI.
- [x] Student and Professional workspace selection.
- [x] Multi-file JPG/JPEG/PNG/WEBP and scanned PDF upload.
- [x] PDF rasterization, image preprocessing and OCR provider abstraction.
- [x] Faithful Reconstruction, AI Enhanced Reconstruction and Complete My Notes processing modes.
- [x] Page-preserving, document-level enhancement rather than separate AI calls per page.
- [x] Reuse saved OCR and enhanced content to avoid repeated provider calls.
- [x] Edit and save reconstructed notes; revision snapshots.
- [x] Original source-page preview and page navigation.
- [x] Missing-topic review at Basic, Detailed and Comprehensive depth through backend API.
- [x] Accept/reject/edit suggestion API.
- [x] PDF, DOCX and TXT export.
- [x] Search, archive, restore, permanent delete and page reorder APIs.

## Student workspace and study support
- [x] Source-grounded explanations, summaries and quizzes.
- [x] Flashcards and visual mind maps.
- [x] Ask My Notes grounded in supplied notes.
- [x] Formula/equation recognition task with uncertainty markers.
- [x] Teacher-notes versus student-notes comparison task.
- [x] Translation while preserving formulas and technical terms.
- [x] Seven-day study plan / study-time estimates.
- [x] Browser text-to-speech for generated content (browser voice availability varies).

## Professional workspace
- [x] Meeting audio transcription API and transcript/minutes generation.
- [x] Task and action-item extraction.
- [x] Persistent tasks with due dates, reminders and completion status.
- [x] Report, proposal, technical-document and research-brief generation.
- [x] Document comparison task.

## Admin and operations
- [x] Server-side admin authorization by configured ADMIN_EMAIL.
- [x] Live user/document/page/suggestion counts and read-only database table browser.
- [ ] Full daily/weekly/monthly usage analytics and active-user event tracking require an event-logging service/table.
- [ ] Email error notifications require SMTP configuration and an error-event delivery worker.
- [ ] Scheduled encrypted backups require deployment scheduling and storage credentials.

## Performance and security
- [x] Argon2id configured with a responsive memory-hard profile; existing Argon2 hashes remain verifiable.
- [x] Database connection health checks and connection-pool pre-ping/recycling.
- [x] Bounded AI concurrency and no retry loop for hard daily quota exhaustion.
- [x] OCR and study-aid caching to reduce duplicate processing.
- [x] Upload ownership checks and backend-only API keys.
- [ ] Production worker queue, malware scanning, refresh-token rotation, email verification, password reset, rate limiting and security audit require deployment work.

## Important setup dependencies
- Gemini/OpenAI credentials are required for hosted AI handwriting OCR and generation.
- Tesseract language data must be installed for every configured local OCR language; Tesseract is not reliable for cursive handwriting.
- SMTP and push notifications require provider credentials. Browser speech uses the installed browser/OS voices.
- Keep the existing MySQL database and the user's local `.env`; this package intentionally does not contain secrets or user data.
