import asyncio
import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

async def main():
    client = TelegramClient(
        'host',
        int(os.getenv('TG_API_ID')),
        os.getenv('TG_API_HASH')
    )

    await client.connect()

    qr = await client.qr_login()

    import qrcode

    img = qrcode.QRCode(border=1)
    img.add_data(qr.url)
    img.print_ascii()

    print("Открой Telegram → Настройки → Устройства → Подключить устройство")
    print("QR-ссылка (открой в браузере, если не хочешь ASCII):")
    print(qr.url)

    await qr.wait()   # ждём подтверждение

    print("Авторизация завершена, сессия сохранена")
    await client.disconnect()

asyncio.run(main())
