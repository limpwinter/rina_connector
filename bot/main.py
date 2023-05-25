import asyncio
from TgController import TgController
from TgView import TgView

BOT_TOKEN = '6025774622:AAHHZjjL3ZiIXC9WhNgkhm_c_Gtuu5ieYis'

async def main():
    tg_view = TgView(BOT_TOKEN)
    tg_controller = TgController(tg_view)

    # Setting controller after creating it
    await tg_view.set_controller(tg_controller)

    await tg_controller.run()

# Main execution
if __name__ == '__main__':
    asyncio.run(main())
