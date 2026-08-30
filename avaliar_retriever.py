from retriever import carregar_indice, buscar
from embeddings import get_embedding


indice = carregar_indice()


perguntas = [
    "How do I make asynchronous HTTP requests?",
    "How do I set a timeout in HTTPX?",
    "How do I use HTTP/2?",
    "How can I authenticate a request?",
    "How do I configure SSL certificates?",
]


for pergunta in perguntas:

    print("\n" + "=" * 70)
    print(f"PERGUNTA: {pergunta}")
    print("=" * 70)

    resultados = buscar(
        pergunta,
        indice,
        get_embedding,
        top_k=3
    )

    for i, resultado in enumerate(resultados, start=1):

        chunk = resultado["chunk"]

        print(f"\nResultado #{i}")
        print(f"Score: {resultado['score']:.4f}")
        print(f"Arquivo: {chunk['source']}")
        print(f"Seção: {chunk['section']}")
        print(f"Texto: {chunk['text'][:250]}...")