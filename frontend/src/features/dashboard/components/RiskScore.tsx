import type { RiskScoreModel } from "../types";

export type RiskScoreProps = {
  value: RiskScoreModel;
};

export function RiskScore({ value }: RiskScoreProps) {
  return (
    <section aria-label="리스크 점수">
      <strong>Risk</strong>

      <div>
        <span>{value.score}</span>
        <span> - {value.level}</span>
      </div>

      {value.summary && <p>{value.summary}</p>}
    </section>
  );
}