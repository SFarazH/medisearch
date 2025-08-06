from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import typesense

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = typesense.Client({
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': 'xyz',
    'connection_timeout_seconds': 2
})

@app.get("/search")
def search_medicines(q: str = Query(..., min_length=1)):
    search_parameters = {
        'q': q,
        'query_by': 'name,short_composition1,short_composition2',
        'sort_by': 'price:asc',
        'num_typos': 2,
        'per_page': 20
    }
    results = client.collections['medicines'].documents.search(search_parameters)
    hits = results.get("hits", [])

    selected_fields = ["name", "manufacturer_name", "short_composition1", "short_composition2"]

    filtered_docs = []
    for item in hits:
        doc = item.get("document", {})
        filtered_doc = {field: doc.get(field) for field in selected_fields}
        filtered_docs.append(filtered_doc)
    print(len(filtered_docs))
    return filtered_docs

