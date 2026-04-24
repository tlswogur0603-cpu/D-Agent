import type { RiskScoreModel } from "../types";

export type RiskScoreProps = {
  value: RiskScoreModel;
};

const levelStyles = {
  low: {
    card: "bg-green-50 border-green-200",
    text: "text-green-700",
    badge: "bg-green-100 text-green-800 border-green-200",
    label: "안전 (Low)",
  },
  medium: {
    card: "bg-yellow-50 border-yellow-200",
    text: "text-yellow-700",
    badge: "bg-yellow-100 text-yellow-800 border-yellow-200",
    label: "주의 (Medium)",
  },
  high: {
    card: "bg-red-50 border-red-200",
    text: "text-red-700",
    badge: "bg-red-100 text-red-800 border-red-200",
    label: "위험 (High)",
  },
};

export function RiskScore({ value }: RiskScoreProps) {
  const style = levelStyles[value.level] || levelStyles.medium;

  return (
    <div className="flex flex-col gap-6">
      <section aria-label="리스크 점수" className={`p-5 rounded-xl border ${style.card} flex items-center justify-between`}>
        <div className="flex flex-col">
          <span className={`text-sm font-bold mb-1 ${style.text}`}>종합 위험도</span>
          <div className="flex items-baseline gap-1">
            <span className={`text-4xl font-extrabold ${style.text}`}>{value.score}</span>
            <span className={`text-sm font-medium ${style.text}`}>/ 10</span>
          </div>
        </div>
        <div className={`px-4 py-2 rounded-full border text-sm font-bold shadow-sm ${style.badge}`}>
          {style.label}
        </div>
      </section>

      {value.summary && (
        <section aria-label="핵심 이슈" className="flex flex-col gap-3">
          <h4 className="text-base font-bold text-gray-900 flex items-center gap-2">
            <span className="w-1.5 h-5 bg-gray-900 rounded-sm inline-block"></span>
            핵심 이슈
          </h4>
          <div className="bg-gray-50 rounded-xl p-5 border border-gray-200 text-sm text-gray-700 leading-relaxed whitespace-pre-wrap shadow-inner">
            {value.summary}
          </div>
        </section>
      )}
    </div>
  );
}