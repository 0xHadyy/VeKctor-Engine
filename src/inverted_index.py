from src.tokenizer import Tokenizer
from collections import defaultdict


class invertedIndex:
    def __init__(self):
        self.tokenizer = Tokenizer()
        # Using default dict for dynamique assigning
        self.inverted_index = defaultdict(dict)
        self.papers = {}
        self.next_id = 0
        self.docIDs_list = []

    def get_posting_list(self, term):
        return self.inverted_index[term]

    def get_docIDs(self):
        return self.docIDs_list

    def inverted_indexer(self, paper: dict) -> dict:
        paper_id = self.next_id
        self.papers[paper_id] = {
            "id": paper["id"],
            "title": paper["title"],
            "abstract": paper["abstract"],
            "length": len(paper["title"]) + len(paper["abstract"]),
        }
        title_tokens = self.tokenizer.tokenize(paper["title"])
        summary_tokens = self.tokenizer.tokenize(paper["abstract"])
        # count the tokens

        token_count = defaultdict(lambda: {"title": 0, "abstract": 0})

        for token in title_tokens:
            token_count[token]["title"] += 1

        for token in summary_tokens:
            token_count[token]["abstract"] += 1

        for token, count in token_count.items():
            # creating new entry
            self.inverted_index[token][paper_id] = {
                "title_count": count["title"],
                "abstract_count": count["abstract"],
                "total_freq": count["title"] + count["abstract"],
            }

        self.docIDs_list.append(self.next_id)
        self.next_id += 1
        return self.inverted_index
