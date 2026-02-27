from telethon import TelegramClient

# Your API ID and Hash
api_id = 22727397
api_hash = 'bfd549b603b93787f122c6efbbd76fab'

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Sending a message to yourself
    await client.send_message('me', 'Hello, this is a test message from the bot!')
    
with client:
    client.loop.run_until_complete(main())