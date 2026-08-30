from retriever import carregar_indice, buscar
from embeddings import get_embedding


indice = carregar_indice()

pergunta = "How do I configure SSL certificates?"

resultados = buscar(
    pergunta,
    indice,
    get_embedding,
    top_k=5
)

print("\n--- RESULTADOS ---")

for i, resultado in enumerate(resultados, start=1):
    chunk = resultado["chunk"]

    print(f"\nResultado #{i}")
    print(f"Score: {resultado['score']:.4f}")
    print(f"Arquivo: {chunk['source']}")
    print(f"Seção: {chunk['section']}")
    print(f"Texto: {chunk['text'][:300]}")