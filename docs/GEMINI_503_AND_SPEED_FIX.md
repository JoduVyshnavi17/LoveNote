# Gemini 503 recovery and processing stability

## What changed
- Gemini requests now retry temporary overload/rate-limit/server failures with exponential backoff.
- Optional fallback Gemini model IDs can be configured in `backend/.env`.
- AI request concurrency is bounded. The previous document processor launched four Gemini OCR calls at once; this could create request bursts and worsen 503 overload.
- Audio transcription uses the same retry and fallback path.
- Invalid API keys, unsupported model IDs and malformed requests are not blindly retried.

## Configure
In `backend/.env`, check these settings:

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your_actual_key
GEMINI_MODEL=the_model_enabled_for_your_key
GEMINI_FALLBACK_MODELS=
AI_RETRY_ATTEMPTS=3
AI_RETRY_BASE_SECONDS=1.5
AI_MAX_CONCURRENT_REQUESTS=1
```

You may add comma-separated fallback model IDs only if they are currently enabled for the same API key in Google AI Studio. Do not copy example model IDs from old tutorials without checking availability.

## Restart
Stop the backend terminal with Ctrl+C, then run `START_BACKEND.cmd` again. The frontend does not need to be restarted for backend-only changes.

## Important limits
- Retries improve recovery from temporary 503 errors; they cannot guarantee that Google's service is available.
- If every configured model is overloaded, the app will return a readable temporary-service error rather than fabricate a result.
- Faster processing also depends on image/PDF size, number of pages, network, model capacity and API quota.
- Gemini API usage may be billable or quota-limited according to your Google AI Studio / Cloud project settings.
- No API key is included in this ZIP. Keep the key only in `backend/.env`.
