import sys
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code')
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code\\rina')
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code\\rmq')
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code\\model')

import asyncio

from TgController import TgController
from TgView import TgView

from rmq.RmqController import RmqController


BOT_TOKEN = '6025774622:AAHHZjjL3ZiIXC9WhNgkhm_c_Gtuu5ieYis'


class TgServer():

    async def start_server():
        tg_view = TgView(BOT_TOKEN)
        tg_controller = TgController(tg_view)

        await tg_view.set_controller(tg_controller)
        await tg_controller.run()
        RmqController.start_consuming_from_rina(tg_controller)

if __name__ == '__main__':
    asyncio.run(TgServer.start_server())