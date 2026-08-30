# QA AI Workshop

## Identificação

* Nome do aluno: Dereck Patrick Morais de Sá
* Formato da solução: Script
* Link do vídeo: https://youtu.be/Gynto_8WXPU
* Link do Github: https://github.com/Dereck234/QA-AI/tree/workshop

## Objetivo

Uma IA capaz de compreender perguntas e oferecer respostas relevantes sobre a documentação do projeto HTTPX.

A solução implementa um sistema de QA baseado em recuperação semântica. Os documentos são divididos em chunks, transformados em embeddings e comparados com o embedding da pergunta para recuperar os trechos mais relevantes. Os resultados recuperados podem então ser utilizados pelo modelo local para gerar uma resposta baseada na documentação.

## Arquitetura resumida

```text
Documentos Markdown
        ↓
      Chunks
        ↓
    Embeddings
        ↓
      Índice
        ↓
Pergunta → Embedding
        ↓
Similaridade de cosseno
        ↓
Threshold + Top-K
        ↓
Trechos relevantes
        ↓
Modelo local Qwen3
        ↓
Resposta + Fontes
```

A base utilizada contém 23 arquivos Markdown da documentação do HTTPX.

Os documentos são divididos em chunks e cada chunk mantém metadados de origem, seção e posição. Os chunks são transformados em embeddings de 768 dimensões utilizando o modelo `nomic-embed-text`.

Durante uma consulta, o embedding da pergunta é comparado com os embeddings dos chunks utilizando similaridade de cosseno. Os resultados são ordenados pelo score, filtrados pelo threshold e os 3 melhores resultados são retornados.

Os resultados recuperados são utilizados como contexto para a geração da resposta utilizando o modelo local `qwen3:8b`.

## Como executar do zero

### 1. Requisitos

* Python 3.x
* Ollama instalado e funcionando localmente
* Modelo `nomic-embed-text`
* Modelo `qwen3:8b`

### 2. Instalar os modelos no Ollama

```bash
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

O projeto utiliza o Ollama localmente, portanto não é necessário utilizar uma API paga ou fornecer uma API key.

### 3. Obter a base HTTPX

A base utilizada na atividade corresponde ao repositório:

```text
https://github.com/encode/httpx
```

Commit utilizado:

```text
b5addb64f0161ff6bfe94c124ef76f6a1fba5254
```

Os arquivos Markdown utilizados correspondem à documentação do HTTPX.

A busca recursiva encontrou:

```text
Encontrados: 23 arquivos
```

### 4. Criar o ambiente Python

```bash
python -m venv .venv
```

Ative o ambiente virtual e instale as dependências necessárias.

### 5. Criar o índice

O índice é criado percorrendo os arquivos Markdown, gerando os chunks e calculando um embedding para cada chunk.

Na versão utilizada nos testes:

```text
Total de chunks: 264
Total de embeddings: 264
Tamanho dos embeddings: 768
```

O índice é armazenado em `indice.json`.

### 6. Fazer uma pergunta

Execute:

```bash
python teste_rag.py
```

O sistema solicitará uma pergunta:

```text
Digite sua pergunta:
```

Digite a pergunta desejada e pressione Enter.

O sistema exibirá a resposta e as fontes recuperadas.

## Decisões técnicas

### Chunking

* Estratégia: divisão baseada em títulos Markdown.
* Tamanho máximo: 1000 caracteres.
* Overlap: não utilizado.
* Metadados armazenados: `text`, `source`, `section` e `position`.

O sistema identifica linhas que começam com `#` e utiliza os títulos para determinar a seção atual. O conteúdo é acumulado até atingir o limite configurado.

Chunks finais com 100 caracteres ou menos não são adicionados ao índice.

A estratégia foi escolhida porque a documentação do HTTPX possui uma estrutura organizada por títulos e subseções, permitindo preservar o contexto de cada trecho.

### Embeddings e busca

* Modelo: `nomic-embed-text`.
* Execução: Ollama local.
* Dimensão: 768.
* Similaridade: cosseno.
* `top_k`: 3.
* Threshold: 0.60.

O mesmo modelo é utilizado para gerar o embedding dos documentos e das perguntas.

O fluxo de recuperação é:

```text
Pergunta
   ↓
Embedding da pergunta
   ↓
Similaridade com cada chunk
   ↓
Ordenação por score
   ↓
Filtro por threshold >= 0.60
   ↓
Top 3 resultados
```

O `top_k=3` foi escolhido para limitar a quantidade de contexto recuperado e facilitar a identificação dos trechos mais relevantes.

O threshold de `0.60` evita que resultados com baixa similaridade sejam considerados suficientemente relevantes.

### Metadados e fontes

Cada chunk mantém informações sobre sua origem:

```text
source
section
position
```

Durante a busca, essas informações são retornadas junto com o score de similaridade.

Exemplo:

```text
Score: 0.7403 | arquivos-md\async.md → Making requests
```

Dessa forma, é possível rastrear o resultado recuperado até o arquivo e a seção correspondente da documentação original.

## Perguntas de teste

### 1. Pergunta com resposta clara

* Pergunta: `How do I make asynchronous HTTP requests?`
* Resultado esperado: encontrar informações relacionadas ao uso do `AsyncClient`, `async/await` e métodos de requisição assíncronos.
* O resultado foi relevante? Por quê: Sim. Os três primeiros resultados vieram de `async.md` e estavam diretamente relacionados ao assunto da pergunta.

Resultados observados:

```text
Score: 0.7403 | arquivos-md\async.md → Making requests
Score: 0.7377 | arquivos-md\async.md → Async Support
Score: 0.7154 | arquivos-md\async.md → Making Async requests
```

Os trechos recuperados explicam o uso do `AsyncClient` e de `await` para realizar requisições assíncronas.

### 2. Pergunta ampla ou ambígua

* Pergunta: `How does HTTPX work?`
* Resultado esperado: encontrar informações gerais relacionadas ao funcionamento do HTTPX.
* O resultado foi relevante? Por quê: Não. Nenhum resultado atingiu o threshold mínimo de `0.60`, portanto o sistema informou que não encontrou a informação na documentação fornecida.

Esse teste demonstrou uma limitação do retriever: perguntas muito amplas podem não possuir similaridade suficiente com um chunk específico.

### 3. Pergunta fora do escopo

* Pergunta: `What is the capital of Brazil?`
* Como o sistema reagiu: o sistema informou que não encontrou essa informação na documentação fornecida.
* Como essa reação poderia melhorar: o sistema poderia apresentar uma mensagem mais específica indicando que a pergunta provavelmente está fora do domínio da documentação ou que nenhum trecho atingiu o threshold mínimo de similaridade.

## Limitações conhecidas

* Perguntas muito amplas podem não atingir o threshold mínimo de similaridade.
* O sistema não possui interface gráfica e funciona por meio do terminal.
* Não existe overlap entre chunks.
* A estratégia de chunking é baseada em títulos Markdown e limite de caracteres.
* O threshold de `0.60` é fixo e pode precisar de ajustes dependendo das perguntas.
* A qualidade da resposta gerada depende da qualidade dos trechos recuperados.
* O sistema depende do Ollama e dos modelos locais para gerar embeddings e respostas.

## Uso de ferramentas de IA

* Ferramenta utilizada: ChatGPT.
* Tarefas em que ajudou: estudo dos conceitos de RAG, embeddings, similaridade semântica, planejamento da implementação, revisão de código, interpretação de erros, elaboração de testes e documentação.
* Exemplo representativo de prompt ou orientação: solicitação para explicar passo a passo como implementar e compreender um sistema de QA/RAG, incluindo chunking, embeddings, busca semântica, geração de respostas e avaliação.
* O que foi testado, modificado ou validado por mim: a solução foi executada localmente. Foram testados a leitura dos documentos, criação dos chunks, geração dos embeddings, criação do índice, busca semântica, threshold, `top_k`, tratamento de perguntas fora do domínio e identificação das fontes.

## Referências e código externo

* Repositório HTTPX: `https://github.com/encode/httpx`
* Commit utilizado: `b5addb64f0161ff6bfe94c124ef76f6a1fba5254`
* Ollama
* Modelo de embeddings: `nomic-embed-text`
* Modelo de geração: `qwen3:8b`
* Documentação utilizada: arquivos Markdown da documentação do HTTPX.

O código da solução foi desenvolvido e adaptado durante a atividade, utilizando IA como ferramenta de apoio para aprendizado, revisão e resolução de problemas.

## Segurança

* [x] Minha solução não usa API key.
* [ ] Minha solução usa segredo protegido e nenhuma chave foi publicada.
