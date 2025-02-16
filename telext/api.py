from io import BytesIO
from typing import BinaryIO

from telext import RawTelegramBot, RawResponse


class InputDataValidationError(Exception):
    pass


class CustomTelegramApiBase:
    # Except (empty list):
    # - chat_member,
    # - message_reaction,
    # - message_reaction_count.
    _DEFAULT_ALLOWED_UPDATES = []

    def __init__(self, raw_telegram_bot: RawTelegramBot):
        self._raw_telegram_bot = raw_telegram_bot
        self._last_update_id: int | None = None

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

        raw_response: RawResponse = (
            await self._raw_telegram_bot.get_with_response(
                method='getUpdates',
                **data
            )
        )

        self._renew_last_update_id(raw_response)

        return raw_response


class CustomTelegramApi(CustomTelegramApiBase):
    """
    An Extendable API: https://core.telegram.org/bots/api.
    """
    _MSG_SPECIFY_PHOTO_OR_DOCUMENT = 'Specify <photo> or <document>.'

    async def send_text_message(
            self,
            *,
            chat_id: int | str,
            text: str
    ):
        data = dict(
            chat_id=chat_id,
            text=text
        )

        await self._raw_telegram_bot.get_with_response(
            method='sendMessage',
            **data
        )

    async def send_photo_from_image_url(
            self,
            *,
            chat_id,
            url: str,
            caption: str = None
    ):
        data = dict(photo=url)

        if caption is not None:
            data['caption'] = caption

        await self._raw_telegram_bot.get_with_response(
            method='sendPhoto',
            chat_id=chat_id,
            **data
        )

    async def send_document_from_buffer(
            self,
            *,
            chat_id,
            photo: BinaryIO | BytesIO | None = None,
            document: BinaryIO | BytesIO | None = None,
            caption: str = None
    ) -> RawResponse:
        if not any([photo, document]):
            raise InputDataValidationError(self._MSG_SPECIFY_PHOTO_OR_DOCUMENT)

        data = dict()
        method = None

        if photo is not None:
            method = 'sendPhoto'
            data.update(photo=photo)
        elif document is not None:
            method = 'sendDocument'
            data.update(document=document)

        if caption is not None:
            data['caption'] = caption

        return await self._raw_telegram_bot.post_with_response(
            method=method,
            chat_id=str(chat_id),
            **data
        )
