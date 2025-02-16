"""
Sending image from URL (in the Internet).
"""

import asyncio
import os

from telext import RawTelegramBot, TelegramCustomApi


async def main():
    telegram_bot_client = RawTelegramBot(
        telegram_server_url=os.environ['TELEGRAM_SERVER_URL'],
        token=os.environ['BOT_TOKEN']
    )
    telegram_custom_api = TelegramCustomApi(telegram_bot_client)

    while True:
        last_updates_raw_response = await telegram_custom_api.get_next_update(
            forget_previous_updates=True
        )

        result = last_updates_raw_response.json['result']

        if len(result) > 0:
            the_only_message = result[0]['message']

            chat_id = the_only_message['chat']['id']

            await telegram_custom_api.send_photo_from_image_url(
                chat_id=chat_id,
                url=os.environ['CHECK_SCRIPTS_IMAGE_URL'],
                caption=f'Picture as answer to your message.',
            )

        await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
