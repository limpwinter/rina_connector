from src.response import *
from src.request import *

import random


class FeedbackDatabase:
    def __init__(self):
        self.feedback_db = []

    def leave_feedback(self, text):
        self.feedback_db.append(text)

    def print_db(self):
        print(self.feedback_db)


class TablesDatabase:
    def __init__(self):
        self.free_tables = {i: 0 for i in range(25)}

    def print_free_tables(self):
        for table in self.free_tables.keys():
            if self.free_tables[table]:
                continue
            else:
                print(table)


class RinaController:
    def __init__(self, model=None):
        self.model = model
        self.feedback_db = FeedbackDatabase()
        self.table_db = TablesDatabase()

    def pull(self, response: ResponseController = None):
        print("good")

    def push(self, request: RequestController):
        print(request)

    def produce_response(self, js_resp):
        user_id = js_resp['user_id']
        request_type = js_resp['request_type']
        annotation = js_resp['annotation']
        if request_type == 'Order':
            request_obj = self.handle_order(annotation)
        elif request_type == 'Book':
            request_obj = self.handle_book(annotation)
        elif request_type == 'RestaurantInfo':
            request_obj = self.handle_info(annotation)
        elif request_type == 'Menu':
            request_obj = self.handle_menu(annotation)
        elif request_type == 'Feedback':
            request_obj = self.handle_feedback(annotation)

    def handle_order(self, annotation):
        """

        :param annotation: json file with configuration
        :return: 1: success, 0: failure
        """
        options = [0, 1]
        rand_val = random.choice(options)
        return rand_val

    def handle_book(self, annotation):
        """

        :param annotation: json file with configuration
        :return: 1: success, 0: failure
        """
        options = [0, 1]
        rand_val = random.choice(options)
        return rand_val

    def handle_info(self, annotation):
        pass

    def handle_menu(self):
        img_folder = 'https://park-rovesnik.ru/thumb/2/Bvua2YZKQvHOgcgH9IXaEA/r/d/izobrazhenie_v_menyu_drova_a4_2.jpg'
        return img_folder

    def handle_feedback(self, annotation):
        text = annotation['feedback_text']
        self.feedback_db.leave_feedback(text=text)


RequestController()
a = RinaController()
model = RequestController(321, 'Feedback')
model.set_params('NEPLOHO')
# print(model.to_json())
js_resp = model.to_json()
a.produce_response(js_resp)
a.produce_response(js_resp)
a.feedback_db.print_db()
