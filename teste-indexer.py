from indexer import criar_indice


chunks, embeddings = criar_indice()

print()
print(f"Total de chunks: {len(chunks)}")
print(f"Total de embeddings: {len(embeddings)}")
print(f"Tamanho do primeiro embedding: {len(embeddings[0])}")