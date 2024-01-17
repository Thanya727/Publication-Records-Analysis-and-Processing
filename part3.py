from collections import Counter
from os import remove
from typing import List
from utils import read_page, get_or
from bs4 import BeautifulSoup
import re
from nltk import download
from nltk.tokenize.api import TokenizerI
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize.mwe import MWETokenizer
from nltk.corpus import stopwords
from string import punctuation
from datetime import datetime
from os.path import exists
from multiprocessing import Pool


download("stopwords")
CONF_URL = "https://dblp.org/db/conf/aaai/index.html"
CONF_REGEX = r"conf/aaai/(\d{2,4})"
STOPWORDS = set(stopwords.words("english"))
CACHE_DIR = "./part_3_cache/"


def printl(list):
    for e in list:
        print(e)


def read_article(url):
    try:
        soup = BeautifulSoup(read_page(url), features="html.parser")
    except ValueError:
        print(f"failed to read {url}")
        return ""
    try:
        title = soup.find("h1", {"class": "page_title"}).text
        abstract = "\n".join(soup.find(
            "section", {"class": "item abstract"}).text.split("\n")[2:])
    except AttributeError:
        print(url)
        return get_or(soup.find("h1", {"class": "page_title"}),
                      lambda i: i.text, "").replace("\\", "\\\\")
    return (title + " " + abstract).replace("\\", "\\")


def get_papers(url):
    print(f"{datetime.now()}: Starting a year!")
    try:
        year = re.search(r"aaai(\d{2,4})", url).groups()[0]
    except AttributeError as e:
        print(url)
        raise e
    path = f"{CACHE_DIR}{year}.txt"
    if exists(path):
        with open(path, "r", encoding="utf-8") as cache:
            return cache.read()

    soup = BeautifulSoup(read_page(url), features="html.parser")
    article_points = soup.find_all("li", {"class": "entry inproceedings"})

    if int(year) <= 2009:
        body = "\n".join(p.find("cite").find(
            "span", {"class": "title"}).text for p in article_points)
    else:
        article_links = (p.find("nav")
                         .find("ul")
                         .find("li")
                         .find("div")
                         .find("a")["href"] for p in article_points)
        with Pool() as pool:
            body = "".join(pool.imap_unordered(
                read_article, article_links, 10))

    with open(path, "w", encoding="utf-8") as cache:
        try:
            cache.write(body)
        except UnicodeEncodeError:
            # If it doesn't work, just don't cache it!
            print("failed to cache!")
            remove(path)
    return body


class BPETokeniser(TokenizerI):
    def __init__(self, text, num_iters=10_000, base_tokeniser=wordpunct_tokenize, invalid_tok=lambda _: False):
        print("tokenising...")
        self.base_tokeniser = base_tokeniser
        self.invalid_tok = invalid_tok
        tokens = self._tokenise_init(text)
        word_pairs = []
        for _ in range(num_iters):
            pairs = list(zip(tokens, tokens[1:]))
            pair_freqs = Counter(pairs)
            new_token = self._flatten(
                max(pair_freqs, key=lambda p: pair_freqs[p]))
            word_pairs.append(new_token)
            tokens = self._merge_pair(pairs, new_token)

        self.pair_tokeniser = MWETokenizer(word_pairs)

    def _isvalidtoken(self, token):
        return all([token not in STOPWORDS,
                    token not in punctuation,
                    not token.isnumeric(),
                    *[punct not in token for punct in punctuation if punct != "-"],
                    not self.invalid_tok(token)
                    ])

    @staticmethod
    def _flatten(mytuple):
        left, right = mytuple
        if type(left) is tuple:
            return (*left, right)
        elif type(right) is tuple:
            return (left, *right)
        else:
            return mytuple

    def _tokenise_init(self, text):
        return [tok.lower()
                for tok in self.base_tokeniser(text) if self._isvalidtoken(tok)]

    def _merge_pair(self, pairs, tomeld):
        if tomeld[0] == "deep" and tomeld[1] == "learning":
            print("deep learning")
        skip = False
        output = []
        for pair in pairs:
            if skip:
                skip = False
                continue
            elif pair == tomeld:
                output.append(tomeld)
                skip = True
            else:
                output.append(pair[0])
        return output

    def tokenize(self, s: str) -> List[str]:
        orig_tokens = self._tokenise_init(s)
        return self.pair_tokeniser.tokenize(orig_tokens)


def main():
    soup = BeautifulSoup(read_page(CONF_URL), features="html.parser")
    uls = soup.find_all("ul", {"class": "publ-list"})
    procs = (ul.find(id=lambda i: re.match(CONF_REGEX, i)) for ul in uls)
    urls = (proc.find("a", {"class": "toc-link"})["href"] for proc in procs)
    years = [get_papers(url) for url in urls]
    full_corpus = "\n".join(years)
    tokeniser = BPETokeniser(full_corpus)
    overall_counter = Counter(tokeniser.tokenize(full_corpus))
    one_time_tokens = {
        token for token in overall_counter if overall_counter[token] <= 1}
    print("tokenised!")
    token_freqs = [Counter(token
                           for token in tokeniser.tokenize(year)
                           if token not in one_time_tokens) for year in years]

    def normalised_frequency(t): return t[1] - overall_counter[t[0]]/len(years)
    freqsorts = [[i[0] for i in sorted(year.items(), key=normalised_frequency, reverse=True)]
                 for year in token_freqs]
    printl([i[:10] for i in freqsorts])
    return freqsorts


if __name__ == "__main__":
    main()
