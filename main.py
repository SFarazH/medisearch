from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import typesense
from elasticsearch import Elasticsearch
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Typesense client ---
ts_client = typesense.Client({
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': 'xyz',
    'connection_timeout_seconds': 2
})

# --- Elasticsearch client ---
es_client = Elasticsearch(
    hosts=["http://localhost:9200"], 
)


@app.get("/search/typesense")
def search_typesense(q: str = Query(..., min_length=1), page: int = 1):
    start_time = time.perf_counter()
    search_parameters = {
        'q': q,
        'query_by': 'name,shortComposition1,shortComposition2',
        'sort_by': 'price:asc',
        'num_typos': 2,
        'per_page': 250,
        'page': page
    }
    results = ts_client.collections['medicines'].documents.search(search_parameters)
    hits = results.get("hits", [])

    selected_fields = ["name", "manufacturerName", "shortComposition1", "shortComposition2"]

    filtered_docs = []
    for item in hits:
        doc = item.get("document", {})
        filtered_doc = {field: doc.get(field) for field in selected_fields}
        filtered_docs.append(filtered_doc)
    end_time = time.perf_counter()
    time_taken_ms = (end_time - start_time) * 1000
    return {"time_taken_sec": time_taken_ms,"count": len(filtered_docs), "results": filtered_docs}


@app.get("/search/elasticsearch")
def search_elasticsearch(q: str = Query(..., min_length=1), page: int = 1):
    start_time = time.perf_counter()
    size = 20
    from_ = (page - 1) * size

    body = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["name", "shortComposition1", "shortComposition2"]
            }
        },
        "sort": [
            {"price": {"order": "asc"}}
        ],
        "from": from_,
        "size": 250
    }

    results = es_client.search(index="medicines", body=body)
    hits = results.get("hits", {}).get("hits", [])

    selected_fields = ["name", "manufacturerName", "shortComposition1", "shortComposition2"]

    filtered_docs = []
    for item in hits:
        doc = item.get("_source", {})
        filtered_doc = {field: doc.get(field) for field in selected_fields}
        filtered_docs.append(filtered_doc)
    end_time = time.perf_counter()
    time_taken_ms = (end_time - start_time) * 1000
    return {"time_taken_sec": time_taken_ms,"count": len(filtered_docs), "results": filtered_docs}
