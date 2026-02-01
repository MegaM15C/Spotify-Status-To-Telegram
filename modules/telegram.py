import qrcode
import asyncio
import aiofiles.os
import os
from telethon import TelegramClient, functions, errors
from telethon.types import UserFull
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
    if not await check_exists_session_telegram():
        try:
            client = TelegramClient(
                'host',
                int(os.getenv('TG_API_ID')),
                os.getenv('TG_API_HASH')
            )
            await client.connect()
            qr = await client.qr_login()
            img = qrcode.QRCode(border=1)
            img.add_data(qr.url)
            img.print_ascii()
            print("Open Telegram → Settings → Devices → Connect a device")
            print("QR link (open in browser if you don’t want ASCII):")
            print(qr.url)
            await qr.wait()   # wait for confirmation
            print("Authorization completed, session saved")
            await client.disconnect()
        except asyncio.TimeoutError:
            print("Authorization failed :(")
    client = TelegramClient(
        'host',
        int(os.getenv('TG_API_ID')),
        os.getenv('TG_API_HASH')
    )
    return await client.start()



async def get_user_info(
    client: TelegramClient
) -> tuple[UserFull, bool]:
    try:
        full_info = await client(functions.users.GetFullUserRequest('me'))
        # print(full_info.users[0].premium)  # True, если Premium
        return full_info, full_info.users[0].premium
    except errors.FloodWaitError as e:
        print(f"Flood wait: {e.seconds} sec")
        await asyncio.sleep(e.seconds)



async def update_telegram_status(
    client: TelegramClient,
    music:str,
    full_info:list
):
    try:
        stat = full_info.full_user.about
        if music != stat:
            await client(functions.account.UpdateProfileRequest(about=music))
    except errors.FloodWaitError as e:
        print(f"Flood wait: {e.seconds} sec")
        await asyncio.sleep(e.seconds)

if __name__ == '__main__':
    asyncio.run(get_session())
