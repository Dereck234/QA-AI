import json
import urllib.request


def get_embedding(text):
    url = "http://localhost:11434/api/embed"

    data = {
        "model": "nomic-embed-text",
        "input": text,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["embeddings"][0]


def cosine_similarity(a, b):
    dot_product = 0

    for i in range(len(a)):
        dot_product += a[i] * b[i]

    magnitude_a = 0

    for value in a:
        magnitude_a += value * value

    magnitude_b = 0

    for value in b:
        magnitude_b += value * value

    magnitude_a = magnitude_a ** 0.5
    magnitude_b = magnitude_b ** 0.5

    return dot_product / (magnitude_a * magnitude_b)


question = "What is Python?"

question_embedding = get_embedding(question)


with open("documents/networking.txt", "r", encoding="utf-8") as file:
    document = file.read()


chunks = document.split("\n\n")


# Generate an embedding for every chunk.
chunk_embeddings = []

for i, chunk in enumerate(chunks):
    embedding = get_embedding(chunk)

    chunk_embeddings.append(embedding)

    print(f"Chunk {i}: {len(embedding)} dimensions")


# Compare the question against every chunk.
results = []

for i, chunk_embedding in enumerate(chunk_embeddings):
    score = cosine_similarity(
        question_embedding,
        chunk_embedding,
    )

    results.append((score, i))


print()
print("--- SIMILARITY SCORES ---")

for score, i in results:
    print(f"Chunk {i}: {score}")


# Sort from highest similarity to lowest.
results.sort(reverse=True)

print()
print("--- RANKED RESULTS ---")

for score, i in results:
    print(f"Chunk {i}: {score}")

top_k = 3

retrieved_chunks = []

for score, i in results[:top_k]:
    retrieved_chunks.append(chunks[i])


context = "\n\n".join(retrieved_chunks)


print()
print("--- RETRIEVED CONTEXT ---")
print(context)

prompt = f"""
Answer the question using only the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

print()
print("--- PROMPT ---")
print(prompt)

def generate_answer(prompt):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen3:8b",
        "prompt": prompt,
        "stream": False,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["response"]

answer = generate_answer(prompt)

print()
print("--- ANSWER ---")
print(answer)