from fastapi import FastAPI
from gif_search_api.src.api.gif_search_init import index, retriever
from gif_search_api.src.models.gif_search_model import SearchQueryInput, SearchQueryOutput
from gif_search_api.src.utils.async_utils import async_retry

app = FastAPI(
    title="GIF search",
    description="Endpoints for a GIF search",
)


@async_retry(max_retries=10, delay=1)
async def gif_search(query):
    # Generate embeddings for the query
    xq = retriever.encode(query).tolist()
    # Compute cosine similarity between query and embeddings vectors and gif description
    xc = index.query(vector=xq, top_k=10, include_metadata=True)
    result = []
    for context in xc['matches']:
        url = context['metadata']['url']
        result.append(url)
    return await result


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/gif-search")
async def query_hospital_agent(query: SearchQueryInput) -> SearchQueryOutput:
    query_response = await gif_search(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response
