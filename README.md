# 🏐 Volleyball Coach — Desafio de Avaliação de Agente de IA

## O que é este desafio

Este repositório contém a suíte de **testes automatizados e de segurança** usada para avaliar o **Volleyball Coach**, um agente de IA especializado em voleibol, construído sobre **Amazon Bedrock/AgentCore** e exposto via **API Gateway + Lambda**.

O objetivo do desafio é validar dois aspectos do agente:

1. **Qualidade das respostas** — usando um *Golden Dataset* de 22 casos e o framework **DeepEval** (integrado ao `pytest`) para medir aderência aos critérios esperados, fidelidade à Knowledge Base (*Faithfulness*) e relevância das respostas (*Answer Relevancy*).
2. **Segurança e resistência a ataques** — usando uma campanha de **Red Team** com 15 ataques (prompt injection, jailbreak, vazamento de informação e uso indevido de ferramentas).

Este código foi a base para o relatório completo do desafio (baseline, resultados de avaliação, achados do Red Team e comparação antes/depois da refatoração do agente).

## Estrutura do projeto

```
.
├── middleware_client.py           # Cliente HTTP que invoca o agente (via API Gateway)
├── judge.py                       # LLM avaliador local (Ollama) usado pelo DeepEval
├── red_team.py                    # Script que executa a campanha de Red Team
├── deepeval_dados/
│   └── golden_dataset.json        # 22 casos de teste (GD01–GD22)
├── red_team_dados/
│   ├── red_team_dataset.json      # 15 ataques (RT-01–RT-15)
│   └── response_redteam*.json     # Respostas registradas do agente por ataque
├── tests_deepeval/
│   ├── test_criteria.py           # Métrica G-Eval (critérios do Golden Dataset)
│   ├── test_faithfulness.py       # Métrica Faithfulness
│   └── test_relevancy.py          # Métrica Answer Relevancy
└── requirements.txt
```

## Pré-requisitos

- **Python 3.10+**
- O agente **Volleyball Coach já implantado** na AWS (Bedrock/AgentCore) com um endpoint HTTP acessível via API Gateway — os testes chamam esse endpoint, não simulam o agente localmente.
- **Ollama** instalado localmente, com o modelo `llama3.2:3b` baixado — é o LLM usado como *judge* pelas métricas do DeepEval:
  ```bash
  ollama pull llama3.2:3b
  ollama serve
  ```

## Configuração

1. Clone o repositório e crie um ambiente virtual:
   ```bash
   git clone https://github.com/marynmendes/Desafio-2.git
   cd Desafio-2
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Crie um arquivo `.env` na raiz do projeto com a URL do middleware/API Gateway do agente:
   ```
   API_URL=https://sua-api-gateway.exemplo.com/invoke
   ```
3. Confirme que o Ollama está rodando e com o modelo `llama3.2:3b` disponível.

> ⚠️ Os scripts de teste leem os arquivos JSON e importam `judge.py`/`middleware_client.py` usando caminhos relativos à pasta de onde são executados. Os comandos abaixo já consideram isso.

## Como testar

### 1. Testes automatizados (DeepEval + pytest)

```bash
cp judge.py middleware_client.py tests_deepeval/
cp deepeval_dados/golden_dataset.json tests_deepeval/
cd tests_deepeval

pytest test_criteria.py -v       # Métrica G-Eval — casos GD01 a GD07
pytest test_faithfulness.py -v   # Métrica Faithfulness — GD01, 03, 07, 10, 13, 16
pytest test_relevancy.py -v      # Métrica Answer Relevancy — GD01, 06, 09, 12, 15, 20
```

Cada teste envia a pergunta do caso para o agente (via `invoke_agent`), avalia a resposta com o modelo julgador local e falha se a nota ficar abaixo do *threshold* definido na métrica (0.8 para G-Eval e Faithfulness, 0.7 para Answer Relevancy).

### 2. Campanha de Red Team

```bash
cd ..   # volte para a raiz do projeto, se estiver em tests_deepeval/
cp red_team_dados/red_team_dataset.json .
python red_team.py
```

O script envia os 15 ataques (RT-01–RT-15) ao agente e salva as respostas em `response_redteam_novo.json`, com o `status_code` e a resposta completa de cada caso — use esse arquivo para conferir manualmente se o comportamento do agente correspondeu ao `expected_behavior` de cada ataque.

## O que observar nos resultados

- **DeepEval:** o teste falha automaticamente (via `assert_test`) se a nota da métrica ficar abaixo do threshold — acompanhe o relatório do `pytest` no terminal.
- **Red Team:** não há *assert* automático; a validação é manual, comparando `response.actual_output` com `expected_behavior` de cada caso em `response_redteam_novo.json`. Preste atenção especial a pedidos de extração de conteúdo bruto da Knowledge Base e a tentativas de revelar instruções internas — foram os pontos mais sensíveis identificados na baseline deste projeto.

## Observações

- Os testes dependem de um **agente já implantado e acessível**; sem uma `API_URL` válida no `.env`, todas as chamadas falham.
- O `judge.py` usa um LLM **local** via Ollama — sem o serviço rodando, as métricas do DeepEval não conseguem ser calculadas.
- O `requirements.txt` foi salvo em UTF-16; se o `pip install` reclamar de encoding, reabra e salve o arquivo como UTF-8 antes de instalar.


## Participação🤞
Agradeço a todos os meus colegas que estiveram dividindo suas dúvidas e descobertas comigo ao longo desse desafio, 
em especial ao meu amigo João Gabriel que foi quase um professor particular para mim!
