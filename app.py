from src.arxiv_client import ArxivClient
from src.inverted_index import invertedIndex
from src.boolean_retrieval import booleanRetrieval


class VeKctorEngine:
    def __init__(self):
        self.arxiv = ArxivClient(max_results=40)
        self.inverted_index = invertedIndex()
        self.boolean_ret = booleanRetrieval(self.inverted_index)

        self.indexed_papers = None

        self.engine_pipeline()

    def engine_pipeline(self):
        # Retreving Papers using API
        papers = self.arxiv.search("IA")
        papers_path = self.arxiv.save_papers(papers)

        loaded_papers = self.arxiv.load_json(papers_path)

        # invert indexing (title + abstract)
        for paper in loaded_papers:
            self.indexed_papers = self.inverted_index.inverted_indexer(paper)

        if self.indexed_papers is not None:
            for key, value in self.indexed_papers.items():
                pass
                print(f"{key}->{value}\n")

        # boolean Search
        result = self.boolean_ret.boolean_search("NOT Deep OR NOT IA")
        print(result)


if __name__ == "__main__":
    print("Search Engine is Starting...")
    VeKctorEngine()
