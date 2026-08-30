from pathlib import Path

from chunker import criar_chunks
from embeddings import get_embedding


def criar_indice():
    docs = list(Path("arquivos-md").rglob("*.md"))

    if not docs:
        print("Nenhum documento encontrado em arquivos-md.")
        return [], []

    chunks = []

    for doc in docs:
        chunks_do_arquivo = criar_chunks(doc)
        chunks.extend(chunks_do_arquivo)

    embeddings = []

    for i, chunk in enumerate(chunks):
        print(f"Gerando embedding {i + 1}/{len(chunks)}")

        embedding = get_embedding(chunk["text"])
        embeddings.append(embedding)

    return chunks, embeddings