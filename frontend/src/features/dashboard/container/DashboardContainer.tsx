"use client";

import { useState, useEffect } from "react";
import { useDashboard } from "../hooks";
import { HistoryList } from "../components/HistoryList";
import { ResultCard } from "../components/ResultCard";

export function DashboardContainer() {
  const { data, loading, error } = useDashboard();
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const items = data?.history ?? [];

  useEffect(() => {
    if (items.length > 0 && !selectedId) {
      setSelectedId(items[0].id);
    }
  }, [items, selectedId]);

  if (loading) return <div>로딩중...</div>;
  if (error) return <div>에러: {error}</div>;

  if (items.length === 0) {
    return <div>데이터가 없습니다.</div>;
  }

  const selectedItem = items.find((item) => item.id === selectedId);

  return (
    <main className="p-4">
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      <div className="flex flex-row gap-6">
        <aside className="w-1/3 min-w-[250px] border-r border-gray-200 pr-4">
          <HistoryList
            items={items}
            selectedId={selectedId}
            onSelect={setSelectedId}
          />
        </aside>
        <section className="flex-1">
          {selectedItem && <ResultCard item={selectedItem} />}
        </section>
      </div>
    </main>
  );
}