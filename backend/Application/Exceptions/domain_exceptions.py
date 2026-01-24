from Application.Exceptions.base_exceptions import NotFoundException, BusinessRuleException


class InterviewNotFoundException(NotFoundException):
    def __init__(self, interview_id: str = None):
        if interview_id:
            message = f"Interview with id {interview_id} not found"
        else:
            message = "Interview not found"
        super().__init__(message)


class QuestionNotFoundException(NotFoundException):
    def __init__(self, question_id: str = None):
        if question_id:
            message = f"Question with id {question_id} not found"
        else:
            message = "Question not found"
        super().__init__(message)


class AnswerNotFoundException(NotFoundException):
    def __init__(self, answer_id: str = None):
        if answer_id:
            message = f"Answer with id {answer_id} not found"
        else:
            message = "Answer not found"
        super().__init__(message)


class SummaryNotFoundException(NotFoundException):
    def __init__(self, interview_id: str = None):
        if interview_id:
            message = f"Summary for interview {interview_id} not found"
        else:
            message = "Summary not found"
        super().__init__(message)


class NoAnswersFoundException(BusinessRuleException):
    def __init__(self, interview_id: str = None):
        if interview_id:
            message = f"No answers found for interview {interview_id}"
        else:
            message = "No answers found for this interview"
        super().__init__(message)
