import json

from indexer import criar_indice


chunks, embeddings = criar_indice()

indice = []

for chunk, embedding in zip(chunks, embeddings):
    indice.append({
        "chunk": chunk,
        "embedding": embedding
    })


with open("indice.json", "w", encoding="utf-8") as arquivo:
    json.dump(indice, arquivo, ensure_ascii=False)

print()
print(f"Índice criado com {len(indice)} chunks.")