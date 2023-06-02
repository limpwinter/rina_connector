from abc import ABC, abstractmethod


class BaseResponseInterface(ABC):
    @abstractmethod
    def from_json(self, json_file):
        raise NotImplementedError("Not Implemented")


class ResponseSample(BaseResponseInterface):
    def __init__(self):
        self.image = None
        self.text = None

    def from_json(self, json_file):
        self.image = json_file['image']
        self.text = json_file['text']


class ResponseController:
    def __init__(self):
        self.user_id = None
        self.response = None

    def set_params(self, json_file):
        self.response = ResponseSample()
        self.user_id = json_file['user_id']
        js_annotation = json_file['annotation']
        self.response.from_json(js_annotation)

## Example
# model = ResponseController()
# model.set_params({"user_id": 5, "annotation": {'image': 123, 'text': 234}})
# print(model.response.image)

## TEXT/STATUS DA NET
