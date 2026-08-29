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


texts = [
    "TCP provides reliable delivery.",
    "TCP retransmits lost data.",
    "Python is a programming language.",
]

embeddings = []

for i, text in enumerate(texts):
    embedding = get_embedding(text)

    embeddings.append(embedding)

    print(f"Text {i}: {text}")
    print(f"Dimensions: {len(embedding)}")

similarity_tcp = cosine_similarity(
    embeddings[0],
    embeddings[1],
)

similarity_python = cosine_similarity(
    embeddings[0],
    embeddings[2],
)

print()
print("TCP ↔ TCP:", similarity_tcp)
print("TCP ↔ Python:", similarity_python)