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
git clone https://github.com/LeonardoSantosM/Trabalho_Louzada_G2.git
cd Trabalho_Louzada_G2
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
Trabalho_Louzada_G2/
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
- ✅ Filtros múltiplos no Streamlit (região, bioma, nível de risco, período)
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

- 📁 **Repositório GitHub:** [github.com/LeonardoSantosM/Trabalho_Louzada_G2](https://github.com/LeonardoSantosM/Trabalho_Louzada_G2)
- 🌐 **GitHub Pages:** [leonardosantosm.github.io/Trabalho_Louzada_G2](https://leonardosantosm.github.io/Trabalho_Louzada_G2/)
- 📊 **Dashboard Streamlit:** [trabalholouzadag2.streamlit.app](https://trabalholouzadag2-cmejao59ub6qfdja96jiwg.streamlit.app/)

---

## 📚 Fonte dos Dados

Dados simulados com base na metodologia do **INPE** (Instituto Nacional de Pesquisas Espaciais) — Programa de Monitoramento de Queimadas.
