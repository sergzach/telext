from dataclasses import dataclass

import aiohttp


@dataclass
class RawResponse:
    status: int
    text: str | None = None
    json: dict | list | None = None


class RawTelegramBot:
    def __init__(self, telegram_server_url: str, token: str):
        self._telegram_server_url = telegram_server_url
        self._token = token

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

    async def post_with_response(
            self,
            *,
            method: str,
            **data
    ) -> RawResponse:
        async with aiohttp.ClientSession() as session:
            method_url = self._get_method_url(method=method)

            async with session.post(method_url, data=data) as resp:
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
