import aiohttp
from bs4 import BeautifulSoup

from exceptions import (
    LengthExceeded,
    TextEmpty,
    SameSourceTarget,
    UnsupportedLanguage,
    TooManyRequests,
    RequestError
)
from constants import LANGUAGES
from models import Translated


def is_input_valid(text: str, limit: int = 5000) -> bool:
    """Checks if the text is standarts or not.

    Args:
        text (str): Source text.
        limit (int, optional): Limit of characters. Defaults to 5000.

    Returns:
        bool
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")
    elif len(text) > limit:
        raise LengthExceeded(
            f"Maximum length exceeded : {len(text)} (text) --> {limit} (limit).")
    elif text == "":
        raise TextEmpty("The text is empty.")
    return True


def get_supported_languages_codes() -> list:
    """Returns a list of supported languages.

    Returns:
        list
    """
    return list(LANGUAGES.values())


class GoogleTrans:
    """The google translator class that wraps functions to detect and translate text.

    Args:
        source (str, optional): Language of the text. Defaults to "auto".
        target (str, optional): Target language. Defaults to "en".
        session (`aiohttp.ClientSession`, optional): Your aiohttp client session, if there is one. Defaults to None.
        url (str, optional): Your custom url, must end with "/m" to get the simplified version of the website.
        proxy (str, optional): Should looks like this : "http://your_user:your_password@your_proxy_url:your_proxy_port". Defaults to None.

    Funcs:
        (coro) close() -> None: Closes the aiohttp session.
        (coro) translate(text:str) -> str: Translates a text.
            Example:
                >>> translator = GoogleTrans(source="en", target="fr")
                >>> await translator.translate("ayo, i got a pizza here")
                returns: `aiogtrans.models.Translated`
                str: "Ayo, j'ai une pizza ici"
        (coro) detect(text:str) -> tuple : Detects the language.
            Example:
                >>> result = await translator.detect("Amo i bambini 😳")
                returns: ('italian', 'it')
                >>> result[1]
                returns: 'it'
    """

    def __init__(
        self,
        source: str = "auto",
        target: str = "en",
        session: aiohttp.ClientSession = None,
        url: str = "http://translate.google.com/m",
        proxy: str = None
    ):
        if source == target:
            raise SameSourceTarget(
                f"The source and the target cant be the same : '{source}' (source) --> '{target}' (target)")

        if source in LANGUAGES.keys():
            source = LANGUAGES[source]
        elif source != "auto" and not source in LANGUAGES.values():
            raise UnsupportedLanguage(source)

        if target in LANGUAGES.keys():
            target = LANGUAGES[target]
        elif not target in LANGUAGES.values():
            raise UnsupportedLanguage(target)

        self.source = source
        self.target = target
        self.proxy = proxy
        self.session = session if session else aiohttp.ClientSession()
        self.url = url

    async def close(self) -> None:
        """Closes the aiohttp session."""
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exception_type, exception_value, traceback):
        await self.close()

    async def translate(self, text: str) -> Translated:
        """Translates a text.

        Args:
            text (str) : Original text.

        Returns:
            str: Translated text.

        Example:
            >>> translator = GoogleTrans(source="en", target="fr")
            >>> await translator.translate("ayo, i got a pizza here")
            returns: `aiogtrans.models.Translated`
            str: "Ayo, j'ai une pizza ici"
        """
        if is_input_valid(text):
            async with self.session.get(
                self.url,
                params={
                    "client": "webapp",
                    "sl": self.source,
                    "tl": self.target,
                    "q": text
                },
                proxy=self.proxy,
            ) as response:

                if response.status == 429:
                    raise TooManyRequests(
                        "You made too many requests (maximum : 5 req/sec and 200k req/day).")
                if response.status != 200:
                    raise RequestError(
                        "Error while trying to make a request call to the API, try again and check your connexion.")

                return Translated(original_text=text, cls=BeautifulSoup(await response.text(), "html.parser"))

    async def detect(self, text: str) -> tuple:
        """Detects the language.

        Args:
            text (str): Original text.

        Returns:
            tuple: Language and code.

        Example:
            >>> result = await translator.detect("Amo i bambini 😳")
            returns: ('italian', 'it')
            >>> result[1]
            returns: 'it'
        """
        result = (await self.translate(text)).source
        return (
            list(LANGUAGES.keys())[list(LANGUAGES.values()).index(
                result)],  # Gets the key by value
            result
        )


if __name__ == "__main__":
    import asyncio
    import time

    async def main():
        async with GoogleTrans() as translator:
            start_time = time.time()
            result = await translator.translate("Never gonna give you up, never gonna let you down")
            print(str(result).upper())
            print(result.source)
            print("Took", round(time.time() - start_time, 2), "seconds.")
        # Useless, just here to let the code close the aiohttp session.
        await asyncio.sleep(0.5)

    asyncio.run(main())
