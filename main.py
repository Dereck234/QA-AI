import json
import urllib.request
import string


def build_prompt(question, chunks):
    context = "\n\n".join(chunks)

    return f"""
Answer the user's question using only the provided context.

Context:
{context}

Question:
{question}
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

def retrieve_chunks(question, chunks, top_k=2):
    scored_chunks = []

    for chunk in chunks:
        score = score_chunk(question, chunk)
        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True)

    return scored_chunks[:top_k]

with open("documents/networking.txt", "r", encoding="utf-8") as file:
    document = file.read()

chunks = document.split("\n\n")

question = "What does UDP provide?"

results = retrieve_chunks(question, chunks, top_k=2)

retrieved_chunks = [chunk for score, chunk in results]

prompt = build_prompt(question, retrieved_chunks)

print("\n--- RETRIEVED CONTEXT ---")

for score, chunk in results:
    print(f"\nScore: {score}")
    print(chunk)

answer = generate_answer(prompt)

print("\n--- ANSWER ---")
print(answer)