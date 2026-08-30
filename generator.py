import json
import urllib.request


def gerar_resposta(pergunta, resultados):
    contexto = ""

    for i, resultado in enumerate(resultados, start=1):
        chunk = resultado["chunk"]

        contexto += f"""
[Contexto {i}]
Arquivo: {chunk["source"]}
Seção: {chunk["section"]}
Texto:
{chunk["text"]}
"""

    prompt = f"""
Você é um assistente especializado na documentação do HTTPX.

REGRAS IMPORTANTES:
- Responda somente usando informações explicitamente presentes no contexto.
- Não use conhecimento externo ao contexto.
- Não invente informações.
- Não adicione dicas, exemplos ou explicações que não estejam no contexto.
- Se a informação necessária para responder à pergunta não estiver no contexto,
  responda exatamente:
  "Não encontrei essa informação na documentação fornecida."

Contexto:
{contexto}

Pergunta:
{pergunta}

Resposta:
"""

    data = {
        "model": "qwen3:8b",
        "prompt": prompt,
        "stream": False
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["response"]