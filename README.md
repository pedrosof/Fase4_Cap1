
# FIAP - Faculdade de Informática e Administração Paulista
[![FIAP Logo](images/logo-fiap.png)](https://www.fiap.com.br)

## Fase 4 Cap 1 – Automação e inteligência na FarmTech Solutions
[GitHub](https://github.com/pedrosof/Fase4_Cap1) [Wokwi](https://wokwi.com/projects/415711477314913281)
### Grupo 15

👨‍🎓 **Integrantes**:
- [Fabio Marcos Pedroso Filho](https://www.linkedin.com/in/pedrosof/)

👩‍🏫 **Professores**:

**Tutor(a)**:
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

**Coordenador(a)**:
- [Andre Godoi, PhD](https://www.linkedin.com/in/profandregodoi/)

---

# Documentação: Análise e Geração de Dados para Clima e Solo

## Descrição Geral
Este projeto é composto por dois scripts com objetivos complementares:

1. **Análise e Visualização de Dados**: Um aplicativo interativo em **Streamlit** que permite explorar e visualizar dados relacionados a condições climáticas e sensores do solo.
2. **Geração e Inserção de Dados Simulados**: Um script automatizado que gera dados realistas e os insere em um banco de dados Oracle.

---

## Tecnologias Utilizadas
- **Python**: Linguagem principal do projeto.
- **Bibliotecas**:
  - `Streamlit`: Interface web interativa.
  - `cx_Oracle`: Conexão com banco Oracle.
  - `scikit-learn`: Modelos de regressão, clusterização e geração de dados simulados.
  - `Matplotlib` e `Seaborn`: Visualização de dados.
  - `Pandas` e `NumPy`: Manipulação e análise de dados.

---

## 1. Análise e Visualização de Dados

### Objetivo
Criar uma interface interativa para explorar:
- Tendências de temperatura, umidade e pH.
- Comparações entre dados climáticos e do solo.
- Clusterização (K-Means) e regressão linear para identificar padrões.

### Funcionalidades
- **Seleção de Intervalo de Datas**: Filtra os dados com base em datas escolhidas pelo usuário.
- **Gráficos Gerados**:
  - **Boxplots**: Comparações de temperatura e umidade (clima vs solo).
  - **Tendências Temporais**: Temperaturas ao longo do tempo.
  - **Relações entre Variáveis**:
    - Precipitação x Umidade.
    - Distribuição de pH e Umidade.
  - **Modelos Avançados**:
    - Regressão Linear (Temperatura x Umidade).
    - Clusterização K-Means (Umidade e pH no solo).
  - **Cálculo de Irrigação Diária**: Baseado em variáveis climáticas e do solo.

---

## 2. Geração e Inserção de Dados Simulados

### Objetivo
Automatizar a geração de dados realistas para alimentar um banco de dados Oracle com informações de:
- Temperatura.
- Umidade.
- pH.
- Precipitação.

### Funcionalidades
- **Geração de Dados**:
  - Utiliza `make_regression` para criar valores simulados ajustados a intervalos plausíveis.
  - Suaviza os valores com média móvel.
- **Inserção no Banco**:
  - Dados são inseridos nas tabelas `SENSOR_DATA` e `CONDICOES_CLIMATICAS`.
- **Configuração via Linha de Comando**:
  - `--start_date` e `--end_date`: Definem o intervalo de datas.
  - `-rp`: Define o número de registros por dia.

---

## Comparação entre os Scripts

| Aspecto               | Análise e Visualização                    | Geração e Inserção                     |
|-----------------------|-------------------------------------------|----------------------------------------|
| **Objetivo**          | Explorar e visualizar dados climáticos e do solo. | Gerar e inserir dados simulados.      |
| **Entrada de Dados**  | Banco de dados Oracle.                    | Geração automática (simulada).         |
| **Saída de Dados**    | Gráficos e insights interativos.          | Dados inseridos no banco Oracle.       |
| **Uso de Scikit-learn**| Regressão linear e clusterização.         | Geração de dados com `make_regression`.|

---

## Execução

### Requisitos
- **Dependências Python**:
  - `streamlit`, `cx_Oracle`, `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`.
- **Banco de Dados**:
  - Configurações válidas no arquivo `config/config.cfg`.
  - Tabelas `SENSOR_DATA` e `CONDICOES_CLIMATICAS` devem estar criadas no Oracle.

### Instruções
1. **Análise e Visualização**:
   ```bash
   streamlit run Dashboard-streamlit.py
   ```
2. **Geração e Inserção**:
   ```bash
   python SimulaEntradas-sklearn.py --start_date 2024-01-01 --end_date 2024-11-26 -rp 6
   ```

---

## Melhorias Futuras
1. **Análise Avançada**:
   - Previsão de variáveis climáticas.
2. **Performance**:
   - Implementar paginação para grandes volumes de dados.
3. **Integração**:
   - Exportação de gráficos e dados para relatórios automatizados.

---

[Video do Funcionamento no Youtube](https://youtu.be/baq7eUIWIZs)

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
- **Dashboard-streamlit.py**: Exibe gráficos dos dados obtidos.
- **SimulaEntradas-sklearn.py**: Gera dados para o dia atual e entradas aleatórias para datas anteriores.

### Configuração:

1. Configure o arquivo config/config.cfg (OpenWeather apikey e Conexões Oracle)
2. Configure os arquivos python
```python
cx_Oracle.init_oracle_client(lib_dir="/Path/to/Oracle/instantclient")
```

---

## 🗃 Histórico de Lançamentos

```markdown
- **0.2.0** – 26/11/2024: *Dashboard com download de relatórios Excel e PDF com os gráficos.*
- **0.1.0** – 25/11/2024: *Versão Inicial*
```

---

## 📋 Licença

Este projeto está licenciado sob os termos da licença **GPL**.
