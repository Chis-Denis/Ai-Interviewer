export interface Interview {
  interview_id: string;
  topic: string;
  status: 'not_started' | 'in_progress' | 'completed';
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface CreateInterviewRequest {
  topic: string;
}
