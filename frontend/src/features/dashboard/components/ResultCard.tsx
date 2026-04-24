import type { HistoryItemModel } from "../types";
import { RiskScore } from "./RiskScore";

export type ResultCardProps = {
  item: HistoryItemModel;
};

export function ResultCard({ item }: ResultCardProps) {
  const formattedDate = new Date(item.createdAt).toLocaleString("ko-KR");

  return (
    <article>
      <header>
        <h3>{item.title}</h3>
        <small>{formattedDate}</small>
      </header>

      <div>
        <RiskScore value={item.risk} />
      </div>
    </article>
  );
}