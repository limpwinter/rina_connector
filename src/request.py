from abc import ABC, abstractmethod


class BaseRequestInterface(ABC):

    @abstractmethod
    def to_json(self):
        raise NotImplementedError("Not Implemented")


class MakeOrderRequest(BaseRequestInterface):
    def __init__(self, user_id: int = 0, request_type: int = 0):
        self.user_id = user_id

    def to_json(self):
        pass


class BookingRequest(BaseRequestInterface):
    def __init__(self, table_number: int = 0, number_of_guests: int = 0):
        self.table_number = table_number
        self.number_of_guests = number_of_guests

    def to_json(self):
        pass


class RestaurantInfoRequest(BaseRequestInterface):
    def __init__(self, user_id: int = 0, request_type: int = 0):
        self.user_id = user_id

    def to_json(self):
        pass


class MenuRequest(BaseRequestInterface):
    def __init__(self, user_id: int = 0, request_type: int = 0):
        self.user_id = user_id

    def to_json(self):
        pass


class FeedBackRequest(BaseRequestInterface):
    def __init__(self, user_id: int = 0, request_type: int = 0, feedback_text: str = 'Well done!'):
        self.user_id = user_id
        self.feedback_text = feedback_text

    def to_json(self):
        pass


def order_req(*args):
    return MakeOrderRequest(*args)


def book_req(*args):
    return BookingRequest(*args)


def rest_info_req(*args):
    return RestaurantInfoRequest(*args)


def menu_req(*args):
    return MenuRequest(*args)


def feedback_req(*args):
    return FeedBackRequest(*args)


class RequestController:
    def __init__(self, request_type: str = 'Menu'):
        self.request = request_type

    def set_params(self, *args):
        if self.request == 'Order':
            return order_req(*args)
        elif self.request == 'Book':
            return book_req(*args)
        elif self.request == 'RestaurantInfo':
            return rest_info_req(*args)
        elif self.request == 'Menu':
            return menu_req(*args)
        elif self.request == 'Order':
            return feedback_req(*args)


