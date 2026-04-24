import { apiClient } from "../../shared/lib/axios";

export type HistoryApiItem = {
  id: string;
  created_at: string;
  error_summary: string;
  risk_score: number;
  detected_issues: string[];
  suggested_solutions: string[];
};

export function fetchDashboardData(): Promise<HistoryApiItem[]> {
  return apiClient.get<HistoryApiItem[]>("/api/v1/agent/history");
}