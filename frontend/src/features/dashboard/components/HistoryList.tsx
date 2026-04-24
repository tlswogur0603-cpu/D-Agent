import type { HistoryItemModel } from "../types";
import { ResultCard } from "./ResultCard";

export type HistoryListProps = {
  items: HistoryItemModel[];
};

export function HistoryList({ items }: HistoryListProps) {
  if (!items || items.length === 0) {
    return <p>표시할 기록이 없습니다.</p>;
  }

  return (
    <section aria-label="분석 기록 리스트">
      {items.map((it) => (
        <ResultCard key={it.id} item={it} />
      ))}
    </section>
  );
}