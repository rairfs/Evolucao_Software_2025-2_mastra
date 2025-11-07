# 🧾 Evolução de Software 2025-2

### Equipe 4

01 - Carlos Eduardo Dias dos Santos - 202100104941  
02 - Déborah Abreu Sales - 202100060758  
03 - Eduardo Afonso Passos Silva - 201800102096  
04 - Guilherme Ilan Barboza Carvalho - 201900051196  
05 - Marcelo Venicius Almeida Lima - 202000012981  
06 - Mikael Douglas Santos Farias - 201700053275  
07 - Raí Rafael Santos Silva – 202000138043  
08 - Matheus Soares Santana - 201800147786

## 🎯 Objetivo da atividade

A atividade consiste nos seguintes passos:

- **Selecionar um projeto** do GitHub da lista fornecida no google classroom.
- **Coletar os últimos 100 pull requests fechados** do projeto.
- **Escolher três modelos de linguagem da Hugging Face** com foco em análise de sentimentos (filtro: `language=en` e `search=sentiment`).

  - URL Hugging Face: [https://huggingface.co/models?language=en&sort=trending&search=sentiment](https://huggingface.co/models?language=en&sort=trending&search=sentiment)

- **Executar análise de sentimentos** em todos os comentários dos 100 PRs usando os três modelos escolhidos.
- **Apresentar resultados detalhados e resumidos**, incluindo:

  - Tabela comparando os resultados entre os modelos.
  - Avaliação de quais modelos foram mais efetivos.
  - Impacto da evolução dos PRs no projeto analisado.

- **Entrega**:
  - Tutorial em PDF no Google Classroom (nomes dos integrantes e contribuições detalhadas).
  - Projeto público no GitHub com todo o código e artefatos utilizados.
  - Vídeo explicativo com duração mínima de 7 minutos demonstrando a execução da atividade.

---

# 1. Script de pré-processamento

Este repositório contém o **script_coleta_prs** utilizado para a atividade da disciplina, cujo objetivo é realizar uma análise de sentimentos em comentários de pull requests de um projeto no GitHub.

O script_coleta_prs **coleta os últimos 100 pull requests fechados** do repositório [`mastra-ai/mastra`](https://github.com/mastra-ai/mastra) e todos os comentários associados a esses PRs. Esta etapa é o **pré-processamento** necessário para que, posteriormente, sejam aplicados **modelos de linguagem da Hugging Face** para análise de sentimentos.

## ⚙️ Pré-requisitos

Para executar o script:

1. **Python 3.10+**

   ```bash
   python --version
   ```

2. **Instalar dependências**

   ```bash
   pip install requests tqdm python-dotenv
   ```

3. **GitHub Personal Access Token** (opcional, mas recomendado para evitar limite da API):
   - Criar em [https://github.com/settings/tokens](https://github.com/settings/tokens) com permissão `repo`.
   - Criar um arquivo `.env` na raiz do projeto:
     ```
     GITHUB_TOKEN=seu_token_aqui
     ```
   - ⚠️ O `.env` está listado no `.gitignore` para não ser enviado ao GitHub.

---

## 🚀 Como executar

```bash
python script_coleta_prs.py
```

O script realizará:

1. Coleta dos **100 últimos PRs fechados**.
2. Salvamento das informações dos PRs em:
   - `output/pull_requests.csv`
   - `output/pull_requests.md`
3. Coleta de **todos os comentários** de cada PR.
4. Salvamento dos comentários em:
   - `output/pr_comments.csv`

---

## 📂 Estrutura de saída

```
output/
│
├─ pull_requests.csv       # Lista dos 100 últimos PRs
├─ pull_requests.md        # Lista dos 100 últimos PRs em Markdown
└─ pr_comments.csv         # Todos os comentários de todos os PRs
```

- CSV separado por ponto e vírgula (`;`).
- Markdown visual legível em navegadores ou editores Markdown.

---

##  Modelos de linguagem utilizados
- [tabularisai/multilingual-sentiment-analysis](https://huggingface.co/tabularisai/multilingual-sentiment-analysis)
- [lxyuan/distilbert-base-multilingual-cased-sentiments-student](https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student)
- [nlptown/bert-base-multilingual-uncased-sentiment](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment)

## 🔜 Próximos passos

- Aplicar **modelos de linguagem da Hugging Face** para análise de sentimentos.
- Gerar **relatórios comparativos** entre os modelos.
- Avaliar **impactos na evolução do projeto** com base na análise de sentimentos.
