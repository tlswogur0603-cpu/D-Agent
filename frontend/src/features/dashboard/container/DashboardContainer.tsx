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

  if (loading) return <div className="p-6">로딩중...</div>;
  if (error) return <div className="p-6">에러: {error}</div>;

  if (items.length === 0) {
    return <div className="p-6">데이터가 없습니다.</div>;
  }

  const selectedItem = items.find((item) => item.id === selectedId);

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="flex min-h-screen">
        <aside className="w-[280px] shrink-0 border-r border-gray-200 bg-white px-4 py-5">
          <h1 className="mb-5 text-xl font-bold text-gray-900">D-Agent</h1>

          <HistoryList
            items={items}
            selectedId={selectedId}
            onSelect={setSelectedId}
          />
        </aside>

        <section className="flex-1 overflow-y-auto px-8 py-8">
          {selectedItem && <ResultCard item={selectedItem} />}
        </section>
      </div>
    </main>
  );
}