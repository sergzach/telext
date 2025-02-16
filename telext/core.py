from dataclasses import dataclass
from typing import Callable

import aiohttp


@dataclass
class RawResponse:
    status: int
    text: str | None = None
    json: dict | list | None = None


class InputDataValidationError(Exception):
    pass


class RawTelegramBot:
    # Except (empty list):
    # - chat_member,
    # - message_reaction,
    # - message_reaction_count.
    _DEFAULT_ALLOWED_UPDATES = []

    def __init__(self, telegram_server_url: str, token: str):
        self._telegram_server_url = telegram_server_url
        self._token = token
        self._last_update_id: int | None = None

    def _get_method_url(self, *, method: str) -> str:
        return f'{self._telegram_server_url}/bot{self._token}/{method}'

    async def get_with_response(self, *, method: str, **data) -> RawResponse:
        async with aiohttp.ClientSession() as session:
            method_url = self._get_method_url(method=method)

            async with session.get(method_url, data=data) as resp:
                status = resp.status
                text = None
                json = None

                try:
                    json = await resp.json()
                except Exception:
                    text = await resp.text()

                return RawResponse(status=status, json=json, text=text)

    def _renew_last_update_id(self, raw_response: RawResponse):
        json = raw_response.json

        if json is not None and len(json['result']) > 0:
            self._last_update_id = max(
                [one_update['update_id'] for one_update in json['result']]
            )

    async def get_next_update(
            self,
            *,
            allowed_updates: list[str] | None = None,
            forget_previous_updates: bool = True
    ) -> RawResponse:
        allowed_updates = allowed_updates or self._DEFAULT_ALLOWED_UPDATES

        data = dict(
            limit=1,
            allowed_updates=allowed_updates
        )

        if forget_previous_updates and self._last_update_id is not None:
            data['offset'] = self._last_update_id + 1

        raw_response: RawResponse = await self.get_with_response(
            method='getUpdates',
            **data
        )

        self._renew_last_update_id(raw_response)

        return raw_response

    async def send_message(self, *, chat_id: int | str, text: str):
        data = dict(
            chat_id=chat_id,
            text=text
        )

        await self.get_with_response(
            method='sendMessage',
            **data
        )
