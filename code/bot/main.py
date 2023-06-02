import sys
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code')
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code\\rina')
sys.path.append('c:\\Users\\Mitya\\Documents\\rina_connector\\code\\rmq')

import asyncio

from TgController import TgController
from TgView import TgView



BOT_TOKEN = '6025774622:AAHHZjjL3ZiIXC9WhNgkhm_c_Gtuu5ieYis'

async def main():
    tg_view = TgView(BOT_TOKEN)
    tg_controller = TgController(tg_view)

    await tg_view.set_controller(tg_controller)
    await tg_controller.run()

if __name__ == '__main__':
    asyncio.run(main())