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
    <ul aria-label="분석 기록 리스트" className="flex flex-col gap-2">
      {items.map((it) => (
        <li
          key={it.id}
          onClick={() => onSelect(it.id)}
          className={`cursor-pointer p-3 border rounded-md transition-colors ${selectedId === it.id
              ? "bg-gray-100 border-gray-900"
              : "hover:bg-gray-50 border-gray-200"
            }`}
        >
          <div className="font-medium text-gray-900">{it.title}</div>
          <div className="text-sm text-gray-500">
            {new Date(it.createdAt).toLocaleString("ko-KR")}
          </div>
        </li>
      ))}
    </ul>
  );
}