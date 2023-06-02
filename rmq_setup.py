import rmq_common_tools as rmq_tools  
import traceback 


def create_que(params, channel):
    try:
        channel.queue_declare(queue=params.queue, durable=params.durable)
        rmq_tools.console_log("Q", params.queue, "created succcessfully")
    except Exception:
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Error (queue)!")


def create_exch(params, channel):
    try:
        channel.exchange_declare(exchange=params.exch, exchange_type=params.type, 
                                 durable=params.durable)
        rmq_tools.console_log("Exchange", params.exch, "created succcessfully")
    except Exception:
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Error (exchange)!")


def delete(params, channel):
    if params.queue:
        try:
            channel.queue_delete(queue=params.queue)
            rmq_tools.console_log("Queue", params.queue, "deleted succcessfully")
        except Exception:
            rmq_tools.console_log("Error:\n", traceback.format_exc())
            rmq_tools.console_log("Error deliting q!")
    elif params.exch:
        try:
            channel.exchange_delete(exchange=params.exch)
            rmq_tools.console_log("Exchange", params.exch, "ddeleted succcessfully")
        except Exception:
            rmq_tools.console_log("Error:\n", traceback.format_exc())
            rmq_tools.console_log("Error deleting exchange!")


def bind(params, channel):
    try:
        channel.queue_bind(exchange=params.exch, queue=params.queue, routing_key=params.r_key)
        rmq_tools.console_log("Messages from routing_key = ",
                              params.r_key, "\nsuccesfully bind from  ", params.exch, "\nto q",
                              params.queue)
    except Exception:
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Error creating binding!")


def unbind(params, channel):
    try:
        channel.queue_unbind(exchange=params.exch, queue=params.queue, routing_key=params.r_key)
        rmq_tools.console_log("Unbing routing_key = ",
                              params.r_key, "\n from ", params.exch, "\nto q",
                              params.queue, " ")
    except Exception:
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Error deleting binding!")


def purge(params, channel):
    try:
        channel.queue_purge(queue=params.queue)
        rmq_tools.console_log("Q ", params.queue, "purged succcessfully")
    except Exception:
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Error purging queue", params.queue, " ")


def do_connect():
    #TODO:
    rabbit_address = " TODO "
    rmq_connection = rmq_tools.rmq_connect(rabbit_address)
    rmq_channel = rmq_connection.channel()
    