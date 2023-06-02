import pika
import logging


class TgProducer:

    def send_request_ro_Rina():
        # If you want to have a more secure SSL authentication, use ExternalCredentials object instead
        credentials = pika.PlainCredentials(username='guest', 
                                            password='guest', 
                                            erase_on_connect=True)
        parameters = pika.ConnectionParameters(host='127.0.0.1',
                                               port=5672,
                                               virtual_host='curr_virtual_host', 
                                               credentials=credentials)

        # We are using BlockingConnection adapter to start a session. 
        # It uses a procedural approach to using Pika and 
        # has most of the asynchronous expectations removed
        connection = pika.BlockingConnection(parameters)
       
        # A channel provides a wrapper for interacting with RabbitMQ
        channel = connection.channel()

        # Check for a queue and create it, if necessary
        channel.queue_declare(queue='messages_to_rina')

        # For the sake of simplicity, we are not declaring an exchange, 
        # so the subsequent publish call will be sent to 
        # a Default exchange that is predeclared by the broker
        channel.basic_publish(exchange='', routing_key='messages_to_rina', body='Hello World!')
        logging.info(" [x] Sent message")  

        # Safely disconnect from RabbitMQ
        connection.close() 


