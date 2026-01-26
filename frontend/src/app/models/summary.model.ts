export interface InterviewSummary {
  summary_id: string;
  interview_id: string;
  themes: string[];
  key_points: string[];
  strengths: string[] | null;
  weaknesses: string[] | null;
  missing_information: string[] | null;
  sentiment_score: number | null;
  sentiment_label: string | null;
  confidence_score: number | null;
  clarity_score: number | null;
  consistency_score: number | null;
  overall_usefulness: number | null;
  full_summary_text: string | null;
  created_at: string;
}
