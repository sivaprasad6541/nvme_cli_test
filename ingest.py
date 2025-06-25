# ingest.py
import os
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

source_dir = "nvme-cli"
chunk_size = 40

# Init Chroma
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("nvme_cli_code")

# Step 1: Collect all .c/.h files first
all_code_files = []
for root, _, files in os.walk(source_dir):
    for file in files:
        if file.endswith((".c", ".h")):
            all_code_files.append(os.path.join(root, file))

total_files = len(all_code_files)
print(f"Found {total_files} code files to process.\n")

# Step 2: Chunk & ingest with progress
for idx, file_path in enumerate(all_code_files, start=1):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        continue

    chunks = [
        {
            "text": "".join(lines[i:i + chunk_size]),
            "metadata": {
                "file": file_path.replace("\\", "/"),
                "start_line": i + 1
            }
        }
        for i in range(0, len(lines), chunk_size)
    ]

    for chunk in chunks:
        doc_id = f"{chunk['metadata']['file']}:{chunk['metadata']['start_line']}"
        collection.add(
            documents=[chunk["text"]],
            metadatas=[chunk["metadata"]],
            ids=[doc_id]
        )

    percent = round((idx / total_files) * 100)
    print(f"[{percent:>3}%] Indexed: {file_path}")

print("\n✅ Code ingestion complete.")
