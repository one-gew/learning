import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from main import search_chunks


BASE_DIR = Path(__file__).resolve().parent
CHUNKS_PATH = BASE_DIR / "output" / "chunks.json"
app = FastAPI(title="知识库检索练习")


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=3, ge=1, le=10)


@app.post("/search")
def search(request: SearchRequest) -> dict:
    try:
        chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise HTTPException(
            status_code=503,
            detail="无法读取分块文件，请先运行 main.py，生成 output/chunks.json。",
        ) from error

    results = search_chunks(request.query, chunks, top_k=request.top_k)
    return {
        "query": request.query,
        "count": len(results),
        "results": results,
    }
