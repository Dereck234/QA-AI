from pathlib import Path


def criar_chunks(caminho):
    texto = caminho.read_text(encoding="utf-8")

    partes = texto.split("\n\n")

    chunks = []
    secao_atual = None

    for posicao, parte in enumerate(partes):
        parte = parte.strip()

        if not parte:
            continue

        if parte.startswith("#"):
            secao_atual = parte.lstrip("#").strip()

        chunk = {
            "text": parte,
            "source": str(caminho),
            "section": secao_atual,
            "position": posicao
        }

        chunks.append(chunk)

    return chunks