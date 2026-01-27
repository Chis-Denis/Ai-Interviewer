from uuid import UUID

from application.exceptions.base_exceptions import NotFoundException, BusinessRuleException


class InterviewNotFoundException(NotFoundException):
    def __init__(self, interview_id: UUID = None):
        if interview_id:
            message = f"Interview with id {interview_id} not found"
        else:
            message = "Interview not found"
        super().__init__(message)


class QuestionNotFoundException(NotFoundException):
    def __init__(self, question_id: UUID = None):
        if question_id:
            message = f"Question with id {question_id} not found"
        else:
            message = "Question not found"
        super().__init__(message)


class AnswerNotFoundException(NotFoundException):
    def __init__(self, answer_id: UUID = None):
        if answer_id:
            message = f"Answer with id {answer_id} not found"
        else:
            message = "Answer not found"
        super().__init__(message)


class SummaryNotFoundException(NotFoundException):
    def __init__(self, interview_id: UUID = None):
        if interview_id:
            message = f"Summary for interview {interview_id} not found"
        else:
            message = "Summary not found"
        super().__init__(message)


class NoAnswersFoundException(BusinessRuleException):
    def __init__(self, interview_id: UUID = None):
        if interview_id:
            message = f"No answers found for interview {interview_id}"
        else:
            message = "No answers found for this interview"
        super().__init__(message)


class InterviewAlreadyCompletedException(BusinessRuleException):
    def __init__(self, interview_id: UUID = None):
        if interview_id:
            message = f"Interview {interview_id} is already completed and cannot be modified"
        else:
            message = "Interview is already completed and cannot be modified"
        super().__init__(message)


class MaxQuestionsReachedException(BusinessRuleException):
    def __init__(self, interview_id: UUID = None, max_questions: int = None):
        if interview_id and max_questions:
            message = f"Maximum number of questions ({max_questions}) reached for interview {interview_id}"
        else:
            message = "Maximum number of questions reached for this interview"
        super().__init__(message)


class InvalidAnswerOrderException(BusinessRuleException):
    def __init__(self, message: str = "Answer order is invalid"):
        super().__init__(message)
