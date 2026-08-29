import json
import urllib.request


def generate_embedding(text):
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
    magnitude_b = 0

    for value in a:
        magnitude_a += value * value

    for value in b:
        magnitude_b += value * value

    magnitude_a = magnitude_a ** 0.5
    magnitude_b = magnitude_b ** 0.5

    return dot_product / (magnitude_a * magnitude_b)


texts = [
    "UDP is useful for low latency applications.",
    "UDP is useful when minimizing communication delay.",
    "Python is a programming language.",
]

embeddings = []

for text in texts:
    embedding = generate_embedding(text)
    embeddings.append(embedding)

for i, embedding in enumerate(embeddings):
    print(f"Text {i}: {len(embedding)} dimensions")
