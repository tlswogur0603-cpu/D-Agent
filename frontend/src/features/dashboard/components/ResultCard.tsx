import type { HistoryItemModel } from "../types";
import { RiskScore } from "./RiskScore";

export type ResultCardProps = {
  item: HistoryItemModel;
};

function SectionList({
  title,
  items,
}: {
  title: string;
  items: string[];
}) {
  if (!items || items.length === 0) {
    return null;
  }

  return (
    <section className="rounded-2xl border border-gray-200 bg-white p-5">
      <h4 className="mb-4 text-sm font-bold text-gray-900">{title}</h4>

      <ul className="space-y-3">
        {items.map((text, index) => (
          <li
            key={`${title}-${index}`}
            className="rounded-xl bg-gray-50 px-4 py-3 text-sm leading-6 text-gray-700"
          >
            {text}
          </li>
        ))}
      </ul>
    </section>
  );
}

export function ResultCard({ item }: ResultCardProps) {
  const formattedDate = new Date(item.createdAt).toLocaleString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <article className="w-full max-w-6xl">
      <div className="space-y-6">
        <header className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between gap-4">
            <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
              Analysis Result
            </p>
            <time className="text-xs text-gray-500">{formattedDate}</time>
          </div>

          <h2 className="max-w-4xl text-lg font-semibold leading-7 text-gray-900 md:text-xl">
            {item.title}
          </h2>
        </header>

        <RiskScore value={item.risk} />

        <div className="grid gap-5 xl:grid-cols-2">
          <SectionList title="감지된 문제" items={item.detectedIssues} />
          <SectionList title="추천 해결 방안" items={item.suggestedSolutions} />
        </div>

        {item.rawLog && (
          <details className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <summary className="cursor-pointer text-sm font-semibold text-gray-700">
              원본 로그 보기
            </summary>
            <pre className="mt-4 max-h-64 overflow-auto whitespace-pre-wrap rounded-xl bg-gray-50 p-4 text-xs leading-5 text-gray-600">
              {item.rawLog}
            </pre>
          </details>
        )}
      </div>
    </article>
  );
}