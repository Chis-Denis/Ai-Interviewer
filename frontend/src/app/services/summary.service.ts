import { apiService } from '../core/api.service';
import type { InterviewSummary } from '../models/summary.model';

export class SummaryService {
  async generate(interviewId: string): Promise<InterviewSummary> {
    return apiService.post<InterviewSummary>(`/summaries/interview/${interviewId}`);
  }

  async getByInterviewId(interviewId: string): Promise<InterviewSummary> {
    return apiService.get<InterviewSummary>(`/summaries/interview/${interviewId}`);
  }
}

export const summaryService = new SummaryService();
