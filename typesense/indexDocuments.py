import typesense
import json

client = typesense.Client({
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': 'xyz',
    'connection_timeout_seconds': 2
})

count = 0

with open("medicines.json", "r") as f:
    for line in f:
        doc = json.loads(line)
        client.collections['medicines'].documents.upsert(doc)
        count += 1
        if count % 1000 == 0:
            print(f"{count} documents inserted...")

print("✅ Documents indexed.")
