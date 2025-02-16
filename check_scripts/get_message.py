"""
Getting incomming messages etc. - in raw mode.
"""

import asyncio
import os

from telext import RawTelegramBot, CustomTelegramApi


async def main():
    telegram_bot_client = RawTelegramBot(
        telegram_server_url=os.environ['TELEGRAM_SERVER_URL'],
        token=os.environ['BOT_TOKEN']
    )
    custom_telegram_api = CustomTelegramApi(telegram_bot_client)

    while True:
        last_updates_raw_response = await custom_telegram_api.get_next_update(
            forget_previous_updates=True
        )

        print(f'f{last_updates_raw_response=!r}')

        if len(last_updates_raw_response.json['result']) == 0:
            print('(No more telegram updates.)')
            break

        await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
