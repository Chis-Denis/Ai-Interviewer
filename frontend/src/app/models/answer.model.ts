export interface Answer {
  answer_id: string;
  text: string;
  question_id: string;
  interview_id: string;
  created_at: string;
}

export interface SubmitAnswerRequest {
  question_id: string;
  interview_id: string;
  text: string;
}
