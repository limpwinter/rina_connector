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

    def get_availability(self, index):
        if self.free_tables[index]:
            return 1
        else:
            return 0

    def book_table(self, index):
        self.free_tables[index] = 1
        return


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
            request_obj, status = self.handle_book(annotation)
        elif request_type == 'RestaurantInfo':
            request_obj, status = self.handle_info()
        elif request_type == 'Menu':
            request_obj, status = self.handle_menu()
        elif request_type == 'Feedback':
            status = self.handle_feedback(annotation)
        else:
            raise 'What?'

        response = ResponseSample(image='', text=request_obj)
        return response

    def handle_order(self, annotation):
        dishes = annotation['number_of_dishes']
        return "Done!", 0

    def handle_book(self, annotation):
        table_number = annotation['table_number']
        if self.table_db.get_availability(table_number):

            return 'Trouble while booking', 1
        else:
            self.table_db.book_table(table_number)
            return 'Successfully ordered', 0

    def handle_info(self):
        img_folder = 'https://sun9-73.userapi.com/impf/c855124/v855124307/134ac8/r1OO8GT4M2k.jpg?size=604x417&quality=96&sign=a8e11fd7528f318530ab3b24bdf047f2&type=album'
        return img_folder, 0

    def handle_menu(self):
        img_folder = 'https://park-rovesnik.ru/thumb/2/Bvua2YZKQvHOgcgH9IXaEA/r/d/izobrazhenie_v_menyu_drova_a4_2.jpg'
        return img_folder, 0

    def handle_feedback(self, annotation):
        text = annotation['feedback_text']
        self.feedback_db.leave_feedback(text=text)
        return 0


RequestController()
a = RinaController()
model = RequestController(321, 'Book')
model.set_params(2, 2)
# print(model.to_json())
js_resp = model.to_json()
a.produce_response(js_resp)
a.produce_response(js_resp)
