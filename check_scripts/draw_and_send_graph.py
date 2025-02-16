"""
Draw graph and send it to a user - as answer to any message.
"""

import asyncio
import os
from io import BytesIO

import plotly.express as px

from telext import RawTelegramBot, TelegramCustomApi


def _draw_graph_in_memory() -> BytesIO:
    buf = BytesIO()

    fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])

    buf.write(fig.to_image(format='png'))

    buf.seek(0)

    return buf


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

            graph_in_memory = _draw_graph_in_memory()

            await (
                telegram_custom_api.send_document_from_buffer(
                    chat_id=chat_id,
                    photo=graph_in_memory,
                    caption=(
                        f'This graph has been drawn in memory.'
                    ),
                )
            )

        await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
