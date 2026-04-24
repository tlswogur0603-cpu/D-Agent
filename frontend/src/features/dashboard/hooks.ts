import { useEffect, useState } from "react";
import { fetchDashboardData, type HistoryApiItem } from "./api";
import type { DashboardDataModel, HistoryItemModel } from "./types";

// risk_score → level 변환
function toRiskLevel(score: number): "low" | "medium" | "high" {
  if (score >= 7) return "high";
  if (score >= 4) return "medium";
  return "low";
}

// 백엔드 → 프론트 모델 변환
function mapHistoryItem(item: HistoryApiItem): HistoryItemModel {
  return {
    id: item.id,
    createdAt: item.created_at,
    title: item.error_summary,
    risk: {
      score: item.risk_score,
      level: toRiskLevel(item.risk_score),
      summary: item.detected_issues?.[0] ?? "",
    },
    detectedIssues: item.detected_issues ?? [],
    suggestedSolutions: item.suggested_solutions ?? [],
    rawLog: item.raw_log,
  };
}

export function useDashboard() {
  const [data, setData] = useState<DashboardDataModel | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError(null);

        const res = await fetchDashboardData();

        // 여기서 변환
        const mapped = res.map(mapHistoryItem);

        setData({
          history: mapped,
        });
      } catch (e) {
        setError(e instanceof Error ? e.message : "에러 발생");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  return { data, loading, error };
}