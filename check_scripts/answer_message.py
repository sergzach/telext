"""
Getting an incomming message and repeat it - back to the user.
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

        result = last_updates_raw_response.json['result']

        if len(result) > 0:
            the_only_message = result[0]['message']

            chat_id = the_only_message['chat']['id']
            text = the_only_message['text']

            await custom_telegram_api.send_text_message(
                chat_id=chat_id,
                text=f'I am repeating your message: {text}.'
            )

        await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
