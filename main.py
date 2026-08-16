from dotenv import load_dotenv
from google import genai


def build_prompt(question):
    return f"""
Answer the user's question clearly and concisely.

Question:
{question}
"""


load_dotenv()

client = genai.Client()

question = input("Question: ")

prompt = build_prompt(question)

print("\n--- PROMPT SENT TO MODEL ---")
print(prompt)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt,
)

print("Answer:", response.text)
print("Model:", response.model_version)
print("Prompt tokens:", response.usage_metadata.prompt_token_count)
print("Output tokens:", response.usage_metadata.candidates_token_count)
print("Total tokens:", response.usage_metadata.total_token_count)
