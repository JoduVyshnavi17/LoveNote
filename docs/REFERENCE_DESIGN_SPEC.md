# LoveNotes reference design specification

The four user-supplied reference images are stored in `docs/reference-images/`. They are the visual acceptance references for future implementation and QA.

## Reference 1 — Admin Dashboard Overview
File: `LoveNotes Admin Dashboard Overview(2).png`
- Desktop admin shell with fixed left navigation, LoveNotes mark and page heading.
- KPI row, user activity chart, workspace usage, platform summary.
- Recent signups/activity, system health, errors and alerts.
- MySQL table viewer with table selector, search, structure/query/export/backup actions.
- Top features and quick actions.
- The current implementation now has live DB KPI cards, a live read-only table selector/row browser, DB/API status and server-side admin authorization. The remaining analytics panels/actions (activity charts, error feed, backup/export, notification delivery) are not fully implemented and must not be represented as live data.

## Reference 2 — SaaS UI Design System Showcase
File: `LoveNotes SaaS UI Design System Showcase(2).png`
- Login, account creation, workspace selection, desktop/mobile student dashboard.
- Document library, upload, OCR review, reconstructed notes, Ask My Notes.
- Quiz, flashcards, mind map, meeting intelligence, tasks, reports, technical docs.
- Research library, comparison, profile, settings and export history.
- The image also shows subscription/pricing cards. Product direction from the project requirements is to keep the product free initially; do not implement paid plans, checkout, or premium gates.

## Reference 3 — AI Workspace UI Showcase
File: `LoveNotes AI Workspace UI Showcase(2).png`
- Landing page, login and account creation, workspace selection.
- Student and professional dashboards, upload/page management, reconstruction, multilingual tools.
- Quiz, flashcards, mind maps, Ask My Notes, meeting notes, extracted tasks, reports, technical docs, research summaries, comparison, search, profile, settings and export history.
- A pricing view appears in this image, but project requirements specify free access initially, so it is not a current implementation target.

## Reference 4 — Professional Workspace Dashboard
File: `LoveNotes Professional Workspace Dashboard(2).png`
- Left navigation, global search, student/professional switcher.
- Professional KPI cards, six quick actions, recent documents, project/task overview.
- Ask My Notes panel, professional tools list and bottom upload call-to-action.
- Use real account/document/task data; do not fabricate the sample counts shown in the reference.

## Acceptance rule
A screenshot being stored in the repository is not proof of pixel-perfect implementation. Each page must be run locally and compared side-by-side at the same viewport size. Dynamic values must come from the signed-in user's real data or be explicitly shown as unavailable. Do not copy the reference's sample names, emails, metrics, or task content into production.
