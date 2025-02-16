import asyncio
import os

from src.core import RawTelegramBot


async def main():
    telegram_bot_client = RawTelegramBot(
        telegram_server_url=os.environ['TELEGRAM_SERVER_URL'],
        token=os.environ['BOT_TOKEN']
    )

    response = await telegram_bot_client.get_with_response(
        method='getMe'
    )

    print(f'{response=!r}')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
