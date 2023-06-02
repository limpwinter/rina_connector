import rmq_common_tools as rmq_tools 
import traceback  


# Handler for messages read from the rmq. 
# NOW: Writes the received message to a file or outputs to the console. TDDO
def on_message(channel, method_frame, header_frame, body):
    global all_cnt, lim
    if all_cnt >= lim:
        rmq_tools.console_log('Info collected.')
        raise KeyboardInterrupt
    body_str = body.decode("utf-8")[:4000]
    rkey = method_frame.routing_key
    all_cnt = all_cnt + 1
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def create_que(params, channel):
    try:
        channel.queue_declare(queue=params.queue)
        rmq_tools.console_log("Q ", params.queue, "created successfully ")
    except Exception:
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Q ", params.queue, "already in rmq!")
        exit()


def bind(params, channel):
    try:
        channel.queue_bind(exchange=params.exch, queue=params.queue, routing_key=params.r_key)
        rmq_tools.console_log("Messages from routing_key = ",
                              params.r_key, "\nsuccessflly bind from  ",
                              params.exch, "\nto Q", params.queue)
    except Exception:
        delete(params, channel)
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Error creating binding!")
        exit()


def purge(params, channel):
    try:
        channel.queue_purge(queue=params.queue)
        rmq_tools.console_log("Q", params.queue, "successfully purged")
    except Exception:
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Error purge Q", params.queue, "!")


def delete(params, channel):
    try:
        channel.queue_delete(queue=params.queue)
        rmq_tools.console_log("Q", params.queue, "successfully deleted")
    except Exception:
        rmq_tools.console_log("Error:\n", traceback.format_exc())
        rmq_tools.console_log("Error delete Q!")


def from_existing_que(params, channel):
    rmq_tools.console_log("Starting from_existing_que...")
    channel.basic_consume(on_message, queue=params.queue)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        rmq_tools.console_log("Error:\n", traceback.format_exc())


def from_tmp_que(params, channel):
    create_que(params, channel)
    bind(params, channel)
    from_existing_que(params, channel)
    purge(params, channel)
    delete(params, channel)


def disconnect_consumer(rmq_connection):
    rmq_tools.rmq_disconnect(rmq_connection)