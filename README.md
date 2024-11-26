
# FIAP - Faculdade de Informática e Administração Paulista
[![FIAP Logo](images/logo-fiap.png)](https://www.fiap.com.br)

## Fase 3 Cap 1 – Construindo uma máquina agrícola
[GitHub](https://github.com/pedrosof/Fase3_Cap1)
### Grupo 10

👨‍🎓 **Integrantes**:
- [Fabio Marcos Pedroso Filho](https://www.linkedin.com/in/pedrosof/)

👩‍🏫 **Professores**:

**Tutor(a)**:
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

**Coordenador(a)**:
- [Andre Godoi, PhD](https://www.linkedin.com/in/profandregodoi/)

---

## 📜 Descrição

O objetivo deste projeto é a criação de um sistema de **monitoramento** e **análise de dados** de sensores de solo e condições climáticas, utilizando duas abordagens complementares: uma para a geração de um **dashboard interativo** e outra para os **cálculos de irrigação**.

### Primeiro Código: Python com Dash e R
Este código utiliza **Python** e a biblioteca **Dash** para criar um **dashboard interativo**, que permite visualizar dados de sensores de solo e condições climáticas. O sistema se conecta a um banco de dados Oracle para obter informações sobre **temperatura**, **umidade**, **pH do solo**, e dados climáticos como **temperatura**, **umidade**, e a **condição climática**. 

O código:
- Lê as configurações do banco de dados a partir de um arquivo de configuração.
- Executa uma consulta SQL para combinar dados de sensores e clima.
- Processa esses dados com **Pandas**.
- Exibe gráficos interativos no dashboard, que mostram a variação de diferentes variáveis como temperatura e eventos climáticos.
- Utiliza um script **R** para calcular o volume de água necessário para irrigação e exibe o gráfico gerado no dashboard.

### Segundo Código: R com Análise e Gráficos
O código em **R** conecta-se ao banco de dados Oracle, carrega dados de sensores de solo e condições climáticas, e calcula o volume de água necessário para irrigação. Ele utiliza ajustes baseados em fatores como **temperatura** e **umidade** para determinar **quando** e **quanto irrigar**.

Após realizar os cálculos, o código gera um gráfico de linha que mostra o volume de água necessário ao longo do tempo, salvando-o como um arquivo **PNG** que pode ser exibido no dashboard do primeiro código.

### Terceiro Código: Script de Geração e Inserção de Dados no Banco de Dados Oracle

Este script gera e insere dados aleatórios de sensores de solo e condições climáticas no banco de dados Oracle. Ele também se conecta à API OpenWeather para buscar condições climáticas reais.

#### Principais Funcionalidades:
- **Conexão ao Banco de Dados**: Realizada através de cx_Oracle, utilizando configurações carregadas de um arquivo `config.cfg`.
- **Geração de Datas Aleatórias**: Datas são geradas dentro de um intervalo definido, evitando duplicidades no banco de dados.
- **Inserção de Dados**:
  - Na tabela `sensor_data`: Temperatura do solo, umidade, pH e estado dos botões.
  - Na tabela `condicoes_climaticas`: Temperatura, umidade e clima.
- **Chamada à API OpenWeather**: Busca condições climáticas reais para a cidade especificada no arquivo de configuração.
- **Argumentos de Linha de Comando**: Permite personalizar o número de entradas e o intervalo de datas para os dados gerados.

Esse script é útil para testes e simulações de sistemas que monitoram dados agrícolas e climáticos.

### Resumo Conjunto

Os três códigos trabalham juntos para construir um sistema completo de **monitoramento e análise de dados agrícolas**. O **Python** com **Dash** é utilizado para a visualização e interação com o usuário, permitindo a exibição de dados de sensores de solo e condições climáticas em tempo real. O **R** é responsável pelos cálculos detalhados de irrigação, com base nos dados coletados, gerando gráficos que mostram o volume de água necessário ao longo do tempo.

Além disso, o **terceiro código** automatiza a geração e inserção de dados aleatórios no banco de dados Oracle, simulando as leituras dos sensores de solo e as condições climáticas. Ele também se integra com a API **OpenWeather** para obter dados reais de clima, o que enriquece a análise de irrigação e a precisão dos cálculos.

Juntos, esses três códigos formam um sistema robusto e integrado, que facilita a **tomada de decisões sobre a irrigação**, oferecendo uma visão completa dos dados de solo e clima. O sistema também é útil para testes e simulações, ajudando a prever e otimizar o uso de água em diferentes cenários agrícolas.

- **Dados Climáticos**: Obtidos através da API pública [OpenWeather](https://openweathermap.org/).
- **Dados do Solo**: Capturados por sensores desenvolvidos no site [Wokwi](https://wokwi.com/).

---

# Resumo do que foi criado no Wokwi

- **Projeto do Sensor**: O projeto do sensor criado está disponível em: [Wokwi Project](https://wokwi.com/projects/412014758291630081).

![Wokwi Sensor](images/wokwi.png)

### Resumo do Circuito

Este circuito simulado no Wokwi inclui os seguintes componentes principais:

- **ESP32** programado em **MicroPython**.
- **Sensores**:
  - **DHT22** (`dht1`): Sensor de temperatura (20°C) e umidade (20.5%), conectado ao pino **2** do ESP32.
  - **LDR** (`ldr1`): Sensor de luz com intensidade de **130 lux**, conectado ao pino analógico **34** do ESP32.
- **LEDs**:
  - **LED vermelho** (`led1`): Conectado ao resistor de **150Ω** (`r1`) e ao pino **0** do ESP32.
  - **LED azul** (`led2`): Conectado ao resistor de **90Ω** (`r2`) e ao pino **4** do ESP32.
  - **LED verde-limão** (`led3`): Conectado ao resistor de **140Ω** (`r3`) e ao pino **25** do ESP32.
- **Botões**:
  - **Botão azul** (`btn1`): Conectado ao pino **27** do ESP32.
  - **Botão verde** (`btn2`): Conectado ao pino **26** do ESP32.

Este resumo destaca os componentes principais do circuito e suas conexões essenciais com a placa ESP32.

### Resumo do Script

O script gerado no wokwi monitora **temperatura**, **umidade**, **luminosidade** e o estado de dois botões (P e K) em um sistema embarcado. Ele utiliza sensores como o **DHT22** para coletar dados de temperatura e umidade, e um **LDR** para medir a luminosidade. Além disso, três LEDs indicam o status dessas variáveis:

- **LED de Temperatura (vermelho)**: Acende quando a temperatura ultrapassa o limite definido.
- **LED de Umidade (verde-limão)**: Acende quando a umidade está abaixo do valor mínimo.
- **LED de pH (azul)**: Acende quando a luminosidade está fora da faixa ideal.

Os botões **P** e **K** são monitorados e, quando pressionados, exibem o respectivo estado no console.

Este sistema é ideal para monitoramento de variáveis ambientais e controle visual com LEDs em aplicações embarcadas.

---

[Video do Funcionamento no Youtube](https://youtu.be/RNyyCE6V7ow)

---

## 📁 Estrutura de Pastas

- **config**: Arquivos de configuração.
- **README.md**: Este arquivo com a explicação geral sobre o projeto.
- **wokwi**: Código fonte e JSON do diagrama do sensor de solo.
- **images**: Imagens documentacionais.

---

## 🔧 Como Executar o Código

Para executar o código, siga os passos abaixo:

1. Tenha um banco de dados Oracle configurado e instalado.
2. Utilize [Python](https://www.python.org/downloads/)
3. Utilize o [Oracle Instant Client](https://www.oracle.com/br/database/technologies/instant-client.html).
4. Utilize o [Oracle JDBC Driver](https://www.oracle.com/database/technologies/appdev/jdbc-downloads.html)

### Scripts Principais:

- **Install.py**: Cria a estrutura do banco de dados.
- **Dashboard.py**: Exibe gráficos dos dados obtidos.
- **LigaBomba.R**: Calcula o volume de água necessário para irrigação.
- **SimulaEntradas.py**: Gera dados para o dia atual e entradas aleatórias para datas anteriores.

### Configuração:

1. Configure o arquivo config/config.cfg (OpenWeather apikey e Conexões Oracle)
2. Configure os arquivos python
```python
cx_Oracle.init_oracle_client(lib_dir="/Path/to/Oracle/instantclient")

RSCRIPT_PATH = "/Path/to/Rscript"
SCRIPT_R_PATH = "/Path/to/LigaBomba.R"
GRAPH_PATH = "/Path/to/LigaBomba.png"
```
3. Configure os arquivos R
```r
GRAPH_PATH <- "/Path/to/LigaBomba.png"

drv <- JDBC(driverClass = "oracle.jdbc.OracleDriver", 
            classPath = "/Path/to/ojdbc8.jar")
```

---

## 🗃 Histórico de Lançamentos

```markdown
- **0.9.0** – 20/10/2024: *Volume de Água de Irrigação armazenado em banco de dados*
- **0.8.0** – 20/10/2024: *Ajuste de Climas e Novos Gráficos no Dashboard*
- **0.7.0** – 20/10/2024: *Documentação*
- **0.6.0** – 20/10/2024: *Criação do Simulador de Entradas*
- **0.5.0** – 20/10/2024: *Crição do script R para volumetria de irrigação*
- **0.4.0** – 19/10/2024: *Criação do Dashboard*
- **0.3.0** – 18/10/2024: *Criação do Instalador*
- **0.2.0** – 18/10/2024: *Criação do Circuito e Script do Wokwi*
- **0.1.0** – 17/10/2024: *Versão Inicial*
```

---

## 📋 Licença

Este projeto está licenciado sob os termos da licença **GPL**.
