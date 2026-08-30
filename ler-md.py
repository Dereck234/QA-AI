from pathlib import Path

docs = list(Path("arquivos-md").rglob("*.md"))

for doc in docs:
    print("=" * 50)
    print(f"Arquivo: {doc}")
    print("=" * 50)

    texto = doc.read_text(encoding="utf-8")

    print(texto[:500])
    print()