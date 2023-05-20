from abc import ABC,abstractmethod
class BaseRequestAPI(ABC):
    def __init__(self, user_id: int = 0, task: int = 0):
        self.user_id = user_id
        self.task = task

    @abstractmethod
    def to_json(self):
        raise NotImplementedError("Not Implemented")


class Request