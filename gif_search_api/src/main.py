from fastapi import FastAPI
from api.gif_search_init import index, retriever
from models.gif_search_model import SearchQueryInput, SearchQueryOutput

app = FastAPI(
    title="GIF search",
    description="Endpoints for a GIF search",
)


def gif_search(query):
    # Generate embeddings for the query
    xq = retriever.encode(query).tolist()
    # Compute cosine similarity between query and embeddings vectors and gif description
    xc = index.query(vector=xq, top_k=10, include_metadata=True)
    result = []
    for context in xc['matches']:
        url = context['metadata']['url']
        result.append(url)
    return result


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/gif-search")
async def query_search_agent(query: SearchQueryInput) -> SearchQueryOutput:
    urls = gif_search(query.text)
    external_data = {
        "input": query.text,
        "output": [url for url in urls],
    }
    query_response = SearchQueryOutput(**external_data)

    return query_response
