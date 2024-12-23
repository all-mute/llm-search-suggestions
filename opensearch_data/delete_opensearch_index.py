from opensearchpy import OpenSearch
import os

# OpenSearch connection configuration
CA = os.getenv('OPENSEARCH_CA', '~/.opensearch/root.crt')
PASS = os.getenv('OPENSEARCH_PASS')
HOSTS = os.getenv('OPENSEARCH_HOSTS').split(',')

def delete_index():
    # Create OpenSearch client
    client = OpenSearch(
        HOSTS,
        http_auth=('admin', PASS),
        use_ssl=True,
        verify_certs=True,
        ca_certs=CA or None
    )
    
    index_name = "products"
    
    try:
        # Check if index exists
        if client.indices.exists(index=index_name):
            # Delete the index
            client.indices.delete(index=index_name)
            print(f"Index {index_name} successfully deleted.")
        else:
            print(f"Index {index_name} does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting the index: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    delete_index() 