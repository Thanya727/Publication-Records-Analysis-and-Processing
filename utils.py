
from urllib.request import FancyURLopener
from time import sleep


class Opener(FancyURLopener):
    version = "Mozilla/5.0"


def read_page(url, tries=5):
    try:
        with Opener().open(url) as page:
            return page.read()
    except ValueError as e:
        if tries <= 0:
            raise e
        sleep(0.5)
        return read_page(url, tries-1)


def get_or(item, action, default): return default if item is None else action(item)
