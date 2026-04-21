import { useDashboard } from "../hooks";
import { HistoryList } from "../components/HistoryList";

export function DashboardContainer() {
  const { data, loading, error } = useDashboard();

  if (loading) return <div>로딩중...</div>;
  if (error) return <div>에러: {error}</div>;

  const items = data?.history ?? [];

  return (
    <main>
      <h2>Dashboard</h2>
      <HistoryList items={items} />
    </main>
  );
}