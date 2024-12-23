# AI-enhanced e-commerce search system

## Project Description

This project is an enhanced e-commerce search system that combines traditional search with AI-powered suggestions. It uses OpenSearch for basic search functionality and integrates with LLM services for intelligent search suggestions.

### Features
- Traditional product search using OpenSearch
- AI-enhanced search suggestions
- User-friendly web interface built with Streamlit
- easter egg for Chocolate Chip Cookies

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file with the following variables:
```bash
OPENSEARCH_HOSTS=https://localhost:9200
OPENSEARCH_PASS=admin
OPENSEARCH_CA=path/to/your/ca.pem # optional, if using OpenSearch in cloud
OPENAI_API_KEY=your_api_key
BASE_URL=your_llm_service_url # optional, if not using OpenAI
```

3. Run OpenSearch using Docker Compose:
```bash
docker compose up -d
```

4. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate # for Linux/Mac
or
.venv\Scripts\activate # for Windows
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Load sample data:
```bash
python opensearch_data/load_sample_data.py
```

7. Run the Streamlit application:
```bash
streamlit run app/main.py
```

8. Open your browser and navigate to: `http://localhost:8501`

## Project Structure

- `app/` - main application code
  - `main.py` - Streamlit application
  - `search.py` - OpenSearch search service
  - `llm_service.py` - LLM service for AI-powered suggestions
- `opensearch_data/` - scripts for working with data
  - `load_sample_data.py` - loading sample data
  - `delete_opensearch_index.py` - deleting the index
  - `test_opensearch_query.py` - testing queries

## Additional Commands

- `opensearch_data/load_sample_data.py` - loading sample data
- `opensearch_data/delete_opensearch_index.py` - deleting the index
- `opensearch_data/test_opensearch_query.py` - testing queries



