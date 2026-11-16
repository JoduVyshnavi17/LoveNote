
const API = (
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
).replace(/\/+$/, "");

export async function api(
  path,
  {
    method = "GET",
    body,
    headers = {},
  } = {}
) {
  const requestHeaders = { ...headers };

  const token = localStorage.getItem("ln-token");

  if (token) {
    requestHeaders.Authorization = `Bearer ${token}`;
  }

  if (
    body &&
    !(body instanceof FormData) &&
    !(body instanceof Blob)
  ) {
    requestHeaders["Content-Type"] = "application/json";
  }

  let response;

  try {
    response = await fetch(`${API}${path}`, {
      method,
      headers: requestHeaders,
      body:
        body instanceof FormData || body instanceof Blob
          ? body
          : body !== undefined && body !== null
          ? JSON.stringify(body)
          : undefined,
    });
  } catch (networkError) {
    const error = new Error(
      "Unable to connect to LoveNotes server. Please try again."
    );

    error.status = 0;
    error.data = null;

    throw error;
  }

  const contentType =
    response.headers.get("content-type") || "";

  let payload = null;

  if (response.status !== 204) {
    try {
      if (contentType.includes("application/json")) {
        payload = await response.json();
      } else {
        const text = await response.text();
        payload = text || null;
      }
    } catch {
      payload = null;
    }
  }

  if (!response.ok) {
    let message = `Request failed (${response.status})`;

    const detail =
      payload?.detail ??
      payload?.message ??
      payload?.error;

    if (typeof detail === "string") {
      message = detail;
    } else if (Array.isArray(detail)) {
      message = detail
        .map((item) => item?.msg || String(item))
        .join(", ");
    } else if (detail && typeof detail === "object") {
      message =
        detail.message ||
        detail.msg ||
        JSON.stringify(detail);
    }

    if (response.status === 409) {
      message =
        "Email already registered. Please sign in instead.";
    }

    if (response.status === 404 && path.includes("/login")) {
      message =
        "No account exists with this email. Please create an account.";
    }

    const error = new Error(message);

    error.status = response.status;
    error.data = payload;
    error.response = {
      status: response.status,
      data: payload,
    };

    throw error;
  }

  return payload;
}

export { API };
