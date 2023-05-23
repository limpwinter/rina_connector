from abc import ABC, abstractmethod


class BaseResponseInterface(ABC):
    @abstractmethod
    def from_json(self, json_file):
        raise NotImplementedError("Not Implemented")


class ResponseSample(BaseResponseInterface):
    def __init__(self, image, text):
        self.image = image
        self.text = text

    def from_json(self, json_file):
        pass
        # return {'image': self.image,
        #         'text': self.text}


class ResponseController(BaseResponseInterface):
    def __init__(self, response_id: int = 0):
        self.response_id = response_id
        self.response = None

    def from_json(self, json_file):
        image = json_file['image']
        text = json_file['text']
        self.response = ResponseSample(image, text)


### Example
model = ResponseController(3)
model.from_json({'image': 123, 'text': 234})
print(model.response.image)


### TEXT/STATUS DA NET