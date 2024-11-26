import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import cx_Oracle
from configparser import ConfigParser
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# Inicialização do cliente Oracle
try:
    cx_Oracle.init_oracle_client(lib_dir="/Users/pedrosof/Downloads/instantclient_23_3")
except cx_Oracle.ProgrammingError:
    # Ignorar erro se o cliente já estiver inicializado
    pass

# Função para carregar as configurações do arquivo config.cfg
def carregar_configuracoes():
    config = ConfigParser()
    config.read('config/config.cfg')
    return config

# Função para conectar ao banco de dados Oracle
def conectar_banco():
    config = carregar_configuracoes()
    host = config.get('Database', 'host')
    port = config.get('Database', 'port')
    service_name = config.get('Database', 'service_name')
    username = config.get('Database', 'username')
    password = config.get('Database', 'password')

    dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)
    conn = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
    return conn

# Função para carregar os dados das tabelas
@st.cache_data
def carregar_dados():
    conn = conectar_banco()
    try:
        # Consulta para CONDICOES_CLIMATICAS, ordenada por DATA_COLETA
        query_clima = """
            SELECT ID_CLIMA, DATA_COLETA, TEMPERATURA, CLIMA, UMIDADE, PRECIPITATION 
            FROM CONDICOES_CLIMATICAS 
            ORDER BY DATA_COLETA
        """
        
        # Consulta para SENSOR_DATA, ordenada por READING_DATE
        query_sensores = """
            SELECT ID, READING_DATE, TEMPERATURE, HUMIDITY, PH_VALUE, BUTTON_P_PRESSED, BUTTON_K_PRESSED 
            FROM SENSOR_DATA 
            ORDER BY READING_DATE
        """

        # Carregar dados usando Pandas e cx_Oracle
        condicoes_climaticas = pd.read_sql(query_clima, conn, parse_dates=['DATA_COLETA'])
        sensor_data = pd.read_sql(query_sensores, conn, parse_dates=['READING_DATE'])
    finally:
        conn.close()

    return condicoes_climaticas, sensor_data

# Carregar dados
condicoes_climaticas, sensor_data = carregar_dados()

# Configuração do título do app
st.title("Análise Exploratória de Dados - Clima vs Solo")

# Seleção de intervalo de datas
st.sidebar.header("Seleção de Intervalo de Tempo")

# Obter as datas mínimas e máximas dos datasets
min_date = min(condicoes_climaticas['DATA_COLETA'].min(), sensor_data['READING_DATE'].min()).date()
max_date = max(condicoes_climaticas['DATA_COLETA'].max(), sensor_data['READING_DATE'].max()).date()

