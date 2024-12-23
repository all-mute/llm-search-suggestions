from opensearchpy import OpenSearch

import os

CA = os.getenv('OPENSEARCH_CA', '~/.opensearch/root.crt')
PASS = os.getenv('OPENSEARCH_PASS')
HOSTS = os.getenv('OPENSEARCH_HOSTS').split(',')

class SearchService:
    def __init__(self):
        self.client = OpenSearch(
            HOSTS,
            http_auth=('admin', PASS),
            use_ssl=True,
            verify_certs=True,
            ca_certs=CA or None
        )
        self.index = "products"
        self.k = 5  # Minimum number of hints

    def get_search_hints(self, query):
        response = self.client.search(
            index=self.index,
            body={
                "size": self.k,
                "query": {
                    "match": {
                        "name": query
                    }
                },
                "suggest": {
                    "text": query,
                    "simple_phrase": {
                        "phrase": {
                            "field": "name.trigram",
                            "size": 5,
                            "gram_size": 3
                        }
                    }
                }
            }
        )
        hints = [hit['_source']['name'] for hit in response['hits']['hits']]
        return hints