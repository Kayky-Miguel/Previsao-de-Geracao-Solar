# ☀️ Previsão de Geração Solar

Sistema de previsão de geração de energia solar fotovoltaica para o **dia seguinte**, com resolução horária. O projeto combina dados meteorológicos previstos (Open-Meteo / GFS) com um modelo de Machine Learning treinado, e apresenta os resultados em um painel interativo feito com Streamlit.

> Projeto Integrador I – Engenharia das Energias | UFPB

---

## 📋 Sumário

- [Visão geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Como funciona](#-como-funciona)
- [Estrutura do repositório](#-estrutura-do-repositório)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Como executar](#-como-executar)
- [Variáveis de entrada da previsão](#-variáveis-de-entrada-da-previsão)
- [Limitações conhecidas](#-limitações-conhecidas)
- [Autor](#-autor)

---

## 🔎 Visão geral

Prever a geração fotovoltaica com antecedência ajuda no planejamento do consumo, no dimensionamento de sistemas e na integração de fontes renováveis à rede. Este projeto busca, a cada execução, a previsão do tempo para o dia seguinte e a transforma em uma estimativa de geração (em kWh) para cada hora do dia.

## ✨ Funcionalidades

- Previsão **horária** de geração solar para o dia seguinte.
- Consulta automática de dados meteorológicos via API **Open-Meteo** (modelo `gfs_seamless`).
- Painel web com:
  - **Energia total prevista** (kWh);
  - **Pico de geração** (kWh) e **horário do pico**;
  - Gráfico de linha da geração ao longo do dia;
  - Tabela com os dados detalhados.
- Cache de 1 hora para evitar consultas repetidas à API, com botão para **forçar a atualização**.
- Tratamento de erros (modelo não encontrado, falha na API meteorológica, ausência de dados para o dia seguinte).

## ⚙️ Como funciona

```
Open-Meteo (GFS)  ──►  geracao_solar.py  ──►  modelo_geracao_solar.pkl  ──►  principal.py (Streamlit)
 previsão do tempo      filtra o dia de        prevê a geração (kWh)          métricas, gráfico e tabela
 para hoje e amanhã     amanhã e seleciona     para cada hora
                        as features
```

1. `geracao_solar.py` consulta a API Open-Meteo para hoje e amanhã e mantém apenas as horas do dia seguinte (fuso `America/Recife`).
2. As colunas usadas pelo modelo são lidas de `colunas_features.pkl`, garantindo a mesma ordem e os mesmos nomes do treinamento.
3. O modelo salvo em `modelo_geracao_solar.pkl` gera a previsão de geração para cada hora.
4. `principal.py` exibe o resultado no painel Streamlit.

## 📁 Estrutura do repositório

```
Previsao-de-Geracao-Solar/
├── principal.py                # Interface web (Streamlit)
├── geracao_solar.py            # Função prever(): busca o clima e aplica o modelo
├── modelo_geracao_solar.pkl    # Modelo de Machine Learning treinado
├── colunas_features.pkl        # Lista de features esperadas pelo modelo
├── treinamento_modelo/         # Material usado no treinamento do modelo
├── .gitignore
└── README.md
```

## 🛠️ Tecnologias

- **Python 3**
- [Streamlit](https://streamlit.io/) – interface web
- [pandas](https://pandas.pydata.org/) e [NumPy](https://numpy.org/) – manipulação de dados
- [joblib](https://joblib.readthedocs.io/) – carregamento do modelo e das features
- [requests](https://requests.readthedocs.io/) – consumo da API
- [Open-Meteo API](https://open-meteo.com/) – dados meteorológicos (modelo GFS)
- Biblioteca de Machine Learning usada no treinamento do modelo (ex.: scikit-learn) — necessária para carregar o arquivo `.pkl`

## 🚀 Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/Kayky-Miguel/Previsao-de-Geracao-Solar.git
   cd Previsao-de-Geracao-Solar
   ```

2. (Opcional) Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install streamlit pandas numpy requests joblib scikit-learn
   ```

   > Use a mesma versão da biblioteca de ML com a qual o modelo foi treinado, para evitar incompatibilidades ao carregar o `.pkl`.

## ▶️ Como executar

Na raiz do projeto, rode:

```bash
streamlit run principal.py
```

O painel abrirá no navegador (por padrão em `http://localhost:8501`).

**Uso:**

1. Ajuste as configurações na barra lateral (cidade e potência do sistema em kWp).
2. Veja as métricas, o gráfico e a tabela de geração prevista para amanhã.
3. Clique em **🔄 Atualizar previsão** para buscar dados meteorológicos novos.

> ⚠️ Execute o comando a partir da raiz do projeto: os arquivos `.pkl` são carregados com caminho relativo.

## 🌦️ Variáveis de entrada da previsão

Dados horários obtidos da Open-Meteo:

| Variável | Descrição |
|---|---|
| `shortwave_radiation` | Radiação de onda curta |
| `direct_radiation` | Radiação direta |
| `diffuse_radiation` | Radiação difusa |
| `global_tilted_irradiance` | Irradiância global no plano inclinado (inclinação 7°, azimute 0) |
| `temperature_2m` | Temperatura a 2 m |
| `wind_speed_10m` | Velocidade do vento a 10 m |
| `cloud_cover` | Cobertura de nuvens |

As colunas efetivamente enviadas ao modelo são definidas em `colunas_features.pkl`.

## ⚠️ Limitações conhecidas

- A localização usada na consulta meteorológica está **fixa** no código (latitude -7,1195 e longitude -34,8450, região de João Pessoa/PB). Os campos **Cidade** e **Potência do sistema** da barra lateral ainda não alteram o cálculo da previsão; hoje servem apenas como informação exibida.
- Não há arquivo `requirements.txt`; as dependências precisam ser instaladas manualmente.
- A qualidade da previsão depende da qualidade da previsão meteorológica (GFS) e dos dados usados no treinamento.

## 💡 Possíveis melhorias

- Usar a cidade informada para buscar as coordenadas (geocodificação) e consultar o clima do local escolhido.
- Escalar a previsão de acordo com a potência instalada informada.
- Adicionar um `requirements.txt` com versões fixas.
- Documentar o processo de treinamento e as métricas do modelo (MAE, RMSE, R²).

## 👤 Autor

**Kayky Miguel**
GitHub: [@Kayky-Miguel](https://github.com/Kayky-Miguel)

Projeto desenvolvido na disciplina Projeto Integrador I – Engenharia das Energias, UFPB.
