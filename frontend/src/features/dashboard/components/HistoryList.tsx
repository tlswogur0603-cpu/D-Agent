import type { HistoryItemModel } from "../types";

export type HistoryListProps = {
  items: HistoryItemModel[];
  selectedId: string | null;
  onSelect: (id: string) => void;
};

export function HistoryList({ items, selectedId, onSelect }: HistoryListProps) {
  if (!items || items.length === 0) {
    return <p>표시할 기록이 없습니다.</p>;
  }

  return (
    <ul aria-label="분석 기록 리스트" className="flex flex-col gap-1">
      {items.map((it) => (
        <li
          key={it.id}
          onClick={() => onSelect(it.id)}
          className={`cursor-pointer rounded-lg px-3 py-2 transition-colors ${selectedId === it.id
              ? "bg-gray-100 text-gray-900"
              : "text-gray-700 hover:bg-gray-50"
            }`}
        >
          <div className="truncate text-sm font-medium">
            {it.title}
          </div>
          <div className="mt-1 text-xs text-gray-400">
            {new Date(it.createdAt).toLocaleString("ko-KR")}
          </div>
        </li>
      ))}
    </ul>
  );
}