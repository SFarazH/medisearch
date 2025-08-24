import json
from elasticsearch import Elasticsearch, helpers

ES_HOST = "http://localhost:9200"
INDEX_NAME = "medicines"
FILE_PATH = "medicines.json" 
BATCH_SIZE = 10000

es = Elasticsearch([ES_HOST])

def generate_actions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                doc = json.loads(line)
                yield {
                    "_index": INDEX_NAME,
                    "_source": doc
                }
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {e}")
                continue

def bulk_upload():
    success, failed = 0, 0
    batch = []
    for i, action in enumerate(generate_actions(FILE_PATH), 1):
        batch.append(action)
        if i % BATCH_SIZE == 0:
            resp = helpers.bulk(es, batch, raise_on_error=False)
            success += resp[0]
            failed += len(resp[1])
            print(f"Uploaded {i} docs (success: {success}, failed: {failed})")
            batch = []
    if batch:
        resp = helpers.bulk(es, batch, raise_on_error=False)
        success += resp[0]
        failed += len(resp[1])
        print(f"Uploaded final batch (success: {success}, failed: {failed})")

    print(f"✅ Finished. Total Success: {success}, Failed: {failed}")

if __name__ == "__main__":
    bulk_upload()
