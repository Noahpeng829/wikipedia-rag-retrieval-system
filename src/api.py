from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.retriever import WikiRetriever

app = FastAPI(title="Wikipedia RAG Retrieval API")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

retriever = WikiRetriever()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/search")
def search(req: QueryRequest):
    result_df = retriever.retrieve(req.query, top_k=req.top_k)

    results = []

    for _, row in result_df.iterrows():
        results.append({
            "title": row["title"],
            "section": row["section"],
            "chunk_id": int(row["chunk_id"]),
            "chunk_text": row["chunk_text"],
            "dense_score": float(row["dense_score"]),
            "keyword_score": float(row["keyword_score"]),
            "final_score": float(row["final_score"])
        })

    return {
        "query": req.query,
        "top_k": req.top_k,
        "results": results
    }