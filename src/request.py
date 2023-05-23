from abc import ABC, abstractmethod


class BaseRequestInterface(ABC):

    @abstractmethod
    def to_json(self):
        raise NotImplementedError("Not Implemented")


class MakeOrderRequest(BaseRequestInterface):
    def __init__(self, number_of_dishes: list[int] = [1, 2, 3]):
        self.number_of_dishes = number_of_dishes

    def to_json(self):
        return {'num_of_dishes': self.number_of_dishes}


class BookingRequest(BaseRequestInterface):
    def __init__(self, table_number: int = 0, number_of_guests: int = 0):
        self.table_number = table_number
        self.number_of_guests = number_of_guests

    def to_json(self):
        return {"table_number": self.table_number,
                "number_of_guests": self.number_of_guests}


class RestaurantInfoRequest(BaseRequestInterface):
    def __init__(self, info: str = 'location'):
        self.info = info

    def to_json(self):
        return {'info': self.info}


class MenuRequest(BaseRequestInterface):
    def __init__(self, type_of_menu: str = 'lunch'):
        self.type_of_menu = type_of_menu

    def to_json(self):
        return {"type_of_menu":
                    self.type_of_menu}


class FeedBackRequest(BaseRequestInterface):
    def __init__(self, feedback_text: str = 'Well done!'):
        self.feedback_text = feedback_text

    def to_json(self):
        return {"feedback_text":
                    self.feedback_text}


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
    def __init__(self, user_id: int = 0, request_type: str = 'Menu'):
        self.user_id = user_id
        self.request_obj = None
        self.request_type = request_type

    def set_params(self, *args):
        if self.request_type == 'Order':
            self.request_obj = order_req(*args)
        elif self.request_type == 'Book':
            self.request_obj = book_req(*args)
        elif self.request_type == 'RestaurantInfo':
            self.request_obj = rest_info_req(*args)
        elif self.request_type == 'Menu':
            self.request_obj = menu_req(*args)
        elif self.request_type == 'Feedback':
            self.request_obj = feedback_req(*args)

    def to_json(self):
        return {'user_id': self.user_id,
                'request_type': self.request_type,
                'annotation': self.request_obj.to_json()
                }


### EXAMPLE
model = RequestController(0, 'Book')
model.set_params(10, 5)
print(model.to_json())
###