# Seleção de datas pelo usuário
start_date = st.sidebar.date_input('Data inicial', min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input('Data final', max_date, min_value=min_date, max_value=max_date)

if start_date > end_date:
    st.sidebar.error('Erro: A data final deve ser posterior à data inicial.')
else:
    # Filtrar os dados com base no intervalo selecionado
    condicoes_climaticas_filtrado = condicoes_climaticas[
        (condicoes_climaticas['DATA_COLETA'] >= pd.to_datetime(start_date)) &
        (condicoes_climaticas['DATA_COLETA'] <= pd.to_datetime(end_date))
    ]
    sensor_data_filtrado = sensor_data[
        (sensor_data['READING_DATE'] >= pd.to_datetime(start_date)) &
        (sensor_data['READING_DATE'] <= pd.to_datetime(end_date))
    ]

    # Mostrar os dados filtrados
    #st.header("Dados das Condições Climáticas (Filtrado)")
    #st.write(condicoes_climaticas_filtrado.head())

    #st.header("Dados dos Sensores do Solo (Filtrado)")
    #st.write(sensor_data_filtrado.head())

    # Configurar estilo do Seaborn
    sns.set_style('darkgrid')

    # Gráfico 1: Comparação de Temperaturas - Clima vs Solo
    st.subheader("Comparação de Temperaturas - Clima vs Solo")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=[condicoes_climaticas_filtrado["TEMPERATURA"], sensor_data_filtrado["TEMPERATURE"]], ax=ax1, palette="Set2")
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(["Clima", "Solo"])
    ax1.set_title("Comparação de Temperaturas", fontsize=16)
    ax1.set_ylabel("Temperatura (°C)")
    st.pyplot(fig1)

    # Gráfico 2: Comparação de Umidades - Clima vs Solo
    st.subheader("Comparação de Umidades - Clima vs Solo")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=[condicoes_climaticas_filtrado["UMIDADE"], sensor_data_filtrado["HUMIDITY"]], ax=ax2, palette="Set3")
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(["Clima", "Solo"])
    ax2.set_title("Comparação de Umidades", fontsize=16)
    ax2.set_ylabel("Umidade (%)")
    st.pyplot(fig2)

    # Gráfico 3: Tendência de Temperatura ao Longo do Tempo - Clima
    st.subheader("Tendência de Temperatura ao Longo do Tempo - Clima")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(condicoes_climaticas_filtrado["DATA_COLETA"], condicoes_climaticas_filtrado["TEMPERATURA"], label="Clima", color='orange')
    ax3.set_title("Tendência de Temperatura - Clima", fontsize=16)
    ax3.set_xlabel("Data")
    ax3.set_ylabel("Temperatura (°C)")
    ax3.legend()
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    fig3.autofmt_xdate()
    st.pyplot(fig3)

    # Gráfico 4: Relação entre Precipitação e Umidade no Clima
    st.subheader("Precipitação x Umidade no Clima")
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    if not condicoes_climaticas_filtrado[["PRECIPITATION", "UMIDADE"]].dropna().empty:
        scaler = MinMaxScaler()
        scaled_values = scaler.fit_transform(condicoes_climaticas_filtrado[["PRECIPITATION", "UMIDADE"]].dropna())
        ax4.scatter(scaled_values[:, 0], scaled_values[:, 1], alpha=0.7, c='green')
        ax4.set_title("Precipitação x Umidade (Normalizado)", fontsize=16)
        ax4.set_xlabel("Precipitação (Escala Normalizada)")
        ax4.set_ylabel("Umidade (Escala Normalizada)")
    else:
        ax4.text(0.5, 0.5, 'Dados insuficientes para plotar', horizontalalignment='center', verticalalignment='center')
    st.pyplot(fig4)

    # Gráfico 5: Distribuição de pH e Umidade no Solo
    st.subheader("Distribuição de pH e Umidade no Solo")
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    scatter = ax5.scatter(sensor_data_filtrado["PH_VALUE"], sensor_data_filtrado["HUMIDITY"], alpha=0.6, c=sensor_data_filtrado["HUMIDITY"], cmap='viridis')
    ax5.set_title("Distribuição de pH e Umidade", fontsize=16)
    ax5.set_xlabel("pH")
    ax5.set_ylabel("Umidade (%)")
    fig5.colorbar(scatter, ax=ax5, label='Umidade (%)')
    st.pyplot(fig5)

    # Gráfico 6: Regressão Linear - Temperatura vs Umidade no Clima
    st.subheader("Regressão Linear - Temperatura vs Umidade no Clima")
    if len(condicoes_climaticas_filtrado.dropna(subset=["TEMPERATURA", "UMIDADE"])) > 1:
        X = condicoes_climaticas_filtrado["TEMPERATURA"].values.reshape(-1, 1)
        y = condicoes_climaticas_filtrado["UMIDADE"].values

        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        fig6, ax6 = plt.subplots(figsize=(8, 6))
        ax6.scatter(condicoes_climaticas_filtrado["TEMPERATURA"], condicoes_climaticas_filtrado["UMIDADE"], label="Dados Reais", alpha=0.7)
        ax6.plot(condicoes_climaticas_filtrado["TEMPERATURA"], y_pred, color='red', label="Linha de Regressão")
        ax6.set_title("Regressão Linear - Temperatura vs Umidade no Clima", fontsize=16)
        ax6.set_xlabel("Temperatura (°C)")
        ax6.set_ylabel("Umidade (%)")
        ax6.legend()
        st.pyplot(fig6)
    else:
        st.warning("Dados insuficientes no intervalo selecionado para regressão linear.")

    # Gráfico 7: Clusterização K-Means - Umidade e pH no Solo
    st.subheader("Clusterização K-Means - Umidade e pH no Solo")
    if len(sensor_data_filtrado.dropna(subset=["HUMIDITY", "PH_VALUE"])) > 1:
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(sensor_data_filtrado[["HUMIDITY", "PH_VALUE"]].dropna())

        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(data_scaled)

        sensor_data_filtrado = sensor_data_filtrado.dropna(subset=["HUMIDITY", "PH_VALUE"])
        sensor_data_filtrado["Cluster"] = clusters

        fig7, ax7 = plt.subplots(figsize=(8, 6))
        scatter = ax7.scatter(
            sensor_data_filtrado["HUMIDITY"],
            sensor_data_filtrado["PH_VALUE"],
            c=sensor_data_filtrado["Cluster"],
            cmap="viridis",
            alpha=0.7
        )
        ax7.set_title("Clusterização K-Means - Umidade e pH no Solo", fontsize=16)
        ax7.set_xlabel("Umidade (%)")
        ax7.set_ylabel("pH")
        fig7.colorbar(scatter, ax=ax7, label="Cluster")
        st.pyplot(fig7)
    else:
        st.warning("Dados insuficientes no intervalo selecionado para clusterização.")

    # Gráfico 8: Cálculo de Irrigação Diária
    st.subheader("Cálculo de Irrigação Diária")

    if not condicoes_climaticas_filtrado.empty and not sensor_data_filtrado.empty:
        # Normalizar e tratar os dados
        df_irrigacao = pd.merge(
            condicoes_climaticas_filtrado[["DATA_COLETA", "UMIDADE", "TEMPERATURA"]],
            sensor_data_filtrado[["READING_DATE", "HUMIDITY", "PH_VALUE", "TEMPERATURE"]],
            left_on="DATA_COLETA",
            right_on="READING_DATE",
            how="inner"
        )

        # Constante para cálculo (fator de ajuste)
        k = 10

        # Cálculo de irrigação diária
        df_irrigacao["Irrigacao_Litros_m2"] = k * (
            (100 - df_irrigacao["HUMIDITY"]) / 100 +
            (100 - df_irrigacao["UMIDADE"]) / 100 +
            abs(df_irrigacao["PH_VALUE"] - 6.5) +
            (df_irrigacao["TEMPERATURE"] + df_irrigacao["TEMPERATURA"]) / 2
        )

        # Gráfico da irrigação diária
        fig8, ax8 = plt.subplots(figsize=(10, 6))

        # Plotando a linha principal para os valores diários
        ax8.plot(
            df_irrigacao["DATA_COLETA"],
            df_irrigacao["Irrigacao_Litros_m2"],
            color="#003f5c",  # Azul escuro
            linewidth=2.5,  # Linha mais grossa
            label="Irrigação Diária"
        )

        # Adicionando linha da média
        media_irrigacao = df_irrigacao["Irrigacao_Litros_m2"].mean()
        ax8.axhline(
            y=media_irrigacao,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Média: {media_irrigacao:.2f} L/m²"
        )

        ax8.set_title("Cálculo de Irrigação Diária (Litros/m²)", fontsize=16)
        ax8.set_xlabel("Data")
        ax8.set_ylabel("Litros por m²")
        ax8.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        ax8.tick_params(axis="x", rotation=45)
        ax8.legend()
        st.pyplot(fig8)
    else:
        st.warning("Dados insuficientes para calcular a irrigação diária.")

    # Fim do app
    st.success("Análises concluídas!")
