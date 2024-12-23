from opensearchpy import OpenSearch, helpers
import json
import random
import os

# Configuration for connecting to OpenSearch
CA = os.getenv('OPENSEARCH_CA', '~/.opensearch/root.crt')
PASS = os.getenv('OPENSEARCH_PASS')
HOSTS = os.getenv('OPENSEARCH_HOSTS').split(',')

# Create sample test data
sample_products = [
    {
        "name": "Chocolate Chip Cookies",
        "category": "Cookies",
        "description": "Classic homemade cookies with rich chocolate chips",
        "price": 8.99,
        "tags": ["cookies", "chocolate", "classic", "baked"]
    },
    {
        "name": "Caramel Brownies",
        "category": "Brownies",
        "description": "Fudgy chocolate brownies with caramel swirl",
        "price": 10.99,
        "tags": ["brownies", "chocolate", "caramel", "fudgy"]
    },
    {
        "name": "Vanilla Cupcakes",
        "category": "Cupcakes",
        "description": "Light and fluffy vanilla cupcakes with buttercream frosting",
        "price": 6.99,
        "tags": ["cupcakes", "vanilla", "frosting", "dessert"]
    },
    {
        "name": "Strawberry Cheesecake",
        "category": "Cakes",
        "description": "Creamy cheesecake topped with fresh strawberries",
        "price": 12.99,
        "tags": ["cheesecake", "strawberry", "creamy", "cake"]
    },
    {
        "name": "Gummy Bear Candy",
        "category": "Candies",
        "description": "Colorful fruit-flavored gummy bear candies",
        "price": 4.99,
        "tags": ["candy", "gummy", "fruit", "sweet"]
    }
]

# Function to generate additional products
def generate_more_products(base_products, count=100):
    additional_products = []
    adjectives = ["Deluxe", "Gourmet", "Premium", "Homestyle", "Artisanal"]
    brands = ["Sweet Heaven", "Sugar Palace", "Candy Kingdom", "Divine Treats", "Sweet Dreams"]
    
    for _ in range(count):
        base_product = random.choice(base_products)
        new_product = base_product.copy()
        new_product["name"] = f"{random.choice(adjectives)} {base_product['name']} from {random.choice(brands)}"
        new_product["price"] = round(base_product["price"] * random.uniform(0.8, 1.2), 2)
        additional_products.append(new_product)
    
    return additional_products

def create_index(client, index_name):
    """Create index with mapping"""
    mapping = {
        "mappings": {
            "properties": {
                "name": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"},
                        "trigram": {
                            "type": "text",
                            "analyzer": "trigram"
                        }
                    }
                },
                "category": {"type": "keyword"},
                "description": {"type": "text"},
                "price": {"type": "float"},
                "tags": {"type": "keyword"}
            }
        },
        "settings": {
            "analysis": {
                "analyzer": {
                    "trigram": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "shingle"]
                    }
                },
                "filter": {
                    "shingle": {
                        "type": "shingle",
                        "min_shingle_size": 2,
                        "max_shingle_size": 3
                    }
                }
            }
        }
    }
    
    # Delete index if it exists
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
    
    # Create new index
    client.indices.create(index=index_name, body=mapping)

def load_data(client, index_name, products):
    """Load data into index"""
    actions = [
        {
            "_index": index_name,
            "_source": product
        }
        for product in products
    ]
    
    helpers.bulk(client, actions)

def main():
    # Create OpenSearch client

    client = OpenSearch(
        HOSTS,
        http_auth=('admin', PASS),
        use_ssl=True,
        verify_certs=True,
        ca_certs=CA)
    index_name = "products"
    
    try:
        # Create index
        create_index(client, index_name)
        
        # Generate more test data
        all_products = sample_products + generate_more_products(sample_products)
        
        # Load data
        load_data(client, index_name, all_products)
        
        print(f"Successfully loaded {len(all_products)} products into index {index_name}")
        
        # Check document count in index
        count = client.count(index=index_name)
        print(f"Document count in index: {count['count']}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    main() 