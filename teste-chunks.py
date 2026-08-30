from pathlib import Path
from chunker import criar_chunks


docs = list(Path("arquivos-md").rglob("*.md"))

chunks = criar_chunks(docs[0])

print(f"Arquivo: {docs[0]}")
print(f"Quantidade de chunks: {len(chunks)}")

for chunk in chunks[:5]:
    print("\n" + "=" * 60)
    print(f"Position: {chunk['position']}")
    print(f"Section: {chunk['section']}")
    print(f"Tamanho: {len(chunk['text'])} caracteres")
    print("-" * 60)
    print(chunk["text"])