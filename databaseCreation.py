demonstrativos = """
CREATE TABLE demonstrativos_contabeis (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    reg_ans INT NOT NULL,
    CD_CONTA_CONTABIL INT NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    VL_SALDO_INICIAL NUMERIC(15,2) NOT NULL,
    VL_SALDO_FINAL NUMERIC(15,2) NOT NULL
);
"""

relatorio = """
CREATE TABLE relatorio_cadop(
    id SERIAL PRIMARY KEY,
    registro_ans INT NOT NULL,
    cnpj VARCHAR(14) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100) NOT NULL,
    logradouro VARCHAR(255) NOT NULL,
    numero VARCHAR(20) NOT NULL,
    complemento VARCHAR(255),
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    cep VARCHAR(8) NOT NULL,
    ddd CHAR(2),
    telefone VARCHAR(15),
    fax VARCHAR(15),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255) NOT NULL,
    cargo_representante VARCHAR(255) NOT NULL,
    regiao_comercializacao INT,
    data_registro_ans DATE NOT NULL
);
"""
