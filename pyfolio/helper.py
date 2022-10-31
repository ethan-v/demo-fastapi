from urllib.parse import urlparse


class Helper:

    @staticmethod
    def get_hostname_from_url(url: str) -> str:
        return urlparse(url).netloc
