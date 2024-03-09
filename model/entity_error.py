from abc import ABC, abstractmethod

class Error(ABC):
    @abstractmethod
    def error(self) -> dict:
        pass

    def code(self) -> int:
        pass

class ErrorInvalidFormat(Error):
    def error(self) -> dict:
        return {'error': 'Invalid format'}

    def code(self) -> int:
        return 400

class ErrorNotFound(Error):
    def error(self) -> dict:
        return {'error': 'Not found'}

    def code(self):
        return 404

class ErrorInvalidPayload(Error):
    def error(self) -> dict:
        return {'error': 'Invalid payload'}

    def code(self) -> int:
        return 400