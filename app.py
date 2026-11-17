# -*- coding: utf-8 -*-
"""
MAPA ENERGÉTICO DA COMUNIDADE
Jogo educativo de consumo residencial de energia elétrica.
Projeto de extensão | Engenharia de Energia – IFBA, Campus Lauro de Freitas

Execução:
    pip install -r requirements.txt
    streamlit run app.py
"""

from __future__ import annotations

import html
import math
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------
# CONFIGURAÇÃO E IDENTIDADE VISUAL
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Mapa Energético da Comunidade",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)
GREEN_DARK = "#123D2B"
GREEN = "#42D9E8"
GREEN_LIGHT = "#E7F5EC"
MINT = "#F1F5F9"
GOLD = "#FFD166"
TEXT = "#20352A"
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');
    :root {{ --dark:{GREEN_DARK}; --green:{GREEN}; --pale:{GREEN_LIGHT}; --gold:{GOLD}; }}
    html, body, [class*="css"] {{ font-family:'DM Sans',sans-serif; color:{TEXT}; }}
    .stApp {{ background:linear-gradient(180deg,#F7FBF8 0%,#F2F8F4 100%); }}
    [data-testid="stHeader"] {{ background:rgba(247,251,248,.88); }}
    .block-container {{ padding-top:1.2rem; padding-bottom:3rem; max-width:1200px; }}
    h1,h2,h3 {{ font-family:'Manrope','DM Sans',sans-serif; }}
    .hero {{
      background:linear-gradient(125deg,#103B29 0%,#176B45 58%,#1A9860 100%);
      border-radius:26px; padding:30px 32px; color:white; position:relative;
      overflow:hidden; box-shadow:0 14px 36px rgba(18,61,43,.16);
    }}
    .hero:after {{ content:'⚡'; position:absolute; right:6%; top:-25px; font-size:150px; opacity:.10; }}
    .hero h1 {{ color:white; font-size:clamp(1.8rem,4vw,3rem); line-height:1.08; margin:8px 0 12px; }}
    .hero p {{ color:#E5F5EA; font-size:1.05rem; max-width:720px; }}
    .eyebrow {{ color:#D9F5E3; font-size:.78rem; font-weight:800; letter-spacing:.13em; text-transform:uppercase; }}
    .pill {{ display:inline-block; border:1px solid rgba(255,255,255,.3); color:#fff; border-radius:99px; padding:6px 12px; font-size:.78rem; }}
    .phasebar {{ display:flex; gap:8px; flex-wrap:wrap; margin:18px 0 22px; }}
    .phase {{ background:white; border:1px solid #DDEBE1; color:#567061; padding:9px 13px; border-radius:99px; font-size:.82rem; font-weight:700; }}
    .phase.active {{ background:{GREEN_DARK}; color:white; border-color:{GREEN_DARK}; }}
    .phase.done {{ background:{GREEN_LIGHT}; color:{GREEN_DARK}; border-color:#B8DEC5; }}
    .panel {{ background:white; border:1px solid #E2EEE5; border-radius:20px; padding:18px 20px; box-shadow:0 5px 18px rgba(20,70,42,.045); }}
    .equip-card {{ background:white; border:1px solid #E1ECE4; border-radius:18px; padding:15px; min-height:118px; }}
    .equip-icon {{ font-size:1.75rem; }}
    .equip-name {{ font-weight:800; color:{GREEN_DARK}; margin-top:5px; }}
    .muted {{ color:#6C8073; font-size:.88rem; }}
    .metric {{ background:white; border:1px solid #E2EEE5; border-radius:18px; padding:17px; min-height:120px; }}
    .metric-label {{ color:#6C8073; font-size:.82rem; font-weight:700; }}
    .metric-value {{ color:{GREEN_DARK}; font-size:1.75rem; font-weight:800; margin-top:5px; }}
    .metric-note {{ color:#718477; font-size:.78rem; margin-top:2px; }}
    .tip {{ background:#F0F8F2; border-left:4px solid {GREEN}; border-radius:12px; padding:13px 15px; margin:9px 0; }}
    .gold-tip {{ background:#FFF9E7; border-left:4px solid {GOLD}; border-radius:12px; padding:13px 15px; margin:9px 0; }}
    .gold-tip, .gold-tip b {{
        color: #20352A !important;
    }}

    .equip-card .equip-name {{
        color: #123D2B !important;
    }}

    .equip-card .muted {{
        color: #52665A !important;
    }}

    .stMarkdown h2,
    .stMarkdown h3 {{
        color: #123D2B !important;
    }}

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] p,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stCaptionContainer"] p,
    [data-testid="stAlert"] p {{
        color: #20352A !important;
    }}
    .medal {{ background:linear-gradient(135deg,#F1FAF3,#FFFFFF); border:1px solid #D7EBDD; border-radius:20px; padding:22px; text-align:center; }}
    div.stButton > button {{ border-radius:13px; font-weight:800; min-height:2.8rem; border:1px solid #D5E6DA; }}
    div.stButton > button[kind="primary"] {{ background:{GREEN}; border-color:{GREEN}; color:white; }}
    div.stButton > button[kind="primary"]:hover {{ background:{GREEN_DARK}; border-color:{GREEN_DARK}; }}
    div[data-testid="stMetric"] {{ background:white; border:1px solid #E2EEE5; padding:14px; border-radius:16px; }}
    [data-testid="stProgressBar"] > div > div {{ background:{GREEN}; }}
    .footer {{ color:#7C8E82; font-size:.78rem; text-align:center; padding:22px 0 5px; }}
    @media(max-width:640px) {{
      .block-container {{ padding-left:1rem; padding-right:1rem; }}
      .hero {{ padding:23px 20px; border-radius:20px; }}
      .metric-value {{ font-size:1.45rem; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# CATÁLOGO EDITÁVEL DE EQUIPAMENTOS
# Potências e rotinas são exemplos didáticos, não especificações universais.
# ---------------------------------------------------------------------
CATALOGO: dict[str, dict[str, Any]] = {
    "Geladeira": {"icon": "🧊", "potencia": 150, "horas": 8, "dias": 30, "tipo": "horas", "dica": "Confira a vedação, evite abrir a porta sem necessidade e não coloque alimentos ainda quentes. O consumo real depende muito do modelo e do ciclo do compressor."},
    "Chuveiro elétrico": {"icon": "🚿", "potencia": 5500, "horas": 0.35, "dias": 30, "tipo": "horas", "dica": "Reduzir alguns minutos do banho pode fazer diferença. Use uma temperatura confortável e segura, sem mexer na instalação elétrica."},
    "Ar-condicionado": {"icon": "❄️", "potencia": 1200, "horas": 6, "dias": 25, "tipo": "horas", "dica": "Mantenha filtros limpos, portas e janelas fechadas durante o uso e escolha uma temperatura confortável. Consulte o consumo informado na etiqueta."},
    "Ventilador": {"icon": "🌀", "potencia": 100, "horas": 8, "dias": 25, "tipo": "horas", "dica": "Desligue quando o ambiente estiver vazio e mantenha hélices e grades limpas."},
    "Televisão": {"icon": "📺", "potencia": 100, "horas": 5, "dias": 30, "tipo": "horas", "dica": "Ative o desligamento automático e evite deixar a TV ligada como som ambiente quando ninguém estiver assistindo."},
    "Lâmpadas LED": {"icon": "💡", "potencia": 9, "horas": 5, "dias": 30, "tipo": "horas", "dica": "Apague as luzes de cômodos vazios e aproveite a iluminação natural sempre que possível."},
    "Micro-ondas": {"icon": "🍲", "potencia": 1400, "horas": 0.25, "dias": 20, "tipo": "horas", "dica": "Use o tempo adequado para cada alimento e evite abrir a porta repetidamente durante o funcionamento."},
    "Máquina de lavar": {"icon": "🧺", "potencia": 500, "horas": 1, "dias": 12, "tipo": "ciclos", "dica": "Planeje as lavagens com a capacidade adequada, sem sobrecarregar o equipamento, e evite ciclos desnecessários."},
    "Ferro de passar": {"icon": "👕", "potencia": 1000, "horas": 1, "dias": 4, "tipo": "horas", "dica": "Separe as roupas e passe peças semelhantes em sequência, aproveitando o aquecimento do ferro."},
    "Secador de cabelo": {"icon": "💨", "potencia": 1600, "horas": 0.15, "dias": 20, "tipo": "horas", "dica": "Use pelo tempo necessário e, quando possível, retire o excesso de água com uma toalha antes."},
    "Computador/notebook": {"icon": "💻", "potencia": 120, "horas": 6, "dias": 22, "tipo": "horas", "dica": "Configure suspensão automática, reduza o brilho quando adequado e desligue o equipamento ao terminar."},
    "Outros equipamentos": {"icon": "🔌", "potencia": 300, "horas": 1, "dias": 15, "tipo": "horas", "dica": "Confira a potência na etiqueta ou no manual e registre cada equipamento separadamente para melhorar a estimativa."},
}

DICAS_GERAIS = [
    "Compare a potência e o consumo de modelos usando a Etiqueta Nacional de Conservação de Energia (ENCE).",
    "A economia depende do tempo real de uso, da potência, do estado de conservação e da eficiência de cada aparelho.",
    "Desligar equipamentos quando não estão em uso pode ajudar, mas alguns aparelhos precisam permanecer ligados, como a geladeira.",
]

FASES = [
    "🏠 Monte sua casa",
    "⚡ Descubra seu consumo",
    "🎯 Desafios de economia",
    "📊 Veja sua economia",
    "🏅 Conquiste sua medalha",
]

# ---------------------------------------------------------------------
# ESTADO DA SESSÃO
# ---------------------------------------------------------------------
def inicializar_estado() -> None:
    defaults = {
        "fase": 0,
        "jogo_iniciado": False,
        "equipamentos": {},
        "tarifa": 0.85,
        "reducoes": {},
        "resultado_calculado": False,
    }
    for chave, valor in defaults.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


inicializar_estado()


def consumo_mensal_kwh(potencia_w: float, horas_por_dia: float, dias_por_mes: float,
                       quantidade: int = 1, ciclos_por_semana: float | None = None) -> float:
    """Calcula energia mensal em kWh a partir de potência e tempo de uso."""
    if ciclos_por_semana is not None:
        horas_mes = ciclos_por_semana * (52.0 / 12.0) * horas_por_dia
    else:
        horas_mes = horas_por_dia * dias_por_mes
    return max(0.0, potencia_w * horas_mes * quantidade / 1000.0)


def calcular_consumo_item(nome: str, dados: dict[str, Any]) -> float:
    if dados["tipo"] == "ciclos":
        return consumo_mensal_kwh(
            dados["potencia"], dados["horas"], dados["dias"],
            dados["quantidade"], ciclos_por_semana=dados["dias"]
        )
    return consumo_mensal_kwh(
        dados["potencia"], dados["horas"], dados["dias"], dados["quantidade"]
    )


def obter_dataframe(reduzido: bool = False) -> pd.DataFrame:
    linhas = []
    for nome, dados in st.session_state.equipamentos.items():
        original = calcular_consumo_item(nome, dados)
        reducao = float(st.session_state.reducoes.get(nome, 0)) if reduzido else 0.0
        final = original * (1 - reducao / 100)
        linhas.append({
            "Equipamento": nome,
            "Consumo inicial (kWh)": original,
            "Redução (%)": reducao,
            "Consumo após desafio (kWh)": final,
            "Economia (kWh)": original - final,
        })
    return pd.DataFrame(linhas)


def dinheiro(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def navegar(delta: int) -> None:
    st.session_state.fase = min(4, max(0, st.session_state.fase + delta))


def card_metrica(rotulo: str, valor: str, nota: str = "", icone: str = "✦") -> None:
    st.markdown(
        f"""<div class="metric"><div class="metric-label">{icone} &nbsp;{html.escape(rotulo)}</div>
        <div class="metric-value">{html.escape(valor)}</div>
        <div class="metric-note">{html.escape(nota)}</div></div>""",
        unsafe_allow_html=True,
    )


def mostrar_cabecalho() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">Projeto de extensão • IFBA</div>
          <h1>MAPA ENERGÉTICO<br>DA COMUNIDADE</h1>
          <p>Descubra como seus hábitos influenciam o consumo de energia elétrica
          e aprenda a economizar de forma consciente.</p>
          <span class="pill">🌱 Engenharia de Energia · Campus Lauro de Freitas</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_progresso() -> None:
    atual = st.session_state.fase
    html_fases = []
    for i, nome in enumerate(FASES):
        classe = "active" if i == atual else ("done" if i < atual else "")
        html_fases.append(f'<span class="phase {classe}">{i+1}. {nome}</span>')
    st.markdown('<div class="phasebar">' + "".join(html_fases) + "</div>", unsafe_allow_html=True)
    st.progress((atual + 1) / len(FASES), text=f"Fase {atual + 1} de 5")
    st.markdown("""
    <style>
    [data-testid="stProgress"] p {
        color: #20352A !important;
    }
    </style>
    """, unsafe_allow_html=True)


def botoes_navegacao(voltar: bool = True, avancar: bool = True, texto_avancar: str = "Continuar →") -> None:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if voltar and st.button("← Voltar", use_container_width=True, key=f"voltar_{st.session_state.fase}"):
            navegar(-1)
            st.rerun()
    with c3:
        if avancar and st.button(texto_avancar, type="primary", use_container_width=True, key=f"avancar_{st.session_state.fase}"):
            navegar(1)
            st.rerun()


def validar_casa() -> bool:
    if not st.session_state.equipamentos:
        st.warning("Selecione pelo menos um equipamento para continuar.")
        return False
    return True

def mostrar_cabecalho() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">Projeto de extensão • IFBA</div>
          <h1>MAPA ENERGÉTICO<br>DA COMUNIDADE</h1>
          <p>Descubra como seus hábitos influenciam o consumo de energia elétrica
          e aprenda a economizar de forma consciente.</p>
          <span class="pill">🌱 Engenharia de Energia · Campus Lauro de Freitas</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
# ---------------------------------------------------------------------
# TELA INICIAL
# ---------------------------------------------------------------------
def tela_inicial() -> None:
    mostrar_cabecalho()
    st.write("")
    left, right = st.columns([1.15, 0.85], vertical_alignment="center")
    with left:
        st.markdown(
            '<h2 style="color:#123D2B;">Sua casa, suas escolhas, sua energia.</h2>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color:#20352A;">Neste jogo, você vai montar uma residência, '
            'estimar o consumo dos aparelhos e testar atitudes que podem reduzir '
            'o gasto mensal. Cada decisão revela um pouco mais sobre o uso consciente '
            'da eletricidade.</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="tip" style="color:#123D2B;">'
            '<b style="color:#123D2B;">🎮 Como funciona?</b><br>'
            'Monte sua casa → descubra o consumo → aceite desafios → '
            'compare os resultados → conquiste sua medalha.</div>',
            unsafe_allow_html=True,
        )
        if st.button("🚀 COMEÇAR JOGO", type="primary", use_container_width=True):
            st.session_state.jogo_iniciado = True
            st.session_state.fase = 0
            st.rerun()
    with right:
        st.markdown(
            """
            <div class="panel" style="text-align:center;background:linear-gradient(160deg,#E8F7ED,#FFFFFF);">
              <div style="font-size:5rem;line-height:1.2">🏡</div>
              <div style="font-size:2rem">☀️ &nbsp; 💡 &nbsp; ⚡</div>
              <h3 style="color:#123D2B;margin-bottom:4px">Casa mais consciente</h3>
              <p class="muted">Pequenas mudanças de hábito podem gerar grandes aprendizados.</p>
              <div style="font-size:2rem">🌳 🌿 🌎</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.write("")
    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="panel"><h3>🔎 Descobrir</h3><p class="muted">Entenda quais aparelhos participam mais do consumo residencial.</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="panel"><h3>💚 Aprender</h3><p class="muted">Experimente hábitos mais eficientes com desafios interativos.</p></div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="panel"><h3>🏆 Conquistar</h3><p class="muted">Receba uma medalha de acordo com a economia simulada.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">Projeto de Extensão · Engenharia de Energia · IFBA – Campus Lauro de Freitas</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------
# FASE 1 — MONTAGEM DA CASA
# ---------------------------------------------------------------------
def fase_montar_casa() -> None:
    st.markdown("## 🏠 FASE 1 — MONTE SUA CASA")
    st.markdown(
    '<p style="color:#20352A;">Escolha os equipamentos que existem na residência. Depois, personalize os dados de uso.</p>',
    unsafe_allow_html=True,
)
    st.markdown('<div class="gold-tip">💡 <b>Missão:</b> monte uma casa que represente a realidade. Os valores iniciais são ilustrativos e podem ser editados.</div>', unsafe_allow_html=True)

    nomes = list(CATALOGO.keys())
    for inicio in range(0, len(nomes), 3):
        cols = st.columns(3)
        for col, nome in zip(cols, nomes[inicio:inicio+3]):
            info = CATALOGO[nome]
            with col:
                selecionado = nome in st.session_state.equipamentos
                st.markdown(
                    f'<div class="equip-card"><div class="equip-icon">{info["icon"]}</div>'
                    f'<div class="equip-name">{html.escape(nome)}</div>'
                    f'<div class="muted">Potência ilustrativa: {info["potencia"]} W</div></div>',
                    unsafe_allow_html=True,
                )
                novo = st.checkbox("Adicionar à casa", value=selecionado, key=f"sel_{nome}")
                if novo and nome not in st.session_state.equipamentos:
                    st.session_state.equipamentos[nome] = {
                        "quantidade": 1, "potencia": float(info["potencia"]),
                        "horas": float(info["horas"]), "dias": float(info["dias"]),
                        "tipo": info["tipo"],
                    }
                elif not novo and nome in st.session_state.equipamentos:
                    del st.session_state.equipamentos[nome]
                    st.session_state.reducoes.pop(nome, None)

    if st.session_state.equipamentos:
        st.divider()
        st.markdown("### 🛠️ Personalize os equipamentos da sua casa")
        for idx, (nome, dados) in enumerate(list(st.session_state.equipamentos.items())):
            info = CATALOGO[nome]
            with st.expander(f'{info["icon"]} {nome} · editar dados', expanded=(idx == 0)):
                c1, c2, c3 = st.columns(3)
                with c1:
                    dados["quantidade"] = int(st.number_input("Quantidade", min_value=1, max_value=30, value=int(dados["quantidade"]), step=1, key=f"q_{nome}"))
                    dados["potencia"] = float(st.number_input("Potência (W)", min_value=0.1, max_value=30000.0, value=float(dados["potencia"]), step=10.0, key=f"p_{nome}"))
                with c2:
                    if dados["tipo"] == "ciclos":
                        dados["horas"] = float(st.number_input("Duração de cada ciclo (h)", min_value=0.01, max_value=24.0, value=float(dados["horas"]), step=0.25, key=f"h_{nome}"))
                        dados["dias"] = float(st.number_input("Ciclos por semana", min_value=0.0, max_value=50.0, value=float(dados["dias"]), step=1.0, key=f"d_{nome}"))
                    else:
                        dados["horas"] = float(st.number_input("Horas de uso por dia", min_value=0.0, max_value=24.0, value=float(dados["horas"]), step=0.25, key=f"h_{nome}"))
                        dados["dias"] = float(st.number_input("Dias de uso por mês", min_value=0.0, max_value=31.0, value=float(dados["dias"]), step=1.0, key=f"d_{nome}"))
                with c3:
                    estimativa = calcular_consumo_item(nome, dados)
                    st.metric("Consumo mensal estimado", f"{estimativa:.2f} kWh")
                    if st.button("Remover aparelho", key=f"rem_{nome}"):
                        del st.session_state.equipamentos[nome]
                        st.session_state.reducoes.pop(nome, None)
                        st.rerun()
                if nome == "Geladeira":
                    st.caption("Para a geladeira, o valor de horas/dia é uma aproximação didática do funcionamento equivalente. Prefira o consumo mensal em kWh informado na etiqueta/manual para uma estimativa específica.")
        st.markdown(
    f'<div style="background:#123D2B; color:white; padding:13px 15px; border-radius:12px;">🏡 Sua casa tem <b>{len(st.session_state.equipamentos)} tipos de equipamentos</b> selecionados.</div>',
    unsafe_allow_html=True,
)
    else:
        st.markdown(
            '<div style="background:#123D2B; color:white; padding:13px 15px; border-radius:12px;">'
            '🏡 Sua casa ainda está vazia. Selecione os cartões acima para adicionar aparelhos.'
            '</div>',
            unsafe_allow_html=True,
            )

    st.divider()
    with st.expander("💰 Configurar tarifa de energia usada na simulação"):
        st.number_input(
            "Tarifa simplificada (R$/kWh)", min_value=0.01, max_value=5.0,
            step=0.01, key="tarifa",
            help="Informe um valor aproximado ou consulte a tarifa homologada da distribuidora. Não inclui tributos, iluminação pública e outros itens da fatura.",
        )
        st.caption("A tarifa é editável. O valor padrão é apenas ilustrativo, não representa uma tarifa oficial vigente.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Início", use_container_width=True):
            st.session_state.jogo_iniciado = False
            st.rerun()
    with c2:
        if st.button("Descobrir meu consumo →", type="primary", use_container_width=True):
            if validar_casa():
                st.session_state.fase = 1
                st.rerun()


# ---------------------------------------------------------------------
# FASE 2 — CONSUMO
# ---------------------------------------------------------------------
def fase_consumo() -> None:
    st.markdown("## ⚡ FASE 2 — DESCUBRA SEU CONSUMO")
    df = obter_dataframe()
    if df.empty:
        st.warning("Adicione equipamentos na Fase 1 antes de continuar.")
        if st.button("Voltar para montar a casa"):
            st.session_state.fase = 0
            st.rerun()
        return
    total = float(df["Consumo inicial (kWh)"].sum())
    custo = total * float(st.session_state.tarifa)
    maior = df.sort_values("Consumo inicial (kWh)", ascending=False).iloc[0]

    cols = st.columns(3)
    with cols[0]: card_metrica("Consumo mensal", f"{total:.1f} kWh", "Estimativa da residência", "⚡")
    with cols[1]: card_metrica("Custo mensal", dinheiro(custo), "Tarifa simplificada informada", "💳")
    with cols[2]: card_metrica("Maior consumidor", str(maior["Equipamento"]), f'{maior["Consumo inicial (kWh)"]:.1f} kWh/mês', "🔎")

    st.write("")
    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown("### 📊 Consumo por equipamento")
        fig = px.bar(df.sort_values("Consumo inicial (kWh)", ascending=True),
                     x="Consumo inicial (kWh)", y="Equipamento", orientation="h",
                     color="Consumo inicial (kWh)", color_continuous_scale=["#BFE8CC", "#15945A"])
        fig.update_layout(height=390, margin=dict(l=5,r=5,t=10,b=5), coloraxis_showscale=False,
                          xaxis_title="Consumo mensal (kWh)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("### 🧩 Participação no consumo")
        pie = px.pie(df, values="Consumo inicial (kWh)", names="Equipamento", hole=.58,
                     color_discrete_sequence=["#15945A","#F4C542","#6BBF8A","#80B7A0","#2D6A4F","#A8DDB8","#E4B84A"])
        pie.update_layout(height=390, margin=dict(l=0,r=0,t=10,b=5), legend=dict(font=dict(size=10)))
        st.plotly_chart(pie, use_container_width=True)

    st.markdown("### 🏅 Ranking dos equipamentos")
    rank = df.sort_values("Consumo inicial (kWh)", ascending=False).reset_index(drop=True)
    rank.insert(0, "Posição", [f"{i+1}º" for i in range(len(rank))])
    st.dataframe(rank[["Posição","Equipamento","Consumo inicial (kWh)"]].style.format({"Consumo inicial (kWh)": "{:.2f}"}), use_container_width=True, hide_index=True)
    st.markdown('<div class="gold-tip">Atenção: o consumo estimado depende da potência e do tempo de uso informados. Para equipamentos com ciclos automáticos ou funcionamento intermitente, a potência nominal multiplicada pelo tempo pode ser uma aproximação. Use o consumo da etiqueta/manual quando disponível.</div>', unsafe_allow_html=True)
    botoes_navegacao()


# ---------------------------------------------------------------------
# FASE 3 — DESAFIOS
# ---------------------------------------------------------------------
def fase_desafios() -> None:
    st.markdown("## 🎯 FASE 3 — DESAFIOS DE ECONOMIA")
    st.markdown(
        '<p style="color:#20352A;">Escolha mudanças realistas de hábito. Os controles simulam a redução do consumo de cada equipamento.</p>',
        unsafe_allow_html=True,
    )
    df = obter_dataframe()
    if df.empty:
        st.warning("Volte à Fase 1 e monte sua casa.")
        return

    desafios = {
        "Geladeira": "Ajustar hábitos de abertura da porta e cuidar da vedação",
        "Chuveiro elétrico": "Reduzir o tempo de banho",
        "Ar-condicionado": "Reduzir o tempo de funcionamento",
        "Ventilador": "Desligar quando o ambiente estiver vazio",
        "Televisão": "Evitar deixar ligada sem ninguém assistindo",
        "Lâmpadas LED": "Apagar luzes em ambientes desocupados",
        "Micro-ondas": "Evitar funcionamento desnecessário",
        "Máquina de lavar": "Planejar melhor os ciclos de lavagem",
        "Ferro de passar": "Agrupar roupas para passar de uma só vez",
        "Secador de cabelo": "Usar pelo tempo necessário",
        "Computador/notebook": "Ativar suspensão e desligar ao terminar",
        "Outros equipamentos": "Rever o tempo de uso do equipamento",
    }
    st.markdown(
        '<div class="tip" style="color:#20352A;">🌱 <b>Regra do jogo:</b> escolha reduções que seriam possíveis na rotina da residência. Não é necessário reduzir todos os aparelhos.</div>',
        unsafe_allow_html=True,
    )

    for nome, dados in st.session_state.equipamentos.items():
        atual = int(st.session_state.reducoes.get(nome, 0))
        c1, c2 = st.columns([1.1, 2.2])

        with c1:
            st.markdown(
                f'<p style="color:#20352A; font-weight:bold;">{CATALOGO[nome]["icon"]} {html.escape(nome)}</p>',
                unsafe_allow_html=True,
            )
            st.caption(f"{calcular_consumo_item(nome, dados):.2f} kWh/mês antes do desafio")

        with c2:
            reducao = st.slider(
                desafios.get(nome, "Reduzir o uso"),
                min_value=0, max_value=80, value=atual, step=5,
                key=f"reducao_{nome}",
                help="Percentual simulado de redução do consumo mensal deste equipamento.",
            )
            st.session_state.reducoes[nome] = reducao
            st.progress(reducao / 100, text=f"Redução escolhida: {reducao}%")

        st.divider()

    df_final = obter_dataframe(reduzido=True)
    economia = float(df_final["Economia (kWh)"].sum())
    economia_reais = economia * float(st.session_state.tarifa)
    st.markdown("### ✨ Prévia da sua missão")
    a,b,c = st.columns(3)
    with a: card_metrica("Energia economizada", f"{economia:.2f} kWh", "Por mês", "🌿")
    with b: card_metrica("Dinheiro economizado", dinheiro(economia_reais), "Por mês, na simulação", "💚")
    with c: card_metrica("Desafios ativados", str(sum(v > 0 for v in st.session_state.reducoes.values())), "Equipamentos com mudança", "🎯")
    botoes_navegacao()


# ---------------------------------------------------------------------
# FASE 4 — COMPARAÇÃO E DASHBOARD
# ---------------------------------------------------------------------
def fase_resultados() -> None:
    st.markdown("## 📊 FASE 4 — VEJA SUA ECONOMIA")
    antes_df = obter_dataframe()
    depois_df = obter_dataframe(reduzido=True)
    if antes_df.empty:
        st.warning("Monte sua casa para visualizar os resultados.")
        return

    antes = float(antes_df["Consumo inicial (kWh)"].sum())
    depois = float(depois_df["Consumo após desafio (kWh)"].sum())
    economia = max(0.0, antes - depois)
    tarifa = float(st.session_state.tarifa)
    custo_antes = antes * tarifa
    custo_depois = depois * tarifa
    economia_reais = economia * tarifa
    percentual = (economia / antes * 100) if antes > 0 else 0.0
    economia_anual = economia_reais * 12
    pontuacao = int(round(min(100.0, percentual * 2.0)))

    st.markdown(
        '<div class="tip" style="color:#20352A;">🏁 Compare o cenário original com o cenário após suas escolhas. A projeção anual considera que a mesma economia mensal se repetiria por 12 meses.</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    with cols[0]: card_metrica("Consumo antes", f"{antes:.1f} kWh", "Por mês", "⚡")
    with cols[1]: card_metrica("Consumo depois", f"{depois:.1f} kWh", "Por mês", "🌱")
    with cols[2]: card_metrica("Economia mensal", f"{economia:.1f} kWh", dinheiro(economia_reais), "💚")
    with cols[3]: card_metrica("Redução", f"{percentual:.1f}%", f"Pontuação: {pontuacao}/100", "🏆")

    st.write("")
    a,b = st.columns(2)
    with a:
        st.markdown("### 💡 Comparação do consumo")
        comp = pd.DataFrame({"Cenário":["Antes das mudanças","Depois das mudanças"],
                             "Consumo (kWh/mês)":[antes,depois]})
        fig = px.bar(comp, x="Cenário", y="Consumo (kWh/mês)", color="Cenário",
                     color_discrete_sequence=["#A8B8AD", GREEN])
        fig.update_layout(showlegend=False, height=330, margin=dict(l=5,r=5,t=15,b=5))
        st.plotly_chart(fig, use_container_width=True)
    with b:
        st.markdown("### 💰 Comparação do custo estimado")
        comp_custo = pd.DataFrame({"Cenário":["Antes das mudanças","Depois das mudanças"],
                                   "Custo (R$)":[custo_antes,custo_depois]})
        fig2 = px.bar(comp_custo, x="Cenário", y="Custo (R$)", color="Cenário",
                      color_discrete_sequence=["#E8C75A", GREEN])
        fig2.update_layout(showlegend=False, height=330, margin=dict(l=5,r=5,t=15,b=5))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📈 Seu impacto em 12 meses")
    x,y,z = st.columns(3)
    with x: card_metrica("Economia mensal", dinheiro(economia_reais), "Estimativa", "💵")
    with y: card_metrica("Economia anual", dinheiro(economia_anual), "Projeção por 12 meses", "📅")
    with z: card_metrica("Energia poupada no ano", f"{economia*12:.1f} kWh", "Projeção por 12 meses", "🌎")

    tabela = depois_df[["Equipamento","Consumo inicial (kWh)","Consumo após desafio (kWh)","Economia (kWh)"]].copy()
    st.markdown("### 🔍 Detalhamento por equipamento")
    st.dataframe(tabela.style.format({
        "Consumo inicial (kWh)": "{:.2f}",
        "Consumo após desafio (kWh)": "{:.2f}",
        "Economia (kWh)": "{:.2f}",
    }), use_container_width=True, hide_index=True)
    csv = tabela.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ Baixar meus resultados (CSV)", data=csv,
                       file_name="mapa_energetico_resultados.csv", mime="text/csv")
    botoes_navegacao()


# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# FASE 5 — CONQUISTAS
# ---------------------------------------------------------------------
def fase_medalha() -> None:
    st.markdown("## 🏅 FASE 5 — CONQUISTE SUA MEDALHA")

    antes_df = obter_dataframe()
    depois_df = obter_dataframe(reduzido=True)

    antes = float(antes_df["Consumo inicial (kWh)"].sum()) if not antes_df.empty else 0.0
    depois = float(depois_df["Consumo após desafio (kWh)"].sum()) if not depois_df.empty else 0.0

    economia = max(0.0, antes - depois)
    percentual = (economia / antes * 100) if antes > 0 else 0.0
    pontos = int(round(min(100.0, percentual * 2.0)))

    if percentual >= 30:
        medalha = "🌎"
        titulo = "Herói da Sustentabilidade"
        descricao = "Sua simulação alcançou uma redução de pelo menos 30% do consumo inicial."
    elif percentual >= 20:
        medalha = "⚡"
        titulo = "Mestre da Economia"
        descricao = "Você alcançou uma redução de pelo menos 20% do consumo inicial."
    elif percentual >= 10:
        medalha = "💡"
        titulo = "Guardião da Energia"
        descricao = "Você alcançou uma redução de pelo menos 10% do consumo inicial."
    else:
        medalha = "🌱"
        titulo = "Iniciante Sustentável"
        descricao = "Você concluiu o mapa e começou a identificar oportunidades de economia. Continue testando hábitos possíveis."

    st.markdown(
        f"""<div class="medal">
        <div style="font-size:5rem">{medalha}</div>
        <div style="color:#20352A;font-weight:800;letter-spacing:.12em;font-size:.78rem">SUA CONQUISTA</div>
        <h1 style="color:#20352A;margin:8px 0">{titulo}</h1>
        <p style="color:#20352A">{descricao}</p>
        </div>""",
        unsafe_allow_html=True,
    )

    st.write("")

    a, b, c = st.columns(3)

    with a:
        card_metrica("Pontuação", f"{pontos}/100", "Pontuação proporcional à redução", "🏆")

    with b:
        card_metrica("Redução alcançada", f"{percentual:.1f}%", "Consumo mensal", "📉")

    with c:
        card_metrica("Energia economizada", f"{economia:.2f} kWh", "Por mês", "🌿")

    st.progress(pontos / 100, text=f"Pontuação final: {pontos} de 100")

    st.markdown("### 🎖️ Como funcionam as conquistas?")

    niveis = [
        ("🌱 Iniciante Sustentável", "Menos de 10% de redução ou nenhuma redução simulada."),
        ("💡 Guardião da Energia", "De 10% a menos de 20% de redução."),
        ("⚡ Mestre da Economia", "De 20% a menos de 30% de redução."),
        ("🌎 Herói da Sustentabilidade", "30% ou mais de redução."),
    ]

    for nome, regra in niveis:
        ativo = nome.endswith(titulo)
        classe = "tip" if ativo else "panel"
        status = '<span style="color:#15945A;font-weight:800"> · CONQUISTADA</span>' if ativo else ""


    st.markdown("### 💚 Dicas personalizadas para sua residência")

    for nome in st.session_state.equipamentos:
        st.markdown(
            f'<div class="tip" style="color:#20352A !important; background-color:#E8F5E9 !important;">'
            f'<b style="color:#20352A !important;">{CATALOGO[nome]["icon"]} {html.escape(nome)}</b>'
            f'<br><span style="color:#20352A !important;">{html.escape(CATALOGO[nome]["dica"])}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    for dica in DICAS_GERAIS:
        st.markdown(
            f'<div class="gold-tip" style="color:#20352A !important;">'
            f'✨ {html.escape(dica)}</div>',
            unsafe_allow_html=True,
        )


    st.markdown("### 📚 Fontes e confiabilidade")

    st.markdown(
        """
        - [ANEEL — Tarifas para consumidores](https://www.gov.br/aneel/pt-br/assuntos/consumidores/tarifas)
        - [ANEEL — Ranking das tarifas homologadas](https://www.gov.br/aneel/pt-br/assuntos/tarifas/ranking-das-tarifas)
        - [ANEEL — Bandeiras tarifárias](https://www.gov.br/aneel/pt-br/assuntos/tarifas/bandeiras-tarifarias)
        - [INMETRO — Tabelas de eficiência energética / PBE](https://www.gov.br/inmetro/pt-br/assuntos/regulamentacao/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica)
        """
    )

    st.markdown(
        '<div class="gold-tip"><b>⚠️ Aviso importante:</b> potências e rotinas pré-preenchidas são ilustrativas e editáveis. '
        'Sempre que possível, use os dados da etiqueta, do manual ou do Programa Brasileiro de Etiquetagem do Inmetro. '
        'O custo é uma estimativa simplificada: a conta real pode incluir tributos, bandeiras tarifárias, contribuição de iluminação pública, '
        'regras de faturamento e outros componentes. A tarifa usada deve ser conferida para a distribuidora e o período de interesse.</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("↻ Jogar novamente", type="primary", use_container_width=True):
            st.session_state.fase = 0
            st.session_state.equipamentos = {}
            st.session_state.reducoes = {}
            st.session_state.tarifa = 0.85
            st.session_state.jogo_iniciado = True
            st.rerun()

    with c2:
        if st.button("🏠 Voltar ao início", use_container_width=True):
            st.session_state.jogo_iniciado = False
            st.session_state.fase = 0
            st.rerun()


# ---------------------------------------------------------------------
# APLICAÇÃO
# ---------------------------------------------------------------------
if not st.session_state.jogo_iniciado:
    tela_inicial()
else:
    mostrar_cabecalho()
    mostrar_progresso()
    fase = st.session_state.fase

    if fase == 0:
        fase_montar_casa()
    elif fase == 1:
        fase_consumo()
    elif fase == 2:
        fase_desafios()
    elif fase == 3:
        fase_resultados()
    elif fase == 4:
        fase_medalha()

    st.markdown(
        '<div class="footer">MAPA ENERGÉTICO DA COMUNIDADE · Engenharia de Energia · IFBA – Campus Lauro de Freitas</div>',
        unsafe_allow_html=True,
    )

