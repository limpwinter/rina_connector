from src.response import *
from src.request import *


class RinaController:
    def __init__(self, model=None):
        self.model = model

    def process_request(self, response: ResponseController = None):
        print("good")


a = RinaController()
a.process_request()
