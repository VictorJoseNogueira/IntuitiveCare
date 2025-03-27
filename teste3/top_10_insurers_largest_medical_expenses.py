import dotenv
import os  # noqa
import mysql.connector  # noqa

# Carregar variáveis de ambiente
dotenv.load_dotenv()
# Credenciais do banco de dados
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
BLUE = "\033[1;34m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"


def main():
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

    cursor.execute("""
    SELECT 
        d.reg_ans AS operadora,
        SUM(CAST(d.VL_SALDO_FINAL AS DECIMAL(15, 2))) AS total_despesas,
        r.registro_ans as registro_agencia,
        r.razao_social
    FROM 
        demonstrativos_contabeis as d
    INNER JOIN relatorio_cadop as r on d.reg_ans = r.registro_ans
    WHERE d.descricao Like "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%"
        AND d.data = '2024-10-01'
    GROUP BY 
        d.reg_ans, r.registro_ans, r.razao_social
    ORDER BY 
        total_despesas DESC
    LIMIT 10;
            """)  # noqa E501
    results_last_quarter = cursor.fetchall()

    # Cores ANSI

    print("Top 10 operadoras com mais despesas:\n")
    for row in results_last_quarter:
        print(
            f"{BLUE}{row[0]}{RESET}",
            f"{RED}{row[2]}{RESET}",
            f"{MAGENTA}{row[3]} -{RESET}",
            f"{GREEN}R$ {row[1]}{RESET}",
        )

    cursor.execute("""
    SELECT 
        d.reg_ans AS operadora,
        SUM(CAST(d.VL_SALDO_FINAL AS DECIMAL(15, 2))) AS total_despesas,
        r.registro_ans as registro_agencia,
        r.razao_social
    FROM 
        demonstrativos_contabeis as d
    INNER JOIN relatorio_cadop as r on d.reg_ans = r.registro_ans
    WHERE d.descricao Like "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%"
        AND d.data LIKE '2024%'
    GROUP BY 
        d.reg_ans, r.registro_ans, r.razao_social
    ORDER BY 
        total_despesas DESC
    LIMIT 10;
            """)  # noqa E501
    results_last_year = cursor.fetchall()
    print("Top 10 operadoras com mais despesas no ano:\n")
    for row in results_last_year:
        print(
            f"{BLUE}{row[0]}{RESET}",
            f"{RED}{row[2]}{RESET}",
            f"{MAGENTA}{row[3]} -{RESET}",
            f"{GREEN}R$ {row[1]}{RESET}",
        )

    db.close()


if __name__ == '__main__':
    main()
