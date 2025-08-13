# 💊 Medisearch : Typesense Medicines Search

This project is a lightweight, high-performance, fast full-text search engine for medicines using [Typesense](https://typesense.org/). It provides fast and typo-tolerant search capabilities over a dataset of medicines, with support for pagination and easy indexing via JSON files.

## Tech Stack

**FastAPI** – Python web framework for the API

**Typesense** – In-memory search engine

**Uvicorn** – ASGI server to run the app

## Features

- Full-text search on medicine names and compositions
- Ultra-fast, typo-tolerant fuzzy search using Typesense
- Sample data indexing with JSON
- Pagination support for large datasets

## Installation

1. **Clone the repository**

```
  git clone https://github.com/SFarazH/medisearch
  cd medisearch
```

2. **Install dependencies**

```
pip install -r requirements.txt
```

3. **Start Typesense Server**
   (Using docker)

```
docker run -p 8108:8108 -v/tmp/typesense-data:/data typesense/typesense:0.25.1 \
  --data-dir /data --api-key=xyz --enable-cors
```

4. **Create Collection & Index Documents**

I have added sample data. You can index your own dataset. Ensure to match naming convention

```
python createCollection.py
python indexDocuments.py
```

5. **Start Server**

```
uvicorn main:app --reload
```

Access results at :

```
http://localhost:5000/search?q=paracetamol&page=1
```

**Response:**

```
[
    {
        "name": "Anglopar 500mg Tablet",
        "manufacturerName": "Anglo-French Drugs & Industries Ltd",
        "shortComposition1": "Paracetamol (500mg)",
        "shortComposition2": ""
    },
    {
        "name": "Acuflam SP 100 mg/500 mg/15 mg Tablet",
        "manufacturerName": "Alkem Laboratories Ltd",
        "shortComposition1": "Aceclofenac (100mg) ",
        "shortComposition2": " Paracetamol (500mg) "
    }
]
```

## 📎 Notes

Your data is indexed in-memory by Typesense. If you restart the Typesense server, you’ll need to re-run the indexing script (unless using persistent volumes in Docker).

For production, mount a permanent volume or use Typesense Cloud.

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://faraz-three.vercel.app)
