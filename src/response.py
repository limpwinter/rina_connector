from abc import ABC, abstractmethod


class BaseResponseAPI(ABC):
    @abstractmethod
    def from_json(self, json_file):
        raise NotImplementedError("Not Implemented")


class ResponseController(BaseResponseAPI):
    def __init__(self, json_file):
        self.image, self.text = self.from_json(json_file)

    def from_json(self, json_file):
        """
        KAK KARTINKU V JSONE PEREDAVAT?
        :param json_file:
        :return:
        """