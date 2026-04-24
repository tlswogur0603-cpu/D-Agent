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
    <article className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 md:p-8 flex flex-col gap-6">
      <header className="border-b border-gray-100 pb-4">
        <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-2">
          {item.title}
        </h3>
        <p className="text-sm text-gray-500">
          {formattedDate}
        </p>
      </header>

      <div className="flex-1">
        <RiskScore value={item.risk} />
      </div>
    </article>
  );
}