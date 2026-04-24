"use client";

import { useDashboard } from "../hooks";
import { HistoryList } from "../components/HistoryList";

export function DashboardContainer() {
  const { data, loading, error } = useDashboard();

  if (loading) return <div>로딩중...</div>;
  if (error) return <div>에러: {error}</div>;

  const items = data?.history ?? [];

  if (items.length === 0) {
    return <div>데이터가 없습니다.</div>;
  }
  
  return (
    <main>
      <h2>Dashboard</h2>
      <HistoryList items={items} />
    </main>
  );
}