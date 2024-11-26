import cx_Oracle
import random
from datetime import datetime, timedelta
from configparser import ConfigParser
import argparse
from sklearn.datasets import make_regression
import numpy as np

# Inicializar o Oracle Instant Client (caso necessário)
cx_Oracle.init_oracle_client(lib_dir="/Users/pedrosof/Downloads/instantclient_23_3")

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
    user = config.get('Database', 'username')
    password = config.get('Database', 'password')

    dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)
    conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
    print("Conexão estabelecida com o banco de dados.")
    return conn

# Função para validar as datas fornecidas
def validar_datas(start_date, end_date):
    hoje = datetime.now().date()
    if start_date.date() > hoje:
        raise ValueError(f"A data de início não pode ser futura: {start_date}")
    if end_date.date() > hoje:
        raise ValueError(f"A data de fim não pode ser futura: {end_date}")
    if start_date > end_date:
        raise ValueError(f"A data de início ({start_date}) não pode ser maior que a data de fim ({end_date}).")

# Função para gerar dados usando make_regression
def gerar_dados_regression(n_samples, base, minimo, maximo):
    """
    Gera dados usando make_regression e ajusta para um intervalo específico.
    """
    X, y = make_regression(n_samples=n_samples, n_features=1, noise=0.000005, random_state=42)
    valores = X.flatten() * 5 + base  # Ajuste os valores para o intervalo desejado
    valores = [max(min(v, maximo), minimo) for v in valores]  # Limita ao intervalo
    return valores

# Função para suavizar valores com média móvel
def suavizar_valores(valores, janela=3):
    return [sum(valores[max(0, i-janela+1):i+1]) / (i - max(0, i-janela+1) + 1) for i in range(len(valores))]

# Função para inserir dados na tabela sensor_data
def insert_data_sensor_data(cursor, conn, reading_date, temperature, humidity, ph_value, button_p, button_k):
    insert_sql = """
        INSERT INTO sensor_data (id, reading_date, temperature, humidity, ph_value, button_p_pressed, button_k_pressed)
        VALUES (SENSOR_DATA_SEQ.NEXTVAL, :1, :2, :3, :4, :5, :6)
    """
    try:
        cursor.execute(insert_sql, (reading_date, temperature, humidity, ph_value, button_p, button_k))
        conn.commit()
        print(f"Dados inseridos na tabela sensor_data: {reading_date}, {temperature}, {humidity}, {ph_value}, {button_p}, {button_k}")
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao inserir dados na tabela sensor_data: {e}")
        conn.rollback()

# Função para inserir dados na tabela condicoes_climaticas
def insert_data_condicoes_climaticas(cursor, conn, reading_date, temperatura, umidade, clima, precipitation):
    insert_sql = """
        INSERT INTO condicoes_climaticas (data_coleta, temperatura, umidade, clima, precipitation)
        VALUES (:1, :2, :3, :4, :5)
    """
    try:
        cursor.execute(insert_sql, (reading_date, temperatura, umidade, clima, precipitation))
        conn.commit()
        print(f"Dados inseridos na tabela condicoes_climaticas: {reading_date}, {temperatura}, {umidade}, {clima}, {precipitation}")
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao inserir dados na tabela condicoes_climaticas: {e}")
        conn.rollback()

# Função principal para gerar e inserir dados
def gerar_e_inserir_dados(cursor, conn, start_date, end_date, registros_por_dia):
    hoje = datetime.now().date()
    current_date = start_date.date()
    end_date = min(end_date.date(), hoje)
    interval_hours = 4  # Intervalo de 4 horas entre registros

    print(f"Iniciando a inserção de dados entre {current_date} e {end_date} com no máximo {registros_por_dia} registros por dia.")

    hum_base = 50.0
    ph_base = 6.5
    precip_base = 20.0

    while current_date <= end_date:
        # Gerar valores para o dia atual
        temperatures = gerar_dados_regression(registros_por_dia, base=25.0, minimo=10, maximo=40)
        humidities = gerar_dados_regression(registros_por_dia, base=50.0, minimo=30, maximo=80)
        ph_values = gerar_dados_regression(registros_por_dia, base=6.5, minimo=4.0, maximo=7.0)
        precipitacao = gerar_dados_regression(registros_por_dia, base=20.0, minimo=5, maximo=90)

        # Suavizar os valores gerados
        temperatures = suavizar_valores(temperatures, janela=3)
        humidities = suavizar_valores(humidities, janela=3)
        ph_values = suavizar_valores(ph_values, janela=3)
        precipitacao = suavizar_valores(precipitacao, janela=3)

        for i in range(registros_por_dia):
            base_datetime = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=i * interval_hours)

            temp = temperatures[i]
            hum = humidities[i]
            ph = ph_values[i]
            precip = precipitacao[i]

            # Gerar valores para os botões
            button_p_state = random.choice([0, 1])
            button_k_state = random.choice([0, 1])

            # Inserir dados no banco
            insert_data_sensor_data(cursor, conn, base_datetime, temp, hum, ph, button_p_state, button_k_state)

            # Gerar condições climáticas
            clima = random.choice([
                "céu limpo", "nublado", "chuva leve", "chuva intensa",
                "tempestade", "névoa", "ensolarado", "chuva moderada"
            ])

            insert_data_condicoes_climaticas(cursor, conn, base_datetime, temp, hum, clima, precip)

        current_date += timedelta(days=1)

    print("Processo de inserção concluído.")

# Função principal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para gerar e inserir dados no Oracle.")
    parser.add_argument('-rp', type=int, help="Número de registros por dia.", default=6)
    parser.add_argument('--start_date', type=lambda s: datetime.strptime(s, '%Y-%m-%d'), help="Data de início no formato YYYY-MM-DD.")
    parser.add_argument('--end_date', type=lambda s: datetime.strptime(s, '%Y-%m-%d'), help="Data de fim no formato YYYY-MM-DD.")
    args = parser.parse_args()

    hoje = datetime.now()
    start_date = args.start_date if args.start_date else hoje
    end_date = args.end_date if args.end_date else hoje

    try:
        validar_datas(start_date, end_date)
    except ValueError as e:
        print(f"Erro de validação: {e}")
        exit(1)

    conn = conectar_banco()
    cursor = conn.cursor()

    gerar_e_inserir_dados(cursor, conn, start_date, end_date, args.rp)

    cursor.close()
    conn.close()
