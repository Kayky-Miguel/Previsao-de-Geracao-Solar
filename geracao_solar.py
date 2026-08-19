import pandas as pd
import numpy as np
import joblib
import requests
from datetime import date, timedelta

# Carregando o modelo


def prever():
    """
    Retorna um DataFrame com a previsão horária de geração solar para amanhã,
    contendo as colunas 'Hora' (str, formato HH:MM) e 'Geração Prevista' (kWh).
    """

    modelo = joblib.load('modelo_geracao_solar.pkl')
    colunas_features = joblib.load("colunas_features.pkl")

    # --- Busca o clima previsto (Open-Meteo / GFS) ---
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -7.1195,
        "longitude": -34.8450,
        "hourly": "shortwave_radiation,direct_radiation,diffuse_radiation,global_tilted_irradiance,temperature_2m,wind_speed_10m,cloud_cover",
        "tilt": 7,
        "azimuth": 0,
        "models": "gfs_seamless",
        "forecast_days": 2,          # hoje + amanhã
        "timezone": "America/Recife",
    }

    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    df_previsao = pd.DataFrame(resp.json()["hourly"])
    df_previsao["time"] = pd.to_datetime(df_previsao["time"])
    df_previsao = df_previsao.set_index("time")

    # Filtra só o dia de amanhã
    amanha = (pd.Timestamp.now(tz="America/Recife") + pd.Timedelta(days=1)).date()
    df_amanha = df_previsao[df_previsao.index.date == amanha]

    if df_amanha.empty:
        raise ValueError(
            "Não foi possível obter dados meteorológicos para o dia seguinte. "
            "Tente novamente mais tarde."
        )

    X_amanha = df_amanha[colunas_features]   # ajuste pro nome real das suas features

    previsao_geracao_kwh = modelo.predict(X_amanha)

    # Monta o DataFrame horário que a interface espera
    df_resultado = pd.DataFrame({
        "Hora": df_amanha.index.strftime("%H:%M"),
        "Geração Prevista": previsao_geracao_kwh,
    }).reset_index(drop=True)

    return df_resultado