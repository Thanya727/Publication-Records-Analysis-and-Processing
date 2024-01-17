import os
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# stopwords from nltk
import nltk
nltk.download('stopwords')

dir_path = 'part_3_cache'
files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.txt')]
files = sorted(files)
docs = []
for file in files:
    with open(os.path.join(dir_path, file), 'r', encoding='iso-8859-1') as f:
        docs.append(f.read())

# extra stopwords
stop_words = list(stopwords.words('english'))
extended_stop_words = ['outperforms', 'effectiveness', 'accuracy', 'due', 'low', 'recent', 'better', 'best', 'known', 'possible', 'previous', 'https', 'available', 'well', 'important', 'given', 'end', 'may', 'provide', 'several', 'often', 'consider', 'address', 'introduce', 'able', 'however', 'paper', 'show', 'propose', 'proposed', 'based', 'using', 'approach', 'results', 'method', 'methods', 'algorithm', 'problem', 'also', 'different', 'existing', 'experiments', 'demonstrate', 'work', 'used', 'many', 'present', 'number', 'art', 'datasets']
stop_words.extend(extended_stop_words)

# vectorise with stopwords, bigrams and frequency filter
vectorizer = TfidfVectorizer(stop_words=stop_words, ngram_range=(1, 3), max_df=0.85, min_df=0.05)
vectorizer.fit(docs)
responses = vectorizer.transform(docs)

# top n keyphrases
top_n = 10
for i, response in enumerate(responses):
    tfidf_sorting = sorted(list(zip(vectorizer.get_feature_names_out(), response.toarray()[0])), key=lambda x: x[1], reverse=True)
    top_keywords = [item[0] for item in tfidf_sorting][:top_n]
    print(f"Top keyphrases for {files[i]}:")
    print(top_keywords)

# Top keyphrases for 2000.txt:
# ['combinatorial auctions', 'xml', 'knowledge search', 'reasoning planning', 'agent development', 'course action', 'preliminary report', 'spoken dialogue system', 'preliminary', 'mobile robots']
# Top keyphrases for 2002.txt:
# ['csp model', 'factored mdps', 'linear value', 'dynamic bayesian networks', 'preference search', 'learning temporal', 'factored markov', 'factored markov decision', 'multiple sequence alignment', 'user interfaces']
# Top keyphrases for 2004.txt:
# ['nondeterministic domains', 'belief revision', 'sketch recognition', 'terrorist', 'perceptually', 'combinatorial auctions', 'self organizing', 'syntactic structure', 'recruitment', 'revision']
# Top keyphrases for 2005.txt:
# ['disambiguation', 'sense disambiguation', 'word sense', 'word sense disambiguation', 'auction protocol', 'boosting semantic', 'semantic web data', 'semantic web', 'reactive', 'multirobot']
# Top keyphrases for 2006.txt:
# ['semantic web', 'human robot interaction', 'robot interaction', 'human robot', 'interventional distributions', 'news framework', 'semi markovian', 'sets logic programs', 'biconnected', 'default logic']
# Top keyphrases for 2007.txt:
# ['semantic web', 'modal logic', 'service composition', 'web service composition', 'equilibria', 'automated semantic', 'composition planning', 'honesty', 'mechanism promoting', 'observatory']
# Top keyphrases for 2008.txt:
# ['voting', 'localization models', 'horn', 'revision', 'sketch recognition', 'activity recognition', 'dimensionality', 'efficient haplotype', 'efficient haplotype inference', 'haplotype inference']
# Top keyphrases for 2010.txt:
# ['label', 'voting', 'world', 'solvers', 'way', 'particular', 'without', 'three', 'various', 'develop']
# Top keyphrases for 2011.txt:
# ['world', 'learn', 'quality', 'significantly', 'real world', 'without', 'matrix', 'trust', 'question', 'even']
# Top keyphrases for 2012.txt:
# ['world', 'real world', 'allows', 'learn', 'current', 'three', 'provides', 'evaluate', 'prior', 'significantly']
# Top keyphrases for 2013.txt:
# ['world', 'real world', 'rank', 'energy', 'particular', 'result', 'significantly', 'costs', 'find', 'make']
# Top keyphrases for 2014.txt:
# ['world', 'quality', 'real world', 'significantly', 'sparse', 'called', 'view', 'target', 'label', 'efficiency']
# Top keyphrases for 2015.txt:
# ['world', 'real world', 'topic', 'sparse', 'significantly', 'learn', 'challenging', 'including', 'current', 'theoretical']
# Top keyphrases for 2016.txt:
# ['deep', 'world', 'real world', 'significantly', 'matrix', 'learn', 'develop', 'dataset', 'extensive', 'particular']
# Top keyphrases for 2017.txt:
# ['deep', 'matrix', 'world', 'real world', 'learn', 'attention', 'label', 'dataset', 'input', 'recently']
# Top keyphrases for 2018.txt:
# ['deep', 'attention', 'dataset', 'world', 'learn', 'neural networks', 'embedding', 'real world', 'convolutional', 'adversarial']
# Top keyphrases for 2019.txt:
# ['deep', 'attention', 'dataset', 'embedding', 'adversarial', 'convolutional', 'neural networks', 'learn', 'world', 'target']
# Top keyphrases for 2020.txt:
# ['deep', 'attention', 'adversarial', 'dataset', 'learn', 'extensive', 'target', 'world', 'neural networks', 'convolutional']
# Top keyphrases for 2021.txt:
# ['deep', 'adversarial', 'attention', 'dataset', 'neural networks', 'extensive', 'world', 'target', 'real world', 'learn']
# Top keyphrases for 2022.txt:
# ['deep', 'transformer', 'dataset', 'adversarial', 'attention', 'extensive', 'trained', 'world', 'github', 'learn']
# Top keyphrases for 2023.txt:
# ['github', 'github com', 'deep', 'transformer', 'extensive', 'adversarial', 'world', 'attention', 'contrastive', 'real world']
