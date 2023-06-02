from producer_tg_client import TgProducer
from consumer_Rina import RinaConsumer


class RmqController:
    #must be better called send request/produce, thanks to 
    def push():
        TgProducer.send_request_ro_Rina()
        #return NotImplementedError
    
    #must be better called receive request/consume, thanks to 
    def pull():
        RinaConsumer.receive_response_Rina()
        #return NotImplementedError
    
