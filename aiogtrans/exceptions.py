from .constants import LANGUAGES


class LengthExceeded(Exception):
    """Exception raised when the maximum length is exceeded."""
    pass


class TextEmpty(Exception):
    """Exception raised when the text is empty."""
    pass


class SameSourceTarget(Exception):
    """Exception raised when the source is the same as the target."""
    pass


class UnsupportedLanguage(Exception):
    """Exception raised for unsupported languages."""

    def __init__(self, language):
        self.language = language

    def __str__(self):
        return f"No support for the provided language : '{self.language}'.\nPlease select one of the supported languages:\n{LANGUAGES}"


class TooManyRequests(Exception):
    "Exception raised if an error occurred during the request call."
    pass


class RequestError(Exception):
    "Exception raised if an error occurred during the request call."
    pass
