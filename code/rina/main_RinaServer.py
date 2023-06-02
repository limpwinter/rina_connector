import sys, os
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code')
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code\\rmq')
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code\\model')

from RinaController import RinaController

from rmq.RmqController import RmqController


class RinaServer:

    def start_server():
        try:
            rina_controller = RinaController()
            RmqController.start_consuming_from_tg(rina_controller)
        except KeyboardInterrupt:
            print("Interrupted")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

if __name__ == '__main__':
    RinaServer.start_server()