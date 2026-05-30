import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os

st.set_page_config(
    page_title="Monitor de Queimadas · Brasil",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paleta ──────────────────────────────────────────────────────────────────
# Verde-floresta profundo + âmbar queimado + fundo carvão
C_BG       = "#0B0F0E"   # fundo principal
C_SURFACE  = "#111714"   # superfície cards
C_BORDER   = "#1E2D24"   # bordas sutis
C_GREEN    = "#2D6A4F"   # verde floresta
C_GREEN_LT = "#52B788"   # verde claro acento
C_AMBER    = "#D4842A"   # âmbar queimado
C_AMBER_LT = "#F4A641"   # âmbar claro
C_TEXT     = "#E8F0EB"   # texto principal
C_MUTED    = "#7A9E87"   # texto secundário

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {{
      font-family: 'DM Sans', sans-serif;
      background-color: {C_BG};
      color: {C_TEXT};
  }}

  /* Sidebar */
  section[data-testid="stSidebar"] {{
      background-color: {C_SURFACE} !important;
      border-right: 1px solid {C_BORDER} !important;
  }}
  section[data-testid="stSidebar"] * {{
      color: {C_TEXT} !important;
  }}

  /* Multiselect tags */
  span[data-baseweb="tag"] {{
      background-color: {C_GREEN} !important;
      border: 1px solid {C_GREEN_LT} !important;
      color: #fff !important;
      border-radius: 4px !important;
  }}

  /* Slider */
  div[data-testid="stSlider"] div[role="slider"] {{
      background-color: {C_AMBER} !important;
  }}
  div[data-testid="stSlider"] .st-bq {{
      background-color: {C_AMBER} !important;
  }}

  .hero-tag {{
      font-family: 'DM Mono', monospace;
      font-size: 0.7rem;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: {C_GREEN_LT};
      margin-bottom: 0.4rem;
  }}
  .hero-title {{
      font-family: 'Syne', sans-serif;
      font-size: clamp(1.8rem, 4vw, 2.8rem);
      font-weight: 800;
      color: {C_TEXT};
      line-height: 1.1;
      margin-bottom: 0.3rem;
  }}
  .hero-title span {{ color: {C_AMBER_LT}; }}
  .hero-sub {{
      font-size: 0.95rem;
      color: {C_MUTED};
      font-weight: 300;
      margin-bottom: 1.5rem;
      max-width: 640px;
  }}

  .section-label {{
      font-family: 'DM Mono', monospace;
      font-size: 0.65rem;
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: {C_GREEN_LT};
      margin-bottom: 0.2rem;
  }}
  .section-title {{
      font-family: 'Syne', sans-serif;
      font-size: 1.2rem;
      font-weight: 700;
      color: {C_TEXT};
      border-bottom: 1px solid {C_BORDER};
      padding-bottom: 0.4rem;
      margin-bottom: 1rem;
  }}

  .kpi-card {{
      background: {C_SURFACE};
      border: 1px solid {C_BORDER};
      border-top: 2px solid {C_GREEN};
      border-radius: 6px;
      padding: 1rem 1.1rem 0.8rem;
      margin-bottom: 0.5rem;
  }}
  .kpi-card:hover {{ border-top-color: {C_AMBER}; transition: border-top-color 0.2s; }}
  .kpi-icon {{ font-size: 1.1rem; margin-bottom: 0.3rem; }}
  .kpi-label {{
      font-family: 'DM Mono', monospace;
      font-size: 0.62rem;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: {C_MUTED};
      margin-bottom: 0.15rem;
  }}
  .kpi-value {{
      font-family: 'Syne', sans-serif;
      font-size: 1.6rem;
      font-weight: 800;
      color: {C_AMBER_LT};
      line-height: 1;
  }}
  .kpi-sub {{
      font-size: 0.72rem;
      color: {C_MUTED};
      margin-top: 0.2rem;
  }}

  .insight-box {{
      background: rgba(82,183,136,0.07);
      border-left: 3px solid {C_GREEN_LT};
      border-radius: 0 6px 6px 0;
      padding: 0.75rem 1rem;
      margin: 0.8rem 0;
      font-size: 0.88rem;
      color: {C_TEXT};
  }}
  .insight-box b {{ color: {C_AMBER_LT}; }}

  .sidebar-title {{
      font-family: 'DM Mono', monospace;
      font-size: 0.65rem;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: {C_GREEN_LT};
      margin-bottom: 0.8rem;
  }}
</style>
""", unsafe_allow_html=True)

# ── Layout Plotly ────────────────────────────────────────────────────────────
LAYOUT = dict(
    plot_bgcolor="#111714",
    paper_bgcolor="#111714",
    font=dict(color=C_TEXT, family="DM Sans", size=11),
    title_font=dict(color=C_TEXT, family="Syne", size=13),
    legend=dict(font=dict(color=C_TEXT), bgcolor="rgba(0,0,0,0)"),
    xaxis=dict(
        tickfont=dict(color=C_MUTED),
        title_font=dict(color=C_MUTED),
        gridcolor=C_BORDER,
        linecolor=C_BORDER,
    ),
    yaxis=dict(
        tickfont=dict(color=C_MUTED),
        title_font=dict(color=C_MUTED),
        gridcolor=C_BORDER,
        linecolor=C_BORDER,
    ),
    margin=dict(t=40, b=30, l=10, r=10),
)

# ── Matplotlib tema escuro ───────────────────────────────────────────────────
matplotlib.rcParams.update({
    "figure.facecolor":  C_SURFACE,
    "axes.facecolor":    C_BG,
    "axes.edgecolor":    C_BORDER,
    "axes.labelcolor":   C_MUTED,
    "xtick.color":       C_MUTED,
    "ytick.color":       C_MUTED,
    "text.color":        C_TEXT,
    "grid.color":        C_BORDER,
    "grid.linewidth":    0.5,
})

# ── Dados ────────────────────────────────────────────────────────────────────
@st.cache_resource
def init_db(csv_path):
    os.makedirs("database", exist_ok=True)
    engine = create_engine("sqlite:///database/queimadas.db")
    df = pd.read_csv(csv_path, parse_dates=["data"])
    df.to_sql("queimadas", engine, if_exists="replace", index=False)
    return engine

@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path, parse_dates=["data"])
    df["mes_nome"] = df["data"].dt.month_name()
    df["trimestre"] = df["data"].dt.quarter.map({1:"T1",2:"T2",3:"T3",4:"T4"})
    return df

CSV_PATH = "dados/simulacao_queimadas_brasil.csv"
engine   = init_db(CSV_PATH)
df_raw   = load_data(CSV_PATH)

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sidebar-title">⬡ Parâmetros de Análise</div>', unsafe_allow_html=True)

    anos = sorted(df_raw["ano"].unique())
    ano_range = st.slider("Período", min_value=int(min(anos)), max_value=int(max(anos)),
                          value=(int(min(anos)), int(max(anos))))

    regioes = st.multiselect("Região", sorted(df_raw["regiao"].unique()),
                             default=sorted(df_raw["regiao"].unique()))

    biomas = st.multiselect("Bioma", sorted(df_raw["bioma"].unique()),
                            default=sorted(df_raw["bioma"].unique()))

    riscos = st.multiselect("Nível de Risco", ["Baixo", "Médio", "Alto", "Crítico"],
                            default=["Baixo", "Médio", "Alto", "Crítico"])

    st.markdown("---")
    st.markdown(f'<div style="font-size:0.75rem; color:{C_MUTED};">Fonte: Dados simulados — INPE<br>Disciplina: Análise e Visualização de Dados com Python</div>', unsafe_allow_html=True)

# ── Filtragem ────────────────────────────────────────────────────────────────
df = df_raw[
    (df_raw["ano"]        >= ano_range[0]) &
    (df_raw["ano"]        <= ano_range[1]) &
    (df_raw["regiao"].isin(regioes if regioes else df_raw["regiao"].unique())) &
    (df_raw["bioma"].isin(biomas  if biomas  else df_raw["bioma"].unique()))  &
    (df_raw["nivel_risco"].isin(riscos if riscos else df_raw["nivel_risco"].unique()))
].copy()

# ══════════════════════════════════════════════════════════
# CABEÇALHO
# ══════════════════════════════════════════════════════════
st.markdown('<div class="hero-tag">🛰️ Sistema de Monitoramento Ambiental · Brasil 2015–2024</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Painel de <span>Queimadas</span><br>no Brasil</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Análise exploratória de focos de incêndio, variáveis climáticas e distribuição de risco por bioma e região — dados INPE.</div>', unsafe_allow_html=True)

if df.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# ══════════════════════════════════════════════════════════
# SEÇÃO 1 — KPIs
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-label">01 — Indicadores</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Resumo do Período Selecionado</div>', unsafe_allow_html=True)

total_focos = int(df["focos_queimada"].sum())
total_area  = df["area_atingida_km2"].sum()
media_temp  = df["temperatura_media"].mean()
media_chuva = df["chuva_mm"].mean()
pct_critico = (df["nivel_risco"] == "Crítico").mean() * 100
media_seca  = df["indice_seca"].mean()

kpi_data = [
    ("🔥", "Focos Detectados",    f"{total_focos:,}",       f"{df['regiao'].nunique()} regiões"),
    ("🌍", "Área Atingida",       f"{total_area:,.0f} km²",  "área total afetada"),
    ("🌡️", "Temperatura Média",   f"{media_temp:.1f} °C",    "média do período"),
    ("🌧️", "Precipitação Média",  f"{media_chuva:.1f} mm",   "chuva acumulada"),
    ("⚠️", "Nível Crítico",       f"{pct_critico:.1f}%",     "dos registros"),
    ("🏜️", "Índice de Seca",      f"{media_seca:.2f}",       "escala 0–1"),
]

cols = st.columns(6)
for col, (icon, label, value, sub) in zip(cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 2 — Análise Temporal
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem">02 — Série Temporal</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Evolução e Sazonalidade dos Focos</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    focos_ano = df.groupby("ano")["focos_queimada"].sum().reset_index()
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=focos_ano["ano"], y=focos_ano["focos_queimada"],
        mode="lines+markers",
        line=dict(color=C_GREEN_LT, width=2.5),
        marker=dict(color=C_AMBER_LT, size=8, line=dict(color=C_BG, width=2)),
        fill="tozeroy",
        fillcolor=f"rgba(45,106,79,0.15)",
        name="Focos"
    ))
    fig_line.update_layout(**LAYOUT, title="Evolução Anual de Focos",
                           xaxis_title="Ano", yaxis_title="Total de Focos")
    st.plotly_chart(fig_line, use_container_width=True)

with col_b:
    focos_mes = df.groupby("mes")["focos_queimada"].mean().reset_index()
    meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    focos_mes["mes_nome"] = focos_mes["mes"].apply(lambda x: meses[x-1])
    cores_mes = [C_AMBER if v == focos_mes["focos_queimada"].max() else C_GREEN
                 for v in focos_mes["focos_queimada"]]
    fig_bar = go.Figure(go.Bar(
        x=focos_mes["mes_nome"], y=focos_mes["focos_queimada"],
        marker_color=cores_mes, marker_line_width=0,
    ))
    fig_bar.update_layout(**LAYOUT, title="Sazonalidade Mensal (média)",
                          xaxis_title="Mês", yaxis_title="Média de Focos")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown('<div class="insight-box">📡 <b>Padrão identificado:</b> Os meses de agosto a outubro concentram os picos históricos de queimadas, coincidindo com o período de estiagem nas regiões Norte e Centro-Oeste — o mês de maior média está destacado em âmbar.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 3 — Distribuição Espacial
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem">03 — Distribuição Espacial</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Focos e Área por Região e Bioma</div>', unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    focos_reg = df.groupby("regiao")["focos_queimada"].sum().reset_index().sort_values("focos_queimada")
    fig_hreg = go.Figure(go.Bar(
        x=focos_reg["focos_queimada"], y=focos_reg["regiao"],
        orientation="h",
        marker=dict(
            color=focos_reg["focos_queimada"],
            colorscale=[[0, C_GREEN], [0.5, C_GREEN_LT], [1, C_AMBER_LT]],
            showscale=False,
        ),
        text=focos_reg["focos_queimada"].apply(lambda x: f"{x:,}"),
        textposition="outside",
        textfont=dict(color=C_MUTED, size=10),
    ))
    fig_hreg.update_layout(**LAYOUT, title="Total de Focos por Região",
                           xaxis_title="Focos", yaxis_title="")
    st.plotly_chart(fig_hreg, use_container_width=True)

with col_d:
    area_bioma = df.groupby("bioma")["area_atingida_km2"].sum().reset_index()
    fig_pie = go.Figure(go.Pie(
        labels=area_bioma["bioma"],
        values=area_bioma["area_atingida_km2"],
        hole=0.45,
        marker=dict(colors=[C_GREEN, C_GREEN_LT, C_AMBER, C_AMBER_LT,
                             "#1B4332", "#D9A44E"],
                    line=dict(color=C_BG, width=2)),
        textfont=dict(color=C_TEXT, size=11),
        textinfo="percent+label",
    ))
    fig_pie.update_layout(**LAYOUT, title="Área Atingida por Bioma (km²)", showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 4 — Correlação Estatística
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem">04 — Correlação Estatística</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Relação entre Variáveis Climáticas e Focos</div>', unsafe_allow_html=True)

col_e, col_f = st.columns(2)

with col_e:
    numeric_cols = ["focos_queimada","temperatura_media","chuva_mm",
                    "area_atingida_km2","indice_seca","qualidade_ar"]
    labels_corr  = ["Focos","Temp.","Chuva","Área","Seca","Ar"]
    corr = df[numeric_cols].corr()
    fig_h, ax = plt.subplots(figsize=(6, 5))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "custom", [C_GREEN, C_BG, C_AMBER], N=256)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap,
                linewidths=1, linecolor=C_BG, ax=ax,
                annot_kws={"size": 9, "color": C_TEXT},
                xticklabels=labels_corr, yticklabels=labels_corr,
                vmin=-1, vmax=1)
    ax.set_title("Mapa de Correlação", fontsize=12, fontweight="bold",
                 color=C_TEXT, pad=12)
    plt.setp(ax.get_xticklabels(), color=C_MUTED, fontsize=9)
    plt.setp(ax.get_yticklabels(), color=C_MUTED, fontsize=9)
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color=C_MUTED)
    plt.setp(cbar.ax.get_yticklabels(), color=C_MUTED)
    plt.tight_layout()
    st.pyplot(fig_h)

with col_f:
    fig_sc = px.scatter(df, x="indice_seca", y="focos_queimada",
                        color="regiao", size="area_atingida_km2",
                        title="Índice de Seca × Focos",
                        labels={"indice_seca":"Índice de Seca","focos_queimada":"Focos"},
                        opacity=0.75, hover_data=["uf","bioma"],
                        color_discrete_sequence=[C_GREEN_LT, C_AMBER_LT,
                                                  "#74C69D", "#D9A44E", "#B7E4C7"])
    fig_sc.update_layout(**LAYOUT)
    st.plotly_chart(fig_sc, use_container_width=True)

st.markdown('<div class="insight-box">📡 <b>Correlação confirmada:</b> Índice de seca apresenta correlação positiva com número de focos. Precipitação (chuva) correlaciona negativamente com área atingida — secas prolongadas amplificam a propagação.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 5 — Nível de Risco
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem">05 — Classificação de Risco</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Distribuição e Concentração por Bioma</div>', unsafe_allow_html=True)

col_g, col_h = st.columns(2)
ordem_risco  = ["Baixo", "Médio", "Alto", "Crítico"]
cores_risco  = {"Baixo": "#2D6A4F", "Médio": "#74C69D", "Alto": C_AMBER, "Crítico": "#C44F1B"}

with col_g:
    risco_count = df["nivel_risco"].value_counts().reindex(ordem_risco).dropna().reset_index()
    risco_count.columns = ["nivel_risco", "count"]
    fig_risco = go.Figure(go.Bar(
        x=risco_count["nivel_risco"], y=risco_count["count"],
        marker_color=[cores_risco[r] for r in risco_count["nivel_risco"]],
        marker_line_width=0,
        text=risco_count["count"],
        textposition="outside",
        textfont=dict(color=C_MUTED, size=10),
    ))
    fig_risco.update_layout(**LAYOUT, title="Frequência por Nível de Risco",
                            xaxis_title="Nível", yaxis_title="Registros", showlegend=False)
    st.plotly_chart(fig_risco, use_container_width=True)

with col_h:
    pivot = df.groupby(["bioma","nivel_risco"]).size().unstack(fill_value=0)
    pivot = pivot.reindex(columns=ordem_risco, fill_value=0)
    fig_stack = go.Figure()
    for nivel in ordem_risco:
        if nivel in pivot.columns:
            fig_stack.add_trace(go.Bar(
                name=nivel, x=pivot.index, y=pivot[nivel],
                marker_color=cores_risco[nivel], marker_line_width=0,
            ))
    fig_stack.update_layout(**LAYOUT, barmode="stack",
                            title="Risco por Bioma (empilhado)",
                            xaxis_title="Bioma", yaxis_title="Registros",
                            legend=dict(font=dict(color=C_TEXT), orientation="h",
                                        yanchor="bottom", y=1.02))
    st.plotly_chart(fig_stack, use_container_width=True)

# ══════════════════════════════════════════════════════════
# SEÇÃO 6 — Tabela
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem">06 — Dados Brutos</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Registros Filtrados</div>', unsafe_allow_html=True)

colunas = ["ano","mes","regiao","uf","bioma","focos_queimada",
           "temperatura_media","chuva_mm","area_atingida_km2",
           "indice_seca","qualidade_ar","nivel_risco"]
st.dataframe(df[colunas].sort_values(["ano","mes"]).reset_index(drop=True),
             use_container_width=True, height=280)
st.caption(f"Exibindo {len(df):,} de {len(df_raw):,} registros totais.")

# ══════════════════════════════════════════════════════════
# SEÇÃO 7 — Conclusão
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-label" style="margin-top:1.5rem">07 — Conclusão</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Interpretação e Recomendações</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="color:{C_TEXT}; font-size:0.95rem; line-height:1.8; max-width:860px;">
O painel analisou <b style="color:{C_AMBER_LT}">{len(df):,} registros</b> entre
<b style="color:{C_AMBER_LT}">{df["ano"].min()} e {df["ano"].max()}</b>,
cobrindo <b style="color:{C_GREEN_LT}">{df["regiao"].nunique()} regiões</b>,
<b style="color:{C_GREEN_LT}">{df["bioma"].nunique()} biomas</b> e
<b style="color:{C_GREEN_LT}">{df["uf"].nunique()} estados</b>.
<br><br>
<b style="color:{C_AMBER_LT}">Principais achados:</b><br>
• A região <b>Norte</b> concentra o maior volume de focos, com destaque para PA e AM.<br>
• <b>Cerrado</b> e <b>Amazônia</b> lideram em área atingida por queimadas.<br>
• O <b>índice de seca</b> é o principal preditor do número de focos — correlação positiva confirmada.<br>
• O período <b>agosto–outubro</b> representa a janela crítica de risco em todas as regiões.<br>
• Eventos <b>Críticos</b> representam <b style="color:{C_AMBER_LT}">{pct_critico:.1f}%</b> dos registros, mas com impacto desproporcional na área destruída.
<br><br>
<b style="color:{C_AMBER_LT}">Recomendação:</b> Implementar sistemas de alerta precoce integrados ao índice de seca e temperatura média,
com ativação prioritária nas regiões Norte e Centro-Oeste entre julho e outubro.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
