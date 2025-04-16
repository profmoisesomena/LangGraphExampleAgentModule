# LangGraphExampleAgent 🌐

Este projeto cria um agente inteligente capaz de buscar informações atualizadas na web usando o modelo **Gemini-2.5-pro-exp-03-25** integrado à **Tavily Search API**.

O agente é implementado usando a arquitetura **ReAct** via **LangGraph**, permitindo raciocinar sobre perguntas recebidas e e executar ações externas (como buscas online) para construir respostas mais completas e atualizadas..

Esta versão do projeto incorpora integração com LangSmith para rastreamento (tracing) das execuções do agente, possibilitando inspecionar e avaliar o passo a passo de suas operações.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.12+](https://www.python.org/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain Core](https://github.com/langchain-ai/langchain)
- [LangChain Google Generative AI (Gemini)](https://github.com/langchain-ai/langchain/tree/main/libs/langchain-google-genai)
- [LangChain Community Tools (Tavily)](https://github.com/langchain-ai/langchain/tree/main/libs/langchain-community)
- [Tavily Search API](https://app.tavily.com/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [LangSmith (plataforma de observabilidade e tracing para agentes LangChain)](https://pypi.org/project/langsmith/)

---

## 📦 Estrutura do Projeto

```
LangGraphExampleAgentWithTracing/
├── .env.example     # Exemplo de configuração de variáveis de ambiente
├── README.md        # Documentação do projeto
├── langgraph_example.py         # Código principal do agente LangGraph (ReAct Agent)
├── requirements.txt # (opcional) Arquivo com dependências do projeto
└── langgraph.json   # Arquivo de Configuração LangGraph
```

## ✨ Novidades e Funcionalidades Adicionadas

- **Integração com LangSmith:** Agora o agente pode registrar automaticamente suas execuções na plataforma LangSmith.
- **Função `run_agent` com decorator `@traceable`:** Facilita rastreamento de interações individuais com o agente.
- **Execução direta com exemplo integrado:** Permite rodar rapidamente uma consulta de exemplo.

#### Imagem com exemplo de tracing de projetos

![alt text](image.png)
---

## ⚙️ Configuração e Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/profmoisesomena/LangGraphExampleAgentWithTracing.git
cd LangGraphExampleAgentWithTracing
```

2. **Crie e ative um ambiente virtual:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # Linux / MacOS
# ou
.venv\Scripts\activate      # Windows
```

3. **Instale as dependências necessárias:**

```bash
pip install -U langgraph langchain-core langchain-google-genai langchain-community tavily-python python-dotenv
pip install -U "langgraph-cli[inmem]"
```

*(Dica: Você pode também criar um `requirements.txt` com essas bibliotecas para facilitar a instalação.)*

4. **Configure as variáveis de ambiente:**

Crie um arquivo `.env` baseado no exemplo `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` preenchendo com suas chaves de API:

```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
```

---

## 🚀 Como Rodar o Agente

Após configurar tudo, para iniciar o ambiente de desenvolvimento do LangGraph:

```bash
langgraph dev
```

Isso abrirá um ambiente interativo para testar o agente!


---
**Execução direta no terminal:**

```bash
python langgraph_example.py
```

---

## 💑 Sobre o `langgraph.json`

O arquivo `langgraph.json` pode ser utilizado para configurar e gerenciar múltiplos agentes, rotas e parâmetros de execução no seu projeto LangGraph.


---

## 🤝 Contribuindo

Contribuições são muito bem-vindas!

- Encontrou um problema? Abra uma [issue](https://github.com/profmoisesomena/LangGraphExampleAgentWithTracing/issues).
- Quer melhorar o agente? Envie um pull request!

Sugestões, melhorias e correções pertinentes são bem vindas. 🚀



