from JsonController import JsonController


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

    def produce_response(self, js_resp):
        """

        :param js_resp: json from request
        :return: response_js: response in json format
        """
        js_resp = JsonController().str_to_dct(js_resp)
        user_id = js_resp['user_id']
        request_type = js_resp['request_type']
        annotation = js_resp['annotation']

        if request_type == 'Order':
            request_obj, status = self.handle_order(annotation)

        elif request_type == 'Book':
            request_obj, status = self.handle_book(annotation)

        elif request_type == 'RestaurantInfo':
            request_obj, status = self.handle_info()

        elif request_type == 'Menu':
            request_obj, status = self.handle_menu()

        elif request_type == 'Feedback':
            request_obj, status = self.handle_feedback(annotation)

        else:
            request_obj, status = "Error", 1

        response_js = {'user_id': user_id, "request_type": request_type,
                       "annotation": {'text': "Successfuly", "image": request_obj}}

        return JsonController().dict_to_str(response_js)

    def handle_order(self, annotation):
        """

        :param annotation: json annotation
        :return:
        text: string
        status : int {0,1}
        """
        dishes = annotation['number_of_dishes']
        return f"https://images.squarespace-cdn.com/content/v1/5f6d8d146cf2e1408ca04fb0/3280e50d-a353-460d-b6b7-b6ef25c22afd/Successfully-black.png", \
               0

    def handle_book(self, annotation):
        """

        :param annotation: json annotation
        :return: text: string
        status : int {0,1}
        """
        table_number = annotation['table_number']
        if self.table_db.get_availability(table_number):

            return 'https://img.industryweek.com/files/base/ebm/industryweek/image/2023/04/failure.6441a1c52787e.png?auto=format,compress&fit=fill&fill=blur&w=1200&h=630', 1
        else:
            self.table_db.book_table(table_number)
            return 'https://images.squarespace-cdn.com/content/v1/5f6d8d146cf2e1408ca04fb0/3280e50d-a353-460d-b6b7-b6ef25c22afd/Successfully-black.png', \
                   0

    def handle_info(self):
        """
        :return: text: string
        status : int {0,1}
        """
        img_folder = 'https://mkevent.ru/wp-content/uploads/2021/04/3-14-1200x675.jpg'
        return img_folder, 0

    def handle_menu(self):
        """
          :return: text: string
          status : int {0,1}
        """
        img_folder = 'https://park-rovesnik.ru/thumb/2/Bvua2YZKQvHOgcgH9IXaEA/r/d/izobrazhenie_v_menyu_drova_a4_2.jpg'
        return img_folder, 0

    def handle_feedback(self, annotation):
        """
          :return: text: string
          status : int {0,1}
          """
        text = annotation['feedback_text']
        self.feedback_db.leave_feedback(text=text)
        return "https://images.squarespace-cdn.com/content/v1/5f6d8d146cf2e1408ca04fb0/3280e50d-a353-460d-b6b7-b6ef25c22afd/Successfully-black.png", \
               0

# a = RinaController()
# model = RequestController(321, 'Book')
# model.set_params(2, 2)
# # print(model.to_json())
# js_resp = model.to_json()
# a.produce_response(js_resp)
# print(a.produce_response(js_resp))
