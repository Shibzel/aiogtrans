from bs4 import BeautifulSoup


class Languages:
    def __init__(self, cls: BeautifulSoup):
        self.bsoup = cls

    @property
    def source(self):
        input_container = self.bsoup.find(
            "div", attrs={"class": "input-container"})
        return input_container.find(
            "input", attrs={"name": "hl"}).get("value")[:2]

    @property
    def target(self):
        input_container = self.bsoup.find(
            "div", attrs={"class": "input-container"})
        return input_container.find(
            "input", attrs={"name": "tl"}).get("value")[:2]


class Translated:
    def __init__(self, original_text, cls: BeautifulSoup):
        self._original = original_text
        self.bsoup = cls
        self.languages = Languages(self.bsoup)

    def __str__(self):
        return self.text

    @property
    def text(self) -> str:
        return self.bsoup.find("div", attrs={"class": "result-container"}).text

    @property
    def original(self) -> str:
        return self._original

    @property
    def source(self) -> str:
        return self.languages.source

    @property
    def target(self) -> str:
        return self.languages.target
