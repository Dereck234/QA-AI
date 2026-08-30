import json
import math


def carregar_indice():
    with open("indice.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def cosine_similarity(vetor_a, vetor_b):
    produto = sum(a * b for a, b in zip(vetor_a, vetor_b))

    tamanho_a = math.sqrt(sum(a * a for a in vetor_a))
    tamanho_b = math.sqrt(sum(b * b for b in vetor_b))

    return produto / (tamanho_a * tamanho_b)


def buscar(pergunta, indice, get_embedding, top_k=3, threshold=0.60):
    if top_k <= 0:
        raise ValueError("top_k deve ser maior que zero.")

    pergunta_embedding = get_embedding(pergunta)

    resultados = []

    for item in indice:
        score = cosine_similarity(
            pergunta_embedding,
            item["embedding"]
        )

        resultados.append({
            "score": score,
            "chunk": item["chunk"]
        })

    resultados.sort(
        key=lambda resultado: resultado["score"],
        reverse=True
    )

    resultados = [
        resultado
        for resultado in resultados
        if resultado["score"] >= threshold
    ]

    return resultados[:top_k]