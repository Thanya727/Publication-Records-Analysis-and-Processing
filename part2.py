import os
import xml.etree.ElementTree as ET
import whoosh.index as index
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.qparser import QueryParser

XML_FILE_PATH = "./dblp/dblp.xml"


def create_index():
    # Define the schema for your index
    schema = Schema(
        title=TEXT(stored=True),
        author=TEXT(stored=True),
        venue=TEXT(stored=True),
        year=DATETIME(stored=True),
        url=TEXT(stored=True),
        pdf_url=TEXT(stored=True),
    )

    # Create or open an index
    if not os.path.exists("index"):
        os.mkdir("index")
    return index.create_in("index", schema)


def parse_dblp():
    with open(XML_FILE_PATH, "r", encoding="ISO-8859-1") as file:
        xml_content = file.read()

    return ET.fromstring(xml_content)


def write_docs(ix, root):
    writer = ix.writer()
    for publication in root:
        title = publication.find("title").text
        authors = publication.text.split('\n')[0]
        venue = publication.text.split('\n')[1]
        year = publication.find("year").text
        urls = publication.text.split('\n')[2]
        url = urls.split(' ')[1]
        pdf_url = urls.split(' ')[2]

        writer.add_document(title=title, author=authors,
                            venue=venue, year=year, url=url, pdf_url=pdf_url)
    writer.commit()


def search(ix, query_str):
    with ix.searcher() as searcher:
        query = QueryParser("author", ix.schema).parse(query_str)
        return searcher.search(query)


def main():
    # Perform a search
    results = search(ix, "author:Paul Kocher")
    for result in results:
        print(f"Title: {result['title']}, Author: {result['author']}, Venue: {result['venue']}, Year: {result['year']}, URL: {result['url']}, PDF URL: {result['pdf_url']}")


ix = create_index()
# Parse the XML file
# tree = ET.parse(r"D:\dblp.xml")
root = parse_dblp()

# Index the data from the XML
write_docs(ix, root)

if __name__ == "__main__":
    main()
