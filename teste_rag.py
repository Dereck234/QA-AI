from retriever import carregar_indice, buscar
from embeddings import get_embedding
from generator import gerar_resposta


indice = carregar_indice()

pergunta = "How do I make asynchronous HTTP requests?"

resultados = buscar(
    pergunta,
    indice,
    get_embedding,
    top_k=3
)

if not resultados:
    print("\n--- RESPOSTA ---")
    print("Não encontrei essa informação na documentação fornecida.")
    exit()

resposta = gerar_resposta(
    pergunta,
    resultados
)

print("\n--- RESPOSTA ---")
print(resposta)

print("\n--- FONTES ---")

for resultado in resultados:
    chunk = resultado["chunk"]

    print(
        f"Score: {resultado['score']:.4f} | "
        f"{chunk['source']} → {chunk['section']}"
    )