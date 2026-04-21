export type ApiClientOptions = {
  baseUrl?: string;
  headers?: Record<string, string>;
};

export type ApiRequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  headers?: Record<string, string>;
  query?: Record<string, string | number | boolean | null | undefined>;
  body?: unknown;
};

function toQueryString(query: ApiRequestOptions["query"]): string {
  if (!query) return "";
  const params = new URLSearchParams();
  for (const [k, v] of Object.entries(query)) {
    if (v === undefined || v === null) continue;
    params.set(k, String(v));
  }
  const s = params.toString();
  return s ? `?${s}` : "";
}

export function createApiClient(options: ApiClientOptions = {}) {
  const baseUrl = options.baseUrl ?? "";
  const baseHeaders = options.headers ?? {};

  async function request<T>(path: string, req: ApiRequestOptions = {}): Promise<T> {
    const url = `${baseUrl}${path}${toQueryString(req.query)}`;
    const method = req.method ?? "GET";
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...baseHeaders,
      ...(req.headers ?? {}),
    };

    const res = await fetch(url, {
      method,
      headers,
      body: req.body === undefined ? undefined : JSON.stringify(req.body),
    });

    if (!res.ok) {
      const text = await res.text().catch(() => "");
      throw new Error(`API 요청 실패: ${method} ${url} (${res.status}) ${text}`);
    }

    const contentType = res.headers.get("content-type") ?? "";
    if (contentType.includes("application/json")) return (await res.json()) as T;
    return (await res.text()) as unknown as T;
  }

  return {
    request,
    get<T>(path: string, query?: ApiRequestOptions["query"]) {
      return request<T>(path, { method: "GET", query });
    },
    post<T>(path: string, body?: ApiRequestOptions["body"]) {
      return request<T>(path, { method: "POST", body });
    },
    put<T>(path: string, body?: ApiRequestOptions["body"]) {
      return request<T>(path, { method: "PUT", body });
    },
    patch<T>(path: string, body?: ApiRequestOptions["body"]) {
      return request<T>(path, { method: "PATCH", body });
    },
    delete<T>(path: string, query?: ApiRequestOptions["query"]) {
      return request<T>(path, { method: "DELETE", query });
    },
  };
}

export const apiClient = createApiClient();
