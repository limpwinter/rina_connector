from consumer_Rina import RinaConsumer

import sys, os

class RinaServer:
    def start_server():
        try:
            RinaConsumer.receive_response_Rina()
        except KeyboardInterrupt:
            print("Interrupted")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


if __name__ == '__main__':
    RinaServer.start_server()
