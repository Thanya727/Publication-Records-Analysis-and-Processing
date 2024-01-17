#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[2]:


def extract_titles(xml_file):
    titles = []
    with open(xml_file, 'r', encoding='ISO-8859-1') as f:
        xml_content = f.read()

    # Replace undefined entities with corresponding characters
    xml_content = xml_content.replace("&Ouml;", "Ö")

    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for element in root:
        if element.tag in ["article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis"]:
            title = element.find("title").text
            titles.append(title)
    return titles

def vectorize_titles(titles):
    vectorizer = TfidfVectorizer()
    title_vectors = vectorizer.fit_transform(titles)
    return title_vectors, vectorizer

def find_similar_papers(input_title, titles, title_vectors, vectorizer):
    input_vector = vectorizer.transform([input_title])
    similarities = cosine_similarity(input_vector, title_vectors)
    similar_paper_indices = similarities.argsort()[0][::-1]
    return [(titles[i], similarities[0][i]) for i in similar_paper_indices if i != 0]

def main():
    xml_file = "dblp.xml"  # Provide the path to your DBLP XML file
    titles = extract_titles(xml_file)
    title_vectors, vectorizer = vectorize_titles(titles)

    while True:
        input_title = input("Enter a research paper title: ")
        if input_title.lower() == "exit":
            break

        similar_papers = find_similar_papers(input_title, titles, title_vectors, vectorizer)

        if not similar_papers:
            print("No similar papers found.")
        else:
            print("Similar Papers:")
            for paper, similarity in similar_papers:
                print(f"Title: {paper} (Similarity: {similarity:.2f})")

if __name__ == "__main__":
    main()

