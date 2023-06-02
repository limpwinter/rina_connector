
from datetime import datetime
import pika

# Returns the connection string to the rmq by the given name from the dictionary
# adr: connection string name from dict 
# Returns the rmq connection string in URLConnectionString format
def rabbit_connection_str(adr):
    cp_rabbit = {
        # TODO !!!!
        # set the connection to the rabbit by IP, %2F - means vhost = "/"
        '192.168.1.25': 'amqp://TODO:TODO@TODO/%2F',
        # set the connection to the rabbit by HOSTNAME
        #TODO !!!! 
        'TODO': 'amqp://TODO@TODO'
    }
    while adr not in cp_rabbit and adr != 'exit':
        adr = input(f'[{time_now()}] specified rmq was not found in the directory \n'
                    'Enter a valid RabbitMQ server address or "exit" \n')
    if adr == 'exit':
        exit()
    return cp_rabbit[adr]

def time_now():
    return datetime.now().strftime('%H:%M:%S')


def console_log(*args):
    print(f'[{time_now()}] {" ".join(args)}')


def rmq_connect(rabbit_address):
    # establish connection w RabbitMQ
    parameters = pika.URLParameters(rabbit_connection_str(rabbit_address))
    console_log("Working rmq adress", rabbit_address)
    connection = pika.BlockingConnection(parameters)
    console_log("Successful connection")
    return connection


def rmq_disconnect(connection):
    connection.close()