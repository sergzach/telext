# telext
An very simple library to create telegram bots with minimum customization.

### A simple example of "echo" bot

```python
import asyncio
import os

from telext import RawTelegramBot


async def main():
    # Creating our bot by specifying TELEGRAM_SERVER_URL=https://api.telegram.org
    # and a token of the bot.
    telegram_bot_client = RawTelegramBot(
        telegram_server_url=os.environ['TELEGRAM_SERVER_URL'],
        token=os.environ['BOT_TOKEN']
    )

    while True:
        # Get a user message.
        last_updates_raw_response = await telegram_bot_client.get_next_update(
            forget_previous_updates=True
        )

        result = last_updates_raw_response.json['result']

        if len(result) > 0:
            # There are new messages. Parse it...
            the_only_message = result[0]['message']

            chat_id = the_only_message['chat']['id']
            text = the_only_message['text']

            # ... then send a message back to the user.
            await telegram_bot_client.send_message(
                chat_id=chat_id,
                text=f'I am repeating your message: {text}.'
            )

        await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
```

### Draw graph in memory with plotly and send it to a customer

```python
"""
Getting an incomming message and repeat it - back to the user.
"""

import asyncio
import os
from io import BytesIO
from typing import BinaryIO

import plotly.express as px

from telext import RawTelegramBot


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

    while True:
        last_updates_raw_response = await telegram_bot_client.get_next_update(
            forget_previous_updates=True
        )
        result = last_updates_raw_response.json['result']

        if len(result) > 0:
            the_only_message = result[0]['message']
            chat_id = the_only_message['chat']['id']

            graph_in_memory = _draw_graph_in_memory()

            raw_response = await (
                telegram_bot_client.send_document_from_buffer(
                    chat_id=chat_id,
                    photo=graph_in_memory,
                    caption=(
                        f'This graph has been drawn in memory.'
                    ),
                )
            )
            l = 4

        await asyncio.sleep(0.5)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

```
