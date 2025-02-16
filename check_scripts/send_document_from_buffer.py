"""
Getting an incomming message and repeat it - back to the user.
"""

import asyncio
import os
from pathlib import Path

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

            image_path = (
                Path(__file__).parent.resolve()
                / 'data'
                / 'photo_2025-02-16_10-13-22.jpg'
            )

            with open(image_path, 'rb') as photo:
                await telegram_custom_api.send_document_from_buffer(
                    chat_id=chat_id,
                    photo=photo,
                    caption=f'Picture (from disk) as answer to your message.',
                )

            document_path = (
                Path(__file__).parent.resolve()
                / 'data'
                / 'eosrt3-eos1100d-bim2-c-en.pdf'
            )

            with open(document_path, 'rb') as document:
                await (
                    telegram_custom_api.send_document_from_buffer(
                        chat_id=chat_id,
                        document=document,
                        caption=(
                            f'A PDF document (from disk) '
                            f'as answer to your message.'
                        ),
                    )
                )

        await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
