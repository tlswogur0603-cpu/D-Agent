import axios, { AxiosInstance, AxiosRequestConfig } from "axios";

/**
 * API 클라이언트 생성 시 사용할 옵션
 */
export type ApiClientOptions = {
  baseUrl?: string; // API 기본 URL (ex: http://localhost:8000)
  headers?: Record<string, string>; // 공통 헤더
};

/**
 * 공통 API 클라이언트 생성 함수
 */
export function createApiClient(options: ApiClientOptions = {}) {
  /**
   * axios 인스턴스 생성
   * - baseURL: 모든 요청에 자동으로 prefix로 붙음
   * - headers: 공통 헤더 설정
   */
  const instance: AxiosInstance = axios.create({
    baseURL: options.baseUrl ?? "",
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  /**
   * 공통 request 함수
   * - 모든 HTTP 요청은 이 함수를 거침
   * - response.data만 반환해서 사용하기 쉽게 만듦
   */
  const request = async <T>(
    path: string,
    config: AxiosRequestConfig = {}
  ): Promise<T> => {
    const response = await instance.request<T>({
      url: path,
      ...config,
    });

    return response.data;
  };

  /**
   * HTTP 메서드별 함수들
   * - 내부적으로 request 함수 사용
   * - query → params (axios 규칙)
   * - body → data (axios 규칙)
   */
  return {
    request,

    get<T>(path: string, query?: Record<string, unknown>) {
      return request<T>(path, {
        method: "GET",
        params: query,
      });
    },

    post<T>(path: string, body?: unknown) {
      return request<T>(path, {
        method: "POST",
        data: body,
      });
    },

    put<T>(path: string, body?: unknown) {
      return request<T>(path, {
        method: "PUT",
        data: body,
      });
    },

    patch<T>(path: string, body?: unknown) {
      return request<T>(path, {
        method: "PATCH",
        data: body,
      });
    },

    delete<T>(path: string, query?: Record<string, unknown>) {
      return request<T>(path, {
        method: "DELETE",
        params: query,
      });
    },
  };
}

/**
 * 실제 사용할 API 클라이언트
 * - 환경변수에서 baseURL 가져옴
 * - NEXT_PUBLIC_ 접두사는 프론트에서 접근 가능하게 하기 위함
 */
export const apiClient = createApiClient({
  baseUrl: process.env.NEXT_PUBLIC_API_URL,
});