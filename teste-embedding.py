from pathlib import Path

from chunker import criar_chunks
from embeddings import get_embedding


docs = list(Path("arquivos-md").rglob("*.md"))

chunks = criar_chunks(docs[0])

texto = chunks[0]["text"]

embedding = get_embedding(texto)

print(f"Texto: {texto}")
print(f"Tamanho do embedding: {len(embedding)}")
print(f"Primeiros 10 valores: {embedding[:10]}")