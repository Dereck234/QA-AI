from pathlib import Path
from chunker import criar_chunks


docs = list(Path("arquivos-md").rglob("*.md"))

chunks = criar_chunks(docs[0])

print(f"Arquivo: {docs[0]}")
print(f"Quantidade de chunks: {len(chunks)}")

for chunk in chunks[:10]:
    print("\n--- CHUNK ---")
    print(f"Position: {chunk['position']}")
    print(f"Section: {chunk['section']}")
    print(f"Text: {chunk['text'][:150]}")