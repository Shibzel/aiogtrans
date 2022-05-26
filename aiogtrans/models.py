from bs4 import BeautifulSoup


class Languages:
    def __init__(
        self,
        cls: BeautifulSoup
    ):
        self._bsoup = cls

    @property
    def source(self):
        input_container = self._bsoup.find(
            "div", attrs={"class": "input-container"})
        return input_container.find(
            "input", attrs={"name": "hl"}).get("value")[:2]

    @property
    def target(self):
        input_container = self._bsoup.find(
            "div", attrs={"class": "input-container"})
        return input_container.find(
            "input", attrs={"name": "tl"}).get("value")[:2]


class Translated(Languages):
    def __init__(
        self,
        original_text: str,
        cls: BeautifulSoup,
    ):
        self._original = original_text
        super().__init__(cls)

    def __str__(self):
        return self.text

    @property
    def text(self) -> str:
        """The translated text."""
        return self._bsoup.find(
            name="div",
            attrs={
                "class": "result-container"
            }
        ).text

    @property
    def original(self) -> str:
        """The original text."""
        return self._original
