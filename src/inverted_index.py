# Create inverted indexing from the tokinized text of arXiv_XXXX.json
# Simple first sketch implementation

# term1 -> [1][3][7]

from typing import Counter
from tokenizer import Tokenizer
from collections import defaultdict, Counter

from arxiv_client import ArxivClient


class inverted_index:
    def __init__(self):
        self.tokinizer = Tokenizer()
        # Using default dict for dynamique assigning
        self.inverted_index = defaultdict(dict)
        self.papers = {}
        self.next_id = 0

    def inverted_indexer(self, paper):
        paper_id = self.next_id
        self.papers[paper_id] = {
            "title": paper["title"],
            "abstrat": paper["abstract"],
            "authors": paper["authors"],
            "arxiv_id": paper["arxiv_id"],
            "pdf_url": paper["pdf_url"],
        }
        title_tokens = self.tokinizer.tokenize(paper["title"])
        summary_tokens = self.tokinizer.tokenize(paper["abstract"])

        frq = 1
        for title_token in title_tokens:
            if paper_id in self.inverted_index[title_token]:
                self.inverted_index[title_token][paper_id]["frequency"] += 1
                # the token is already in the inverted index  but the paper_id doesnt exist
                print(
                    f"Tryin to add the token '{title_token}' to the paper_id : <{paper_id}>, that already exist "
                )
            else:
                paper_info = {"frequency": frq}
                self.inverted_index[title_token][paper_id] = {"frequency": 1}
                print(f"added  the token :'{title_token}' to paper id : <{paper_id}> ")
        self.next_id += 1
        return self.inverted_index


inv = inverted_index()

arXiv = ArxivClient(max_results=4)
docs = arXiv.search("IA")
filepath = arXiv.save_papers(docs)
papers = arXiv.load_json(filepath)
# print(paper[0]["title"])
for paper in papers:
    inverted_index = inv.inverted_indexer(paper)

for key, value in inverted_index.items():
    print(f"{key}:{value}\n")
