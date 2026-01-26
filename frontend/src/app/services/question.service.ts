import { apiService } from '../core/api.service';
import type { Question, GenerateQuestionRequest } from '../models/question.model';

export class QuestionService {
  async generate(data: GenerateQuestionRequest): Promise<Question> {
    return apiService.post<Question>('/questions', data);
  }

  async getByInterviewId(interviewId: string): Promise<Question[]> {
    return apiService.get<Question[]>(`/questions/interview/${interviewId}`);
  }
}

export const questionService = new QuestionService();
