from pathlib import Path


def criar_chunks(caminho, tamanho_maximo=1000):
    texto = caminho.read_text(encoding="utf-8")

    linhas = texto.splitlines()

    chunks = []
    secao_atual = None
    texto_atual = ""

    for linha in linhas:
        linha = linha.strip()

        # Verifica se a linha é um título Markdown
        if linha.startswith("#"):
            # Salva o texto que estava sendo acumulado
            if texto_atual.strip() and len(texto_atual.strip()) > 100:
                chunks.append({
                    "text": texto_atual.strip(),
                    "source": str(caminho),
                    "section": secao_atual,
                    "position": len(chunks)
                })

            # Atualiza a seção
            secao_atual = linha.lstrip("#").strip()

            # Começa um novo bloco com o título
            texto_atual = linha

        else:
            if linha:
                texto_atual += "\n" + linha

                # Se ficou grande demais, cria um chunk
                if len(texto_atual) >= tamanho_maximo:
                    chunks.append({
                        "text": texto_atual.strip(),
                        "source": str(caminho),
                        "section": secao_atual,
                        "position": len(chunks)
                    })

                    texto_atual = ""

    # Não esquecer o último chunk
    if texto_atual.strip() and len(texto_atual.strip()) > 100:
        chunks.append({
            "text": texto_atual.strip(),
            "source": str(caminho),
            "section": secao_atual,
            "position": len(chunks)
        })

    return chunks