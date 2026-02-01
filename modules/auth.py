import qrcode
import asyncio
import aiofiles.os
import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

async def check_exists_session_telegram():
    if await aiofiles.os.path.exists("host.session"):
        print("success")
        return True
    else:
        print("false") 
        return False



async def get_session():
    client = TelegramClient(
        'host',
        int(os.getenv('TG_API_ID')),
        os.getenv('TG_API_HASH')
    )
    if not await check_exists_session_telegram():
        try:
            await client.connect()
            qr = await client.qr_login()
            img = qrcode.QRCode(border=1)
            img.add_data(qr.url)
            img.print_ascii()
            print("Открой Telegram → Настройки → Устройства → Подключить устройство")
            print("QR-ссылка (открой в браузере, если не хочешь ASCII):")
            print(qr.url)
            await qr.wait()   # ждём подтверждение
            print("Авторизация завершена, сессия сохранена")
            # await client.disconnect()
        except asyncio.TimeoutError:
            print("Авторизация не удалась :(")
    return await client.start()

if __name__ == '__main__':
    asyncio.run(get_session())
