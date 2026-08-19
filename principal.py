import streamlit as st
import pandas as pd
import numpy as np
import requests
from geracao_solar import prever
 
st.set_page_config(
    page_title="Sistema de Previsão de Geração Solar",
    page_icon="☀️",
    layout="wide"
)
 
# ---------------------------
# Título e descrição
# ---------------------------
st.title("☀️ Sistema de Previsão de Geração Solar")
st.markdown(
    "Previsão de geração fotovoltaica para o dia seguinte, utilizando dados "
    "meteorológicos (Open-Meteo / GFS) e um modelo de Machine Learning."
)
st.divider()
 
# ---------------------------
# Barra lateral - Configurações
# ---------------------------
st.sidebar.header("⚙️ Configurações")
 
cidade = st.sidebar.text_input("Cidade", "João Pessoa")
 
potencia_sistema = st.sidebar.number_input(
    "Potência do sistema (kWp)",
    min_value=0.0,
    value=5.0,
    step=0.5
)
 
st.sidebar.divider()
 
atualizar = st.sidebar.button("🔄 Atualizar previsão", use_container_width=True)
 
st.sidebar.caption(f"📍 Local: {cidade}")
st.sidebar.caption(f"🔋 Potência instalada: {potencia_sistema} kWp")
 
 
# ---------------------------
# Busca da previsão (com cache)
# ---------------------------
@st.cache_data(ttl=3600, show_spinner="Calculando previsão de geração...")
def obter_previsao():
    return prever()
 
 
if atualizar:
    obter_previsao.clear()  # força buscar dados novos ao clicar no botão
 
try:
    df = obter_previsao()
except FileNotFoundError as e:
    st.error(
        "Não foi possível carregar o modelo (arquivo .pkl não encontrado). "
        f"Detalhes: {e}"
    )
    st.stop()
except requests.exceptions.RequestException as e:
    st.error(f"Erro ao consultar a API meteorológica: {e}")
    st.stop()
except Exception as e:
    st.error(f"Ocorreu um erro ao gerar a previsão: {e}")
    st.stop()
 
if atualizar:
    st.sidebar.success("Previsão atualizada!")
 
# ---------------------------
# Métricas principais
# ---------------------------
col1, col2, col3 = st.columns(3)
 
energia_total = df["Geração Prevista"].sum()
pico_geracao = df["Geração Prevista"].max()
hora_pico = df.loc[df["Geração Prevista"].idxmax(), "Hora"]
 
col1.metric("⚡ Energia Total Prevista", f"{energia_total:.2f} kWh")
col2.metric("📈 Pico de Geração", f"{pico_geracao:.2f} kWh")
col3.metric("🕐 Horário de Pico", f"{hora_pico}")
 
st.divider()
 
# ---------------------------
# Gráfico e tabela em abas
# ---------------------------
tab_grafico, tab_dados = st.tabs(["📊 Gráfico de Geração", "📋 Dados Detalhados"])
 
with tab_grafico:
    st.line_chart(df.set_index("Hora")["Geração Prevista"])
 
with tab_dados:
    st.dataframe(df, use_container_width=True)
 
# ---------------------------
# Rodapé
# ---------------------------
st.divider()
st.caption("Projeto Integrador I - Engenharia das Energias | UFPB")