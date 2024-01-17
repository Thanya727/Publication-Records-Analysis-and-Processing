from utils import read_page
from bs4 import BeautifulSoup
from random import sample


SPELL_LIST = "https://www.aidedd.org/dnd-filters/spells-5e.php"


def description(spell_url):
    htmspell = read_page(spell_url)  # forgive my punning
    potion = BeautifulSoup(htmspell, "html.parser")
    return potion.find("div", {"class": "description"}).get_text()


def get():
    html = read_page(SPELL_LIST)
    soup = BeautifulSoup(html, "html.parser")
    # TODO: is this actually what this is
    spells = soup.find_all("a", {"class": ""})
    spell_links = [spell["href"]
                   for spell in spells[12:-1]]  # get rid of header rows
    select_spells = sample(spell_links, 20)
    return [description(spell) for spell in select_spells]
