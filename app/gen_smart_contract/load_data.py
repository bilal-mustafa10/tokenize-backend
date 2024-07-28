from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

urls = [
    "https://docs.soliditylang.org/en/v0.8.26/introduction-to-smart-contracts.html#blockchain-basics",
    "https://docs.soliditylang.org/en/v0.8.26/solidity-by-example.html",
    "https://docs.soliditylang.org/en/v0.8.26/layout-of-source-files.html",
    "https://docs.soliditylang.org/en/v0.8.26/structure-of-a-contract.html",
    "https://docs.soliditylang.org/en/v0.8.26/contracts.html",
    "https://docs.soliditylang.org/en/v0.8.26/security-considerations.html",
    "https://docs.soliditylang.org/en/v0.8.26/style-guide.html",
    "https://docs.soliditylang.org/en/v0.8.26/common-patterns.html"
]


def load_multiple_urls(urls):
    docs = []
    for url in urls:
        loader = RecursiveUrlLoader(
            url=url, max_depth=20, extractor=lambda x: Soup(x, "html.parser").text
        )
        docs.extend(loader.load())
    return docs


# Load documents from all URLs
docs = load_multiple_urls(urls)

# Sort the list based on the URLs and get the text
d_sorted = sorted(docs, key=lambda x: x.metadata["source"])
d_reversed = list(reversed(d_sorted))
concatenated_content = "\n\n\n --- \n\n\n".join(
    [doc.page_content for doc in d_reversed]
)