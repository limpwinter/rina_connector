from abc import ABC, abstractmethod


class BaseResponseAPI(ABC):
    @abstractmethod
    def from_json(self, json_file):
        raise NotImplementedError("Not Implemented")


class ResponseSample(BaseResponseAPI):
    def __init__(self, image, text):
        self.image = image
        self.text = text

    def from_json(self, json_file):
        pass


class ResponseController(BaseResponseAPI):
    def __init__(self, response_id: int = 0):
        self.response_id = response_id
        self.response = None

    def set_params(self, image, text):
        self.response = ResponseSample(image, text)

    def from_json(self, json_file):
        """
        KAK KARTINKU V JSONE PEREDAVAT?
        :param json_file:
        :return:
        """
