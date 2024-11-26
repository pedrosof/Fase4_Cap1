import cx_Oracle
import random
from datetime import datetime, timedelta
from configparser import ConfigParser
import argparse

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

# Função para ajustar valores respeitando os limites e variações baseadas no valor anterior
def ajustar_valores(valor_anterior, minimo, maximo, variacao_percentual):
    """
    Ajusta o valor com base no último valor gerado, respeitando os limites e a variação percentual.
    """
    max_variacao = valor_anterior * variacao_percentual / 100
    novo_valor = valor_anterior + random.uniform(-max_variacao, max_variacao)
    return max(min(novo_valor, maximo), minimo)

# Função para buscar o último registro do banco de dados
def buscar_ultimo_registro(cursor):
    """
    Busca o último registro inserido no banco de dados para garantir continuidade nos valores.
    """
    query = """
        SELECT 
            sd.temperature, 
            sd.humidity, 
            sd.ph_value, 
            cc.precipitation
        FROM 
            sensor_data sd
        LEFT JOIN 
            condicoes_climaticas cc
        ON 
            TRUNC(sd.reading_date) = TRUNC(cc.data_coleta)
        WHERE 
            ROWNUM = 1
        ORDER BY 
            sd.reading_date DESC
    """
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return {
            "temperature": result[0],
            "humidity": result[1],
            "ph_value": result[2],
            "precipitation": result[3] if result[3] is not None else random.uniform(5, 90)
        }
    else:
        # Valores iniciais caso o banco esteja vazio
        return {
            "temperature": random.uniform(10, 40),
            "humidity": random.uniform(30, 80),
            "ph_value": random.uniform(4.00, 7.00),
            "precipitation": random.uniform(5, 90)
        }

# Função para validar as datas fornecidas
def validar_datas(start_date, end_date):
    hoje = datetime.now().date()
    if start_date.date() > hoje:
        raise ValueError(f"A data de início não pode ser futura: {start_date}")
    if end_date.date() > hoje:
        raise ValueError(f"A data de fim não pode ser futura: {end_date}")
    if start_date > end_date:
        raise ValueError(f"A data de início ({start_date}) não pode ser maior que a data de fim ({end_date}).")

def insert_data_sensor_data(cursor, conn, reading_date, temperature, humidity, ph_value, button_p, button_k):
    """Insere dados na tabela sensor_data."""
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

def insert_data_condicoes_climaticas(cursor, conn, reading_date, temperatura, umidade, clima, precipitation):
    """Insere dados na tabela condicoes_climaticas."""
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

def gerar_e_inserir_dados(cursor, conn, start_date, end_date, registros_por_dia):
    """Gera e insere dados aleatórios nas tabelas sensor_data e condicoes_climaticas."""
    hoje = datetime.now().date()
    current_date = start_date.date()
    end_date = min(end_date.date(), hoje)  # Limitar a data final ao dia de hoje
    interval_hours = 4  # Intervalo de 4 horas entre simulações

    print(f"Iniciando a inserção de dados entre {current_date} e {end_date} com no máximo {registros_por_dia} registros por dia.")

    # Buscar o último registro no banco
    ultimo_registro = buscar_ultimo_registro(cursor)

    temp_base = ultimo_registro["temperature"]
    hum_base = ultimo_registro["humidity"]
    ph_base = ultimo_registro["ph_value"]
    precipitation_base = ultimo_registro["precipitation"]

    while current_date <= end_date:
        # Garante até 6 entradas por dia
        registros_por_dia = min(registros_por_dia, 6)

        for i in range(registros_por_dia):
            # Calcular o horário baseado no índice e no intervalo de horas
            base_datetime = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=i * interval_hours)

            # Ajustar valores com base no último valor gerado
            temp_base = ajustar_valores(temp_base, 10, 40, 5)
            hum_base = ajustar_valores(hum_base, 30, 80, 5)
            ph_base = ajustar_valores(ph_base, 4.00, 7.00, 5)
            precipitation_base = ajustar_valores(precipitation_base, 5, 90, 5)

            # Gerar valores para os botões
            button_p_state = random.choice([0, 1])
            button_k_state = random.choice([0, 1])

            # Inserir dados na tabela sensor_data
            insert_data_sensor_data(cursor, conn, base_datetime, temp_base, hum_base, ph_base, button_p_state, button_k_state)

            # Gerar condições climáticas aleatórias
            clima = random.choice([
                "céu limpo", "nublado", "chuva leve", "chuva intensa",
                "tempestade", "névoa", "ensolarado", "chuva moderada"
            ])

            # Inserir dados na tabela condicoes_climaticas
            insert_data_condicoes_climaticas(cursor, conn, base_datetime, temp_base, hum_base, clima, precipitation_base)

        # Avançar para o próximo dia
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
