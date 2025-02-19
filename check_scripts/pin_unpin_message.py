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
            # Possible 2 updates - one for message
            # and one that message has been pinned.

            the_only_message = result[0]['message']

            chat_id = the_only_message['chat']['id']
            message_id = the_only_message['message_id']

            await custom_telegram_api.send_text_message(
                chat_id=chat_id,
                text='I pinned your last message.'
            )

            await custom_telegram_api.pin_chat_message(
                chat_id=chat_id,
                message_id=message_id
            )

            await asyncio.sleep(3.0)

            await custom_telegram_api.unpin_chat_message(
                chat_id=chat_id,
                message_id=message_id
            )

            await custom_telegram_api.send_text_message(
                chat_id=chat_id,
                text='I have unpinned your last message.'
            )

        await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
