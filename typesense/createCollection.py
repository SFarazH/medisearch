import typesense

client = typesense.Client({
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': 'xyz',
    'connection_timeout_seconds': 2
})

schema = {
    "name": "medicines",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "name", "type": "string"},
        {"name": "price", "type": "float", "optional": True},
        {"name": "manufacturerName", "type": "string", "optional": True},
        {"name": "type", "type": "string", "optional": True},
        {"name": "shortComposition1", "type": "string", "optional": True},
        {"name": "shortComposition2", "type": "string", "optional": True}
    ]
}

try:
    client.collections['medicines'].delete()
except:
    pass

client.collections.create(schema)
print("✅ Collection created.")
