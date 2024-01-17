from utils import read_page
from bs4 import BeautifulSoup
import re

SEARCH_LINK = "https://archiveofourown.org/works/search?work_search%5Bquery%5D=&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=8+years&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=&work_search%5Blanguage_id%5D=en&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=kudos_count&work_search%5Bsort_direction%5D=asc&commit=Search"

WORK_REGEX = re.compile("work_(\d{6})")


def handle_list_item(list_item: str) -> str:
    work_id = re.match(WORK_REGEX, list_item["id"]).groups()[0]
    fic_html = read_page(f"https://archiveofourown.org/works/{work_id}/")

    fic = BeautifulSoup(fic_html, "html.parser")
    tale = fic.find(id="chapter-1")
    return tale.get_text()


def get() -> [str]:
    html = read_page(SEARCH_LINK)

    soup = BeautifulSoup(html, "html.parser")
    return [handle_list_item(i) for i in soup.find_all(name="li", id=re.compile(WORK_REGEX))[:10]]



