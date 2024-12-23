from opensearchpy import OpenSearch

# OpenSearch connection configuration
import os

CA = os.getenv('OPENSEARCH_CA', '~/.opensearch/root.crt')
PASS = os.getenv('OPENSEARCH_PASS')
HOSTS = os.getenv('OPENSEARCH_HOSTS').split(',')

def test_query(query):
    # Create OpenSearch client
    client = OpenSearch(
        HOSTS,
        http_auth=('admin', PASS),
        use_ssl=True,
        verify_certs=True,
        ca_certs=CA or None
    )
    
    index_name = "products"
    query = {
        "query": {
            "match": {
                "name": query
            }
        }
    }
    
    try:
        # Execute query
        response = client.search(index=index_name, body=query)
        print("Query results:")
        for hit in response['hits']['hits']:
            print(hit['_source'])
    except Exception as e:
        print(f"An error occurred while executing the query: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    test_query("I want to order something for my tea time") 
    #test_query("Chocolate Chip Cookies")