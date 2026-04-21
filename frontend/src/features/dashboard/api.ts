import { apiClient } from "../../shared/lib/axios";
import type { DashboardDataModel } from "./types";

export function fetchDashboardData(): Promise<DashboardDataModel> {
  return apiClient.get<DashboardDataModel>("/api/v1/agent/history");
}