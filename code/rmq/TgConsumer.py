import pika
import logging


class TgConsumer:

    def start_consuming(tg_controller):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters(host='127.0.0.1', 
                                               port=5672, 
                                               virtual_host='curr_virtual_host', 
                                               credentials=credentials)
    
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='messages_to_tg')
    
        def callback(ch, method, properties, body):
            tg_controller.receive_response(body)
            msg_log = "[x] Received %r" % body
            logging.info(msg_log)  

        channel.basic_consume(queue='messages_to_tg', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()