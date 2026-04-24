import type { HistoryItemModel } from "../types";
import { RiskScore } from "./RiskScore";

export type ResultCardProps = {
  item: HistoryItemModel;
};

export function ResultCard({ item }: ResultCardProps) {
  const formattedDate = new Date(item.createdAt).toLocaleString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <article className="max-w-2xl bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col gap-5">
      <header className="border-b border-gray-100 pb-3">
        <h3 className="text-lg md:text-xl font-bold text-gray-900 mb-1">
          {item.title}
        </h3>
        <p className="text-xs text-gray-500">
          {formattedDate}
        </p>
      </header>

      <div className="flex-1">
        <RiskScore value={item.risk} />
      </div>
    </article>
  );
}