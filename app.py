import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import os

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Queimadas no Brasil",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ───────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #C0392B;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #7F8C8D;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-left: 4px solid #E74C3C;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        color: white;
    }
    .kpi-label { font-size: 0.8rem; color: #BDC3C7; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #E74C3C; }
    .kpi-delta { font-size: 0.85rem; color: #2ECC71; }
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2C3E50;
        border-bottom: 2px solid #E74C3C;
        padding-bottom: 0.3rem;
        margin: 1.5rem 0 1rem 0;
    }
    .insight-box {
        background: #FEF9F0;
        border-left: 4px solid #F39C12;
        border-radius: 6px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        color: #2C3E50;
    }
</style>
""", unsafe_allow_html=True)

# ── Banco de dados SQLite (funcionalidade avançada) ─────────────────────────
DB_PATH = "database/queimadas.db"

@st.cache_resource
def init_db(csv_path: str):
    os.makedirs("database", exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_csv(csv_path, parse_dates=["data"])
    df.to_sql("queimadas", engine, if_exists="replace", index=False)
    return engine

@st.cache_data
def load_data(csv_path: str):
    df = pd.read_csv(csv_path, parse_dates=["data"])
    df["mes_nome"] = df["data"].dt.month_name()
    df["trimestre"] = df["data"].dt.quarter.map({1: "T1", 2: "T2", 3: "T3", 4: "T4"})
    return df

# ── Caminhos ────────────────────────────────────────────────────────────────
CSV_PATH = "dados/simulacao_queimadas_brasil.csv"
engine = init_db(CSV_PATH)
df_raw = load_data(CSV_PATH)

# ══════════════════════════════════════════════════════════
# SIDEBAR — Filtros múltiplos (funcionalidade intermediária)
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🔍 Filtros")

    anos = sorted(df_raw["ano"].unique())
    ano_range = st.slider("Período (ano)", min_value=int(min(anos)), max_value=int(max(anos)),
                          value=(int(min(anos)), int(max(anos))))

    regioes = st.multiselect("Região", sorted(df_raw["regiao"].unique()),
                             default=sorted(df_raw["regiao"].unique()))

    biomas = st.multiselect("Bioma", sorted(df_raw["bioma"].unique()),
                            default=sorted(df_raw["bioma"].unique()))

    riscos = st.multiselect("Nível de Risco", ["Baixo", "Médio", "Alto", "Crítico"],
                            default=["Baixo", "Médio", "Alto", "Crítico"])

    st.markdown("---")
    st.markdown("**Fonte:** Dados simulados — INPE  \n**Disciplina:** Análise e Visualização de Dados com Python")

# ── Filtragem ────────────────────────────────────────────────────────────────
df = df_raw[
    (df_raw["ano"] >= ano_range[0]) &
    (df_raw["ano"] <= ano_range[1]) &
    (df_raw["regiao"].isin(regioes)) &
    (df_raw["bioma"].isin(biomas)) &
    (df_raw["nivel_risco"].isin(riscos))
].copy()

# ══════════════════════════════════════════════════════════
# CABEÇALHO
# ══════════════════════════════════════════════════════════
st.markdown('<div class="main-title">🔥 Queimadas no Brasil (2015–2024)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Análise exploratória e monitoramento de focos de incêndio por região, bioma e indicadores ambientais.</div>', unsafe_allow_html=True)

if df.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

# ══════════════════════════════════════════════════════════
# SEÇÃO 1 — KPIs Dinâmicos
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Indicadores-Chave (KPIs)</div>', unsafe_allow_html=True)

total_focos = int(df["focos_queimada"].sum())
total_area  = df["area_atingida_km2"].sum()
media_temp  = df["temperatura_media"].mean()
media_chuva = df["chuva_mm"].mean()
pct_critico = (df["nivel_risco"] == "Crítico").mean() * 100
media_seca  = df["indice_seca"].mean()

c1, c2, c3, c4, c5, c6 = st.columns(6)
kpis = [
    (c1, "🔥 Total de Focos",       f"{total_focos:,}",         "focos registrados"),
    (c2, "🌍 Área Atingida (km²)",  f"{total_area:,.0f}",        "km² afetados"),
    (c3, "🌡️ Temp. Média (°C)",     f"{media_temp:.1f}°C",       "temperatura média"),
    (c4, "🌧️ Chuva Média (mm)",     f"{media_chuva:.1f} mm",     "precipitação média"),
    (c5, "⚠️ Eventos Críticos",     f"{pct_critico:.1f}%",       "dos registros"),
    (c6, "🏜️ Índice de Seca",       f"{media_seca:.2f}",         "média do período"),
]
for col, label, value, sublabel in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta">{sublabel}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 2 — Análise Temporal
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📅 Análise Temporal</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    focos_ano = df.groupby("ano")["focos_queimada"].sum().reset_index()
    fig_line = px.line(focos_ano, x="ano", y="focos_queimada",
                       title="Evolução Anual de Focos de Queimada",
                       markers=True, color_discrete_sequence=["#E74C3C"],
                       labels={"ano": "Ano", "focos_queimada": "Focos"})
    fig_line.update_layout(plot_bgcolor="#FAFAFA", paper_bgcolor="white")
    st.plotly_chart(fig_line, use_container_width=True)

with col_b:
    focos_mes = df.groupby("mes")["focos_queimada"].mean().reset_index()
    focos_mes["mes_nome"] = pd.to_datetime(focos_mes["mes"], format="%m").dt.strftime("%b")
    fig_bar = px.bar(focos_mes, x="mes_nome", y="focos_queimada",
                     title="Média Mensal de Focos (sazonalidade)",
                     color="focos_queimada", color_continuous_scale="Reds",
                     labels={"mes_nome": "Mês", "focos_queimada": "Média de Focos"})
    fig_bar.update_layout(plot_bgcolor="#FAFAFA", paper_bgcolor="white", coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown('<div class="insight-box">💡 <b>Insight:</b> Os meses de agosto a outubro concentram historicamente os maiores picos de queimada no Brasil, coincidindo com o período de seca nas regiões Norte e Centro-Oeste.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 3 — Análise por Região e Bioma
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🗺️ Distribuição por Região e Bioma</div>', unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    focos_regiao = df.groupby("regiao")["focos_queimada"].sum().reset_index().sort_values("focos_queimada", ascending=True)
    fig_reg = px.bar(focos_regiao, x="focos_queimada", y="regiao", orientation="h",
                     title="Total de Focos por Região",
                     color="focos_queimada", color_continuous_scale="Oranges",
                     labels={"regiao": "Região", "focos_queimada": "Focos"})
    fig_reg.update_layout(plot_bgcolor="#FAFAFA", paper_bgcolor="white", coloraxis_showscale=False)
    st.plotly_chart(fig_reg, use_container_width=True)

with col_d:
    focos_bioma = df.groupby("bioma")["area_atingida_km2"].sum().reset_index()
    fig_pie = px.pie(focos_bioma, names="bioma", values="area_atingida_km2",
                     title="Área Atingida por Bioma (km²)",
                     color_discrete_sequence=px.colors.sequential.RdBu)
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    fig_pie.update_layout(paper_bgcolor="white", showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 4 — Correlação Estatística (funcionalidade avançada)
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📈 Correlações Estatísticas</div>', unsafe_allow_html=True)

col_e, col_f = st.columns(2)

with col_e:
    numeric_cols = ["focos_queimada", "temperatura_media", "chuva_mm",
                    "area_atingida_km2", "indice_seca", "qualidade_ar"]
    corr = df[numeric_cols].corr()
    fig_corr, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn_r",
                linewidths=0.5, ax=ax, annot_kws={"size": 9})
    ax.set_title("Mapa de Correlação entre Variáveis", fontsize=12, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig_corr)

with col_f:
    fig_scatter = px.scatter(df, x="indice_seca", y="focos_queimada",
                             color="regiao", size="area_atingida_km2",
                             title="Índice de Seca vs. Focos de Queimada",
                             labels={"indice_seca": "Índice de Seca", "focos_queimada": "Focos"},
                             opacity=0.7, hover_data=["uf", "bioma"])
    fig_scatter.update_layout(plot_bgcolor="#FAFAFA", paper_bgcolor="white")
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown('<div class="insight-box">💡 <b>Insight:</b> Existe correlação positiva entre índice de seca e número de focos, e correlação negativa entre chuva e área atingida — confirmando que secas prolongadas potencializam a propagação das queimadas.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 5 — Nível de Risco
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">⚠️ Distribuição do Nível de Risco</div>', unsafe_allow_html=True)

col_g, col_h = st.columns(2)

with col_g:
    risco_ordem = ["Baixo", "Médio", "Alto", "Crítico"]
    risco_cores = {"Baixo": "#2ECC71", "Médio": "#F39C12", "Alto": "#E67E22", "Crítico": "#C0392B"}
    risco_count = df["nivel_risco"].value_counts().reindex(risco_ordem).dropna().reset_index()
    risco_count.columns = ["nivel_risco", "count"]
    fig_risco = px.bar(risco_count, x="nivel_risco", y="count",
                       title="Frequência por Nível de Risco",
                       color="nivel_risco", color_discrete_map=risco_cores,
                       labels={"nivel_risco": "Nível de Risco", "count": "Registros"})
    fig_risco.update_layout(plot_bgcolor="#FAFAFA", paper_bgcolor="white", showlegend=False)
    st.plotly_chart(fig_risco, use_container_width=True)

with col_h:
    risco_bioma = df.groupby(["bioma", "nivel_risco"]).size().reset_index(name="count")
    fig_heat = px.density_heatmap(df, x="bioma", y="nivel_risco",
                                  title="Concentração de Risco por Bioma",
                                  category_orders={"nivel_risco": risco_ordem},
                                  color_continuous_scale="Reds",
                                  labels={"bioma": "Bioma", "nivel_risco": "Risco"})
    fig_heat.update_layout(plot_bgcolor="#FAFAFA", paper_bgcolor="white")
    st.plotly_chart(fig_heat, use_container_width=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 6 — Tabela de dados filtrados
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📋 Dados Filtrados</div>', unsafe_allow_html=True)

colunas_exibir = ["ano", "mes", "regiao", "uf", "bioma", "focos_queimada",
                  "temperatura_media", "chuva_mm", "area_atingida_km2",
                  "indice_seca", "qualidade_ar", "nivel_risco"]
st.dataframe(
    df[colunas_exibir].sort_values(["ano", "mes"]).reset_index(drop=True),
    use_container_width=True,
    height=300,
)

st.caption(f"Exibindo {len(df):,} registros de {len(df_raw):,} no total.")

# ══════════════════════════════════════════════════════════
# SEÇÃO 7 — Conclusão executiva
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📝 Conclusão Executiva</div>', unsafe_allow_html=True)

st.markdown("""
O presente painel analisou **{:,} registros** de focos de queimada no Brasil entre **{} e {}**, 
abrangendo **{} regiões**, **{} biomas** e **{} estados**.

**Principais achados:**
- A região **Norte** concentra o maior volume de focos, especialmente nos estados do Pará e Amazonas.
- O **Cerrado** e a **Amazônia** são os biomas com maior área atingida por queimadas.
- Existe forte correlação entre **índice de seca elevado** e aumento de focos — indicando que o monitoramento climático é fundamental para a prevenção.
- Os meses de **agosto a outubro** representam o período crítico de risco, alinhado à estação seca.
- Eventos classificados como **Crítico** representam {:.1f}% dos registros, mas respondem por uma parcela desproporcional da área destruída.

**Recomendação:** Investir em sistemas de alerta precoce integrados ao índice de seca e temperatura, 
priorizando ações preventivas nas regiões Norte e Centro-Oeste durante o segundo semestre.
""".format(
    len(df),
    df["ano"].min(), df["ano"].max(),
    df["regiao"].nunique(),
    df["bioma"].nunique(),
    df["uf"].nunique(),
    pct_critico
))
