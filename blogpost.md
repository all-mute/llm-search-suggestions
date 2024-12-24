## Introduction

In the world of e-commerce, where competition is growing every day, every detail on a website plays a crucial role in attracting and retaining customers. One such element is the search system. Effective search suggestions not only enhance user experience but also significantly impact conversion rates, turning visitors into buyers.

## Problem Statement
Imagine a situation where a user visits your online store with a specific request, such as "I want something sweet" or "I want to order something for my tea time." However, the standard search system returns a limited number of results or provides no suggestions at all. Traditional search methods often struggle to provide relevant and diverse offerings, negatively affecting conversion metrics.

![demo no search results](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/idj1ze7wnefmnwsxe9sx.png)

# Solution with LLM

[live demo](https://llm-search-suggestions-demo.streamlit.app/)

This is where large language model (LLM) technology, such as GPT, comes to the rescue. We can ask the model to **suggest** user **search queries**, to show at least something in scenarios where we have zero or not enough results from traditional search.

## System Architecture
Let's build a simple system with Streamlit, OpenSearch, and LLM.

Our system combines traditional search based on OpenSearch with LLM capabilities to create intelligent search suggestions. The main components of the architecture include:
- **User Interface**: Developed using Streamlit, it provides a convenient platform for user interaction.
- **Search Service (OpenSearch)**: Utilizes OpenSearch to perform basic search queries.
- **LLM Service**: Generates additional suggestions if traditional search does not provide enough results.

I created a simple OpenSearch index with fake sweets. I will use them for queries:
```python
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
```

The algorithm is simple:
1. User enters a query in the UI.
2. The system performs a traditional search using OpenSearch.
3. If the search returns fewer than 5 results, the system queries the LLM.
4. The LLM generates additional suggestions.
5. The system displays all results to the user.

With this approach, we can be sure that the user will be left with suggestions way more often than with traditional search.

## Example Implementation
(Source link at the end of the post) Let’s consider an example of integrating LLM to enhance search suggestions. Suppose a user enters the query "I want something sweet." If traditional search returns fewer than 5 suggestions, the system queries the LLM, which generates additional proposals:

**Prompt for LLM**:
```python
response = self.client.chat.completions.create(
            model="gpt-4o-mini", # or "llama-lite/latest"
            messages=[{
                "role": "user", 
                "content": f"You are a helpful assistant that helps users find products in an e-commerce store. Generate 5 relevant product suggestions for '{query}'. Return only a JSON array of strings with product names."
            }],
            temperature=0.7,
            max_tokens=100,
        )
```
**Model Response**:
```python
['Chocolate Chip Cookies', 'Assorted Gourmet Candy Box', 'Vanilla Cupcake Mix', 'Chocolate Brownie Bites', 'Caramel Sea Salt Chocolate Bars']
```
These suggestions are then displayed to the user alongside the results from traditional search, creating a more comprehensive and satisfying offering.

![opensearch vs llm suggestions](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/wq6dh4h121vlqh20p5vv.png)

And when the customer clicks on a suggestion, they will get what they possibly need!
![customer success](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/z0vqhb2n20mpfp7qmcfe.png)

# Further Enhancements and Optimizations
The implementation of LLM for search suggestions may lead to a 1-10% increase in finding relevant products by users. However, LLM may not be cheap for that task, so I recommend a few optimizations:
- Caching LLM Queries
- Randomizing LLM suggestions
- Collecting LLM suggestions, indexing them, and implementing a retrieval system to decrease cost
- Using small language models
- Adjusting Generation Temperature sometimes
- Visual Highlighting of LLM Suggestions
- Considering cases when LLM can't suggest anything or can't respond because of ethics
- Considering cases when LLM may suggest something that is not in the store
- Collecting human feedback to improve the system later

![interesting usage](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/x2h3m0wghdw4ana5hwny.png)

* [live demo](https://llm-search-suggestions-demo.streamlit.app/)
* [source code](https://github.com/all-mute/llm-search-suggestions)
* [my tg blog](https://t.me/ai_spaceships)