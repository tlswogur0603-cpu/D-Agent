import { useEffect, useState } from "react";
import { fetchDashboardData } from "./api";
import type { DashboardDataModel } from "./types";

export function useDashboard() {
  const [data, setData] = useState<DashboardDataModel | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const res = await fetchDashboardData();
        setData(res);
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