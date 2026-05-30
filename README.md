# 🔥 Análise de Queimadas no Brasil (2015–2024)

> Projeto de Análise e Visualização de Dados — Avaliação G2  
> Disciplina: Linguagem de Programação — Análise e Visualização de Dados com Python

---

## 📌 Sobre o Projeto

Este projeto realiza uma análise exploratória completa dos focos de queimadas no Brasil entre 2015 e 2024, utilizando dados por região, bioma, estado e variáveis climáticas como temperatura, precipitação e índice de seca.

O objetivo é identificar padrões temporais e espaciais, correlações entre clima e queimadas, e apresentar os resultados em um dashboard interativo.

---

## 🚀 Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/projeto-g2.git
cd projeto-g2
```

### 2. Crie um ambiente virtual e instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Execute o dashboard

```bash
streamlit run app.py
```

### 4. Execute o notebook

```bash
jupyter notebook notebooks/analise_queimadas.ipynb
```

---

## 📁 Estrutura do Projeto

```
projeto-g2/
│
├── app.py                          # Dashboard Streamlit
├── requirements.txt                # Dependências Python
├── README.md                       # Documentação
├── index.html                      # GitHub Pages
│
├── dados/
│   └── simulacao_queimadas_brasil.csv
│
├── database/
│   └── queimadas.db                # Gerado automaticamente
│
├── notebooks/
│   └── analise_queimadas.ipynb
│
└── imagens/
    └── (geradas ao rodar o notebook)
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| Pandas | Manipulação de dados |
| Matplotlib | Visualizações estáticas |
| Seaborn | Gráficos estatísticos |
| Plotly | Gráficos interativos |
| Streamlit | Dashboard web |
| SQLAlchemy + SQLite | Persistência de dados |
| NumPy | Operações numéricas |

### Funcionalidades Intermediárias
- ✅ Filtros múltiplos no Streamlit (região, bioma, período, nível de risco)
- ✅ KPIs dinâmicos (atualizam conforme filtros)
- ✅ Gráficos interativos (Plotly)
- ✅ Análise temporal (evolução anual e sazonalidade mensal)

### Funcionalidades Avançadas
- ✅ Persistência em banco de dados (SQLAlchemy + SQLite)
- ✅ Correlação estatística (mapa de calor + scatter com tendência)

---

## 📊 KPIs Monitorados

- Total de focos de queimada
- Área total atingida (km²)
- Temperatura média (°C)
- Precipitação média (mm)
- Índice de seca médio
- Percentual de eventos críticos

---

## 🔗 Links

- 📁 **Repositório GitHub:** [github.com/SEU_USUARIO/projeto-g2](https://github.com/SEU_USUARIO/projeto-g2)
- 🌐 **GitHub Pages:** [SEU_USUARIO.github.io/projeto-g2](https://SEU_USUARIO.github.io/projeto-g2)
- 📊 **Dashboard Streamlit:** [seu-projeto.streamlit.app](https://seu-projeto.streamlit.app)

---

## 📚 Fonte dos Dados

Dados simulados com base na metodologia do **INPE** (Instituto Nacional de Pesquisas Espaciais) — Programa de Monitoramento de Queimadas.
