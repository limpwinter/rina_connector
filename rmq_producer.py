import rmq_common_tools as rmq_tools  
import traceback  


def from_file(params, channel):
    try:
        text = params.message_file.read()
        channel.basic_publish(exchange=params.exch, routing_key=params.r_key, body=text)
        rmq_tools.console_log("Message: \n", text, "\n f routing_key =", params.r_key,
                              "\nsuccessfully published exchange - ", params.exch)
    except Exception:
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Error publishing!")


def producer_connect(rabbit_address):
    rmq_connection = rmq_tools.rmq_connect(rabbit_address)
    rmq_channel = rmq_connection.channel()


def producer_disconnect(rmq_connection):
    rmq_tools.rmq_disconnect(rmq_connection)