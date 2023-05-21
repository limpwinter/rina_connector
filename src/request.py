from abc import ABC, abstractmethod


class BaseRequestAPI(ABC):

    @abstractmethod
    def to_json(self):
        raise NotImplementedError("Not Implemented")


class MakeOrderRequest(BaseRequestAPI):
    def __init__(self, user_id: int = 0, request_type: int = 0):
        self.user_id = user_id
        self.request_type = request_type

    def to_json(self):
        pass


class BookingRequest(BaseRequestAPI):
    def __init__(self, table_number: int = 0, number_of_guests: int = 0):
        self.table_number = table_number
        self.number_of_guests = number_of_guests

    def to_json(self):
        pass


class RestaurantInfoRequest(BaseRequestAPI):
    def __init__(self, user_id: int = 0, request_type: int = 0):
        self.user_id = user_id
        self.request_type = request_type

    def to_json(self):
        pass


class MenuRequest(BaseRequestAPI):
    def __init__(self, user_id: int = 0, request_type: int = 0):
        self.user_id = user_id
        self.request_type = request_type

    def to_json(self):
        pass


class FeedBackRequest(BaseRequestAPI):
    def __init__(self, user_id: int = 0, request_type: int = 0, feedback_text: str = 'Well done!'):
        self.user_id = user_id
        self.request_type = request_type
        self.feedback_text = feedback_text

    def to_json(self):
        pass
