import arxiv
import json
from datetime import datetime
import os
from pathlib import Path


class ArxivClient:
    def __init__(self, max_results=100):
        self.client = arxiv.Client()
        self.max_results = max_results

    def search(self, query="all", categories=None):
        search_query = query

        search = arxiv.Search(
            query=search_query,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )

        papers = []

        for result in self.client.results(search):
            papers.append(
                {
                    "id": result.get_short_id(),
                    "arxiv_id": result.entry_id,
                    "title": result.title,
                    "abstract": result.summary,
                    "author": [str(author) for author in result.authors],
                    "published": result.published.isoformat(),
                    "categories": result.categories,
                    "pdf_url": result.pdf_url,
                }
            )
        return papers

    def save_papers(self, papers, filename=None):
        if filename is None:
            filename = f"arXiv_{datetime.now().strftime('%Y%m%d')}.json"
            data = "data"
        filepath = f"{Path.cwd()}/data/{filename}"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(papers, f, indent="2")

        return filepath

    def load_json(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)


arv = ArxivClient(max_results=10)

papers = arv.search()

filepath = arv.save_papers(papers)
print(filepath)
data = arv.load_json(filepath)
