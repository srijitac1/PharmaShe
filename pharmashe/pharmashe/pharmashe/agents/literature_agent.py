from Bio import Entrez

Entrez.email = "your_email@example.com"

def fetch_pubmed(query, max_results=5):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    ids = record["IdList"]

    papers = []
    if not ids:
        return papers

    handle = Entrez.efetch(db="pubmed", id=",".join(ids), rettype="abstract", retmode="text")
    abstracts = handle.read().split("\n\n")

    for abs_text in abstracts:
        if abs_text.strip():
            papers.append({"source": "PubMed", "text": abs_text.strip()})

    return papers
