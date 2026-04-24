export type RiskLevel = "low" | "medium" | "high";

export type RiskScoreModel = {
  score: number; // 0~100
  level: RiskLevel;
  summary?: string;
};

export type HistoryItemModel = {
  id: string;
  createdAt: string; // ISO string
  title: string;
  risk: RiskScoreModel;
  detectedIssues: string[];
  suggestedSolutions: string[];
  rawLog?: string;
};

export type DashboardDataModel = {
  history: HistoryItemModel[];
};
