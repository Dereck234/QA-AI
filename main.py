import json
import urllib.request
import string


STOP_WORDS = {
    "a",
    "an",
    "the",
    "is",
    "are",
    "what",
    "does",
    "do",
    "how",
    "why",
    "when",
    "where",
    "to",
    "of",
    "in",
    "on",
}


def build_prompt(question, chunks):
    context = "\n\n".join(chunks)

    return f"""
Answer the user's question using only the provided context.

Context:
{context}

Question:
{question}

Answer:
"""


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


def score_chunk(question, chunk):
    question_words = question.lower().split()
    chunk_words = chunk.lower().split()

    question_words = [
        word.strip(string.punctuation)
        for word in question_words
    ]

    chunk_words = [
        word.strip(string.punctuation)
        for word in chunk_words
    ]

    score = 0

    for word in question_words:
        if word in STOP_WORDS:
            continue

        if word in chunk_words:
            score += 1

    return score


with open("documents/networking.txt", "r", encoding="utf-8") as file:
    document = file.read()

chunks = document.split("\n\n")


question = input("Question: ")

results = []

for chunk in chunks:
    score = score_chunk(question, chunk)
    results.append((score, chunk))

# Most relevant chunks first
results.sort(key=lambda x: x[0], reverse=True)

# Keep only the 5 best chunks
results = results[:5]

retrieved_chunks = [chunk for score, chunk in results]

prompt = build_prompt(question, retrieved_chunks)

print("\n--- RETRIEVED CONTEXT ---")

for score, chunk in results:
    print(f"\nScore: {score}")
    print(chunk)

answer = generate_answer(prompt)

print("\n--- ANSWER ---")
print(answer)