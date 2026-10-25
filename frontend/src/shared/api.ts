export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string,
  ) {
    super(message);
  }
}
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch("/api/v1" + path, {
    ...init,
    credentials: "include",
    headers: {
      ...(init.body ? { "Content-Type": "application/json" } : {}),
      ...init.headers,
    },
  });
  if (response.status === 204) return undefined as T;
  const body = await response.json();
  if (!response.ok)
    throw new ApiError(
      body.error?.message ?? "No se pudo completar la solicitud",
      response.status,
      body.error?.code ?? "error",
    );
  return body as T;
}
export async function mutate<T>(
  path: string,
  body?: unknown,
  method = "POST",
  headers: Record<string, string> = {},
) {
  const csrf = await api<{ csrf_token: string }>("/auth/csrf");
  return api<T>(path, {
    method,
    headers: { "X-CSRF-Token": csrf.csrf_token, ...headers },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}
