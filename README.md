# telext
A small and extendable library to create telegram bots with minimum customization.

It's easy to add new methods according to fast-growing https://core.telegram.org/bots/api.

### Key Features

- **It's extendable**: you may inherits from `telext.CustomTelegramApiBase` or `telext.CustomTelegramApi`.
- **It's small**: it's really tiny and easy-to-understand.
- **It's asynchronious:** it works with `asyncio`.

##### A simple example of "echo" bot

```python
import asyncio
import os

from telext import RawTelegramBot, CustomTelegramApi


async def main():
    telegram_bot_client = RawTelegramBot(
        telegram_server_url="https://api.telegram.org",
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
```

##### Draw graph in memory with plotly and send it to a customer

```python
import asyncio
import os
from io import BytesIO

import plotly.express as px

from telext import RawTelegramBot, CustomTelegramApi


def _draw_graph_in_memory() -> BytesIO:
    buf = BytesIO()

    fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])

    buf.write(fig.to_image(format='png'))
    buf.seek(0)

    return buf


async def main():
    telegram_bot_client = RawTelegramBot(
        telegram_server_url="https://api.telegram.org",
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

            graph_in_memory = _draw_graph_in_memory()

            await (
                custom_telegram_api.send_document_from_buffer(
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
```
