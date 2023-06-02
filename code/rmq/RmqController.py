from TgProducer import TgProducer
from TgConsumer import TgConsumer
from RinaProducer import RinaProducer
from RinaConsumer import RinaConsumer


class RmqController:

    @staticmethod
    def send_to_rina(message_dict):
        TgProducer.produce(message_dict)
        
    @staticmethod
    def send_to_tg(message_dict):
        RinaProducer.produce(message_dict)

    @staticmethod
    def start_consuming_from_rina(controller):
        TgConsumer.start_consuming(controller)
        
    @staticmethod
    def start_consuming_from_tg(controller):
        RinaConsumer.start_consuming(controller)