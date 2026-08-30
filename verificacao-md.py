from pathlib import Path

docs = list(Path("arquivos-md").rglob("*.md"))

print(f"Encontrados: {len(docs)} arquivos")