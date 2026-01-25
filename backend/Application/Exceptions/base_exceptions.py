class ApplicationException(Exception):
    pass


class NotFoundException(ApplicationException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BusinessRuleException(ApplicationException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class LlmServiceError(ApplicationException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)