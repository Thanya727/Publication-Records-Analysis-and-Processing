from copy import copy
import fanfics
import spells
import Onion_Text
from itertools import chain
from nltk import download, pos_tag
from nltk.tokenize import TreebankWordTokenizer, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter
from random import sample
from functools import cache
from string import punctuation

download("punkt")
download("averaged_perceptron_tagger")
STOPWORDS = set(stopwords.words("english"))


@cache
def tokenise(doc: str) -> [str]:
    return TreebankWordTokenizer().tokenize(doc)


def stem(tokens: [str]) -> [str]:
    stemmer = PorterStemmer()
    return [stemmer.stem(tok) for tok in tokens]


def tag_pos(sentences: [str]):
    return [pos_tag(tokenise(s)) for s in sentences]


def dealwith_page(pack):
    docs = pack.get()
    tokenised = [[t for t in tokenise(d) if t.lower() not in STOPWORDS and t not in punctuation]
                 for d in docs]
    stemmed = [stem(tokens) for tokens in tokenised]
    all_tokens = list(chain.from_iterable(tokenised))
    all_stems = list(chain.from_iterable(stemmed))

    sentences = list(chain.from_iterable(sent_tokenize(doc) for doc in docs))

    sentence_lengths = Counter([len(s) for s in sentences])

    rand_sentences = sample(sentences, 3)
    tagged_rand = tag_pos(rand_sentences)

    print(pack.__name__)
    print(Counter(copy(all_tokens)).most_common(20))
    print(Counter(copy(all_stems)).most_common(20))
    print(sentence_lengths)
    print(tagged_rand)
    print("")
    return all_tokens, all_stems, tagged_rand, sentences


def main():
    return [dealwith_page(pack) for pack in [fanfics, spells, Onion_Text]]


if __name__ == "__main__":
    main()
