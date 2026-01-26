import { apiService } from '../core/api.service';
import type { Answer, SubmitAnswerRequest } from '../models/answer.model';

export class AnswerService {
  async submit(data: SubmitAnswerRequest): Promise<Answer> {
    return apiService.post<Answer>('/answers', data);
  }

  async getByInterviewId(interviewId: string): Promise<Answer[]> {
    return apiService.get<Answer[]>(`/answers/interview/${interviewId}`);
  }
}

export const answerService = new AnswerService();
