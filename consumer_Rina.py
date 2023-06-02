import pika
import logging

from rina import RinaController

class RinaConsumer:
    # script that must be executed forever 
    # until a keyboard interrupt exception is received
    def receive_response_Rina():
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters(host='127.0.0.1', 
                                               port=5672, 
                                               virtual_host='curr_virtual_host', 
                                               credentials=credentials)
    
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='messages_to_rina')
    
        # Since RabbitMQ works asynchronously, every time you receive a message, 
        # a callback function is called. We will simply print the message body to the terminal 
        def callback(ch, method, properties, body):
            # TODO body to json dict
            RinaController.produce_response(body)
            msg_log = "[x] Received %r" % body
            logging.info(msg_log)  

        # Consume a message from a queue. 
        # The auto_ack option simplifies our example, 
        # as we do not need to send back an acknowledgement query 
        # to RabbitMQ which we would normally want in production
        channel.basic_consume(queue='messages_to_rina', on_message_callback=callback, auto_ack=True)
        #print(' [*] Waiting for messages. To exit press CTRL+C')
    
    # Start listening for messages to consume
        channel.start_consuming()
    
