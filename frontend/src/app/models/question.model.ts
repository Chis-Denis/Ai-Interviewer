export interface Question {
  question_id: string;
  text: string;
  interview_id: string;
  question_order: number;
  created_at: string;
}

export interface GenerateQuestionRequest {
  interview_id: string;
}
