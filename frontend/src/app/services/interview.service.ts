import { apiService } from '../core/api.service';
import type { Interview, CreateInterviewRequest } from '../models/interview.model';

export class InterviewService {
  async getAll(): Promise<Interview[]> {
    return apiService.get<Interview[]>('/interviews');
  }

  async getById(interviewId: string): Promise<Interview> {
    return apiService.get<Interview>(`/interviews/${interviewId}`);
  }

  async create(data: CreateInterviewRequest): Promise<Interview> {
    return apiService.post<Interview>('/interviews', data);
  }

  async delete(interviewId: string): Promise<void> {
    return apiService.delete<void>(`/interviews/${interviewId}`);
  }
}

export const interviewService = new InterviewService();
