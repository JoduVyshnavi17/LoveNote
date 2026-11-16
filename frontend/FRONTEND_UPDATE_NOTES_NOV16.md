# LoveNotes Frontend Update — November 16

This package contains frontend-only changes. Backend source and database files are not included or modified.

## Included changes
- Study progress is calculated from the current workspace's uploaded document count. It increases as documents are added and decreases when documents are deleted.
- Guest preview is persisted for the browser session via local storage. Guest preview clears document/task state and shows zero personal uploads. Upload routes and the New Document action direct guests to sign in or create an account.
- Workspace selection displays only Student Workspace and Professional Workspace cards, with locally styled illustrations.
- Removed the Student Teacher-vs-Student comparison and Professional Document Comparison navigation/actions.
- Removed the extra dashboard workspace switcher; workspace switching is available through the two workspace cards.
- Registration handles the backend's HTTP 409 `Email already registered` response and displays a clear message.

## Backend-dependent limitations
- The currently supplied backend's document list response does not include a workspace field, and its upload endpoint does not persist a workspace value. This frontend records the workspace for newly uploaded document IDs in browser local storage and falls back to the account purpose for older documents. Durable, cross-device Student/Professional separation requires a backend/database change and server-side ownership checks.
- The currently supplied login endpoint returns the same HTTP 401 `Incorrect email or password` response for both an unknown email and a wrong password. The frontend cannot safely distinguish those cases without a backend endpoint or a distinct response code. Duplicate registration is distinguishable because the backend returns HTTP 409.

## Run
```bash
npm install
npm run dev
```
