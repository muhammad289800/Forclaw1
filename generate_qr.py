import asyncio
import qrcode
from telethon import TelegramClient, errors, functions
from telethon.sessions import StringSession

API_ID = '22727397'
API_HASH = 'bfd549b603b93787f122c6efbbd76fab'
PASSWORD = 'Muhammad1@%'

async def main():
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.connect()
    
    qr_login = await client.qr_login()
    print("Generating QR Code...")
    
    img = qrcode.make(qr_login.url)
    img.save("telegram_qr.png")
    print("QR Code saved as telegram_qr.png")
    
    try:
        user = await qr_login.wait(timeout=60)
        print(f"Logged in as {user.username}")
    except errors.SessionPasswordNeededError:
        print("2FA Password needed, logging in with password...")
        await client.sign_in(password=PASSWORD)
        user = await client.get_me()
        print(f"Logged in as {user.username} after 2FA")
    except asyncio.TimeoutError:
        print("QR Code expired.")
        return
    
    print(f"SESSION_STRING: {client.session.save()}")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
