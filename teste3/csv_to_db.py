import csv  # noqa
import dotenv  # noqa
import os  # noqa
import mysql.connector  # noqa
import pandas as pd  # noqa
import time  # noqa

# Carregar variáveis de ambiente
dotenv.load_dotenv()
# Credenciais do banco de dados
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

create_database_relatorio = """
CREATE TABLE IF NOT EXISTS relatorio_cadop (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    registro_ans INT NOT NULL,
    cnpj VARCHAR(14) NOT NULL,
    razao_social VARCHAR(140),
    nome_fantasia VARCHAR(140),
    modalidade VARCHAR(3),
    logradouro VARCHAR(40),
    numero VARCHAR(20),
    complemento VARCHAR(40),
    bairro VARCHAR(30),
    cidade VARCHAR(30),
    uf CHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(4),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(50),
    cargo_representante VARCHAR(40),
    regiao_comercializacao INT,
    data_registro_ans DATE,
    UNIQUE KEY uk_registro_ans_cnpj (registro_ans, cnpj)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

query_relatorio = """
INSERT IGNORE INTO relatorio_cadop (
    registro_ans, cnpj, razao_social, nome_fantasia, modalidade,
    logradouro, numero, complemento, bairro, cidade, uf, cep,
    ddd, telefone, fax, endereco_eletronico, representante,
    cargo_representante, regiao_comercializacao, data_registro_ans
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""   # noqa E501

create_database_demonstrativos = """
CREATE TABLE IF NOT EXISTS demonstrativos_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    reg_ans INT NOT NULL,
    CD_CONTA_CONTABIL INT NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    VL_SALDO_INICIAL DECIMAL(15,2),
    VL_SALDO_FINAL DECIMAL(15,2),
    UNIQUE KEY uk_dados_unicos (data, reg_ans, CD_CONTA_CONTABIL, descricao),
    INDEX idx_descricao (descricao)  -- Índice adicionado diretamente na criação
) ENGINE=InnoDB;
"""  # noqa E501

query_demonstrativos = """
INSERT INTO demonstrativos_contabeis (
    data,reg_ans,CD_CONTA_CONTABIL,descricao,VL_SALDO_INICIAL,VL_SALDO_FINAL
) VALUES (
    %s, %s, %s, %s, %s, %s
)
"""   # noqa E501
list_files = [
    "teste3/data/4T2024.csv",
    "teste3/data/3T2024.csv",
    "teste3/data/2T2024.csv",
    "teste3/data/1T2024.csv",
    "teste3/data/4T2023.csv",
    "teste3/data/3T2023.csv",
    "teste3/data/2T2023.csv",
    "teste3/data/1T2023.csv",
]
file_path_csv = r'teste3\data\Relatorio_cadop.csv'


def convert_nan_to_none(valor):
    """Converte valores NaN/NaT do pandas para None (NULL no banco de dados)."""  # noqa E501
    return None if pd.isna(valor) else valor


def convert_comma_into_period(value):
    """Converte valores com virgula para pontos."""
    if isinstance(value, str):
        return value.replace(",", ".")
    return value


def convert_date_format(value):
    if isinstance(value, str):
        if len(value.split('/')) == 3 and len(value) == 10:
            try:
                day, month, year = value.split('/')
                if len(day) == 2 and len(month) == 2 and len(year) == 4:
                    return f"{year}-{month}-{day}"
            except ValueError:
                pass
    return value


def insert_list_on_db(db, create_database_demonstrativos, list_files, query_demonstrativos, batch_size = 20000):  # noqa E501
    """
    Insere dados de arquivos CSV no banco de dados MySQL.
    Args:
        db: Conexão com o banco de dados
        criar_tabela_sql: Comando SQL para criação da tabela
        lista_arquivos: Lista de caminhos para arquivos CSV
        query_insercao: Query SQL para inserção dos dados
        tamanho_lote: Tamanho do lote para processamento (default: 20000)
    """
    if db.is_connected():
        print("Conectado ao banco de dados MySQL")
    else:
        print("Nenhuma conexão estabelecida")
    try:
        cursor = db.cursor()
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        cursor = None

    for file_csv in list_files:
        print(f"Processando {file_csv}")
        batch_size = batch_size
        for chunk in pd.read_csv(file_csv, chunksize=batch_size, sep=';'):
            data = [
                tuple(
                    convert_nan_to_none(
                        convert_comma_into_period(convert_date_format(value))
                        ) for value in row
            )   # noqa E501
                for row in chunk.itertuples(index=False, name=None)
            ]

            if cursor:
                try:
                    cursor.execute(create_database_demonstrativos)
                    cursor.executemany(query_demonstrativos, data)
                    db.commit()  # Add this line to commit the transaction
                    print(f"Inserted {cursor.rowcount} rows")  # noqa
                except mysql.connector.Error as err:
                    print(f"Erro ao executar consulta SQL: {err}")
                    db.rollback()  # Rollback on error


def insert_csv_on_db(db, create_database_relatorio, file_path_csv, query_relatorio,  batch_size = 20000):  # noqa E501
    db = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    if db.is_connected():
        print("Conectado ao banco de dados MySQL")
    else:
        print("Nenhuma conexão estabelecida")
    try:
        cursor = db.cursor()
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        cursor = None

    batch_size = batch_size
    for chunk in pd.read_csv(file_path_csv, chunksize=batch_size, sep=';'):
        data = [
                tuple(
                    convert_nan_to_none(
                        convert_comma_into_period(convert_date_format(value))
                        ) for value in row
            )   # noqa E501
                for row in chunk.itertuples(index=False, name=None)
            ]

    if cursor:
        try:
            cursor.execute(create_database_relatorio)
            cursor.executemany(query_relatorio, data)
            db.commit()  # Add this line to commit the transaction
            print(f"Inserted {cursor.rowcount} rows")  # noqa
        except mysql.connector.Error as err:
            print(f"Erro ao executar consulta SQL: {err}")
            db.rollback()  # Rollback on error
    cursor.close()
    db.close()


def main():
    initial_time = time.time()
    db = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    insert_csv_on_db(db, create_database_relatorio, file_path_csv, query_relatorio)  # noqa E501
    insert_list_on_db(db, create_database_demonstrativos, list_files, query_demonstrativos)  # noqa E501

    db.close()
    print(f"Tempo de execução: {time.time() - initial_time:.2f} segundos")


if __name__ == "__main__":
    main()
