import qrcode
import asyncio
import aiofiles.os
import os
from telethon import TelegramClient, functions, errors
from telethon.types import UserFull

async def check_exists_session_telegram() -> bool:
    """
    Check whether the Telegram session file exists.

    Returns:
        bool: 
            True if the session file exists,
            False if the session file does not exist.
    """
    if await aiofiles.os.path.exists("host.session"):
        # print("success")
        return True
    else:
        # print("false") 
        return False



async def get_session() -> TelegramClient:
    """
    Ensure an authorized TelegramClient session exists and return a started client.

    Workflow:
    - Check whether a Telegram session file already exists.
    - If the session does not exist:
        * Create a TelegramClient.
        * Initiate QR-code login.
        * Display the QR code (ASCII and URL) for authorization.
        * Wait for the user to confirm login in the Telegram app.
        * Save the session on successful authorization.
    - If authorization via QR times out, print an error message.
    - Create a TelegramClient again using the saved session.
    - Start the client and return it.

    Returns:
        TelegramClient: An initialized and authorized Telegram client instance.
    """
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
            print("Authorization failed :( . Restart the script")
    
    client = TelegramClient(
        'host',
        int(os.getenv('TG_API_ID')),
        os.getenv('TG_API_HASH')
    )
    return await client.start()



async def get_user_info(
    client: TelegramClient
) -> tuple[UserFull, bool]:
    """
    Retrieve full information about the current Telegram user.

    Workflow:
    - Send a request to Telegram API to fetch full user information for the
      authorized account ("me").
    - Extract and return:
        * The full user information object.
        * The user's Premium status.

    Error handling:
    - If a FloodWaitError occurs, print the required wait time and pause
      execution for the specified number of seconds before exiting the function.

    Args:
        client (TelegramClient): An active and authorized Telethon client.

    Returns:
        tuple[UserFull, bool]:
            - UserFull: Full information about the current user.
            - bool: True if the user has Telegram Premium, False otherwise.
    """
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
) -> None:
    """
    Update the Telegram profile "about" text with the provided status.

    Workflow:
    - Read the current "about" field from the already fetched full user info.
    - Compare it with the new status text.
    - Send an update request only if the text has changed, to avoid unnecessary API calls.

    Error handling:
    - If a FloodWaitError occurs, print the required wait time and pause
      execution for the specified number of seconds before exiting the function.

    Args:
        client (TelegramClient): An active and authorized Telethon client.
        music (str): New status text to be set in the Telegram profile.
        full_info (list): Full user information object containing the current
                          profile data (including the "about" field).

    Returns:
        None
    """
    try:
        stat = full_info.full_user.about
        if music != stat:
            await client(functions.account.UpdateProfileRequest(about=music))
    except errors.FloodWaitError as e:
        print(f"Flood wait: {e.seconds} sec")
        await asyncio.sleep(e.seconds)

if __name__ == '__main__':
    asyncio.run(get_session())
