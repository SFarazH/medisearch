from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
index_name = "medicines"

def create_index():
    if not es.indices.exists(index=index_name):
        es.indices.create(
            index=index_name,
            body={
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "autocomplete": {
                                "tokenizer": "standard",
                                "filter": ["lowercase", "stop", "asciifolding"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "name": {"type": "text", "analyzer": "autocomplete"},
                        "shortComposition1": {"type": "text", "analyzer": "autocomplete"},
                        "shortComposition2": {"type": "text", "analyzer": "autocomplete"},
                    }
                }
            }
        )
        print(f"Index '{index_name}' created with mappings.")
    else:
        print(f"Index '{index_name}' already exists.")

if __name__ == "__main__":
    create_index()
