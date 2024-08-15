from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

# Define the URLs to scrape
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


# Function to load multiple URLs
def load_multiple_urls(urls):
    docs = []
    for url in urls:
        # Set custom headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }

        # Initialize the RecursiveUrlLoader with the specified headers
        loader = RecursiveUrlLoader(
            url=url,
            max_depth=20,  # Adjust the depth as needed
            extractor=lambda x: Soup(x, "html.parser").text,
            headers=headers,
            check_response_status=True,  # Check response status to skip bad requests
            continue_on_failure=True  # Continue loading even if some requests fail
        )

        # Load documents and extend the docs list
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