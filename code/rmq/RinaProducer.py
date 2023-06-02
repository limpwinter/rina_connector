import pika
import json


class RinaProducer:

    @staticmethod
    def produce(message_dict):
        credentials = pika.PlainCredentials(username='guest', 
                                            password='guest', 
                                            erase_on_connect=True)
        parameters = pika.ConnectionParameters(host='127.0.0.1',
                                               port=5672,
                                               virtual_host='curr_virtual_host', 
                                               credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        channel.queue_declare(queue='messages_to_tg')
        channel.basic_publish(
            exchange='', 
            routing_key='messages_to_tg', 
            body=json.dumps(message_dict)
        )
        print(" [x] Sent JSON message.")

        connection.close()