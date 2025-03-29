# Testes de Nivelamento v.250321

## 📌 Descrição
Este repositório contém a implementação dos testes de nivelamento v.250321, divididos em quatro etapas principais:

1. **Web Scraping**: Download e compactação de arquivos PDF.
2. **Transformação de Dados**: Extração e conversão de dados de PDF para CSV.
3. **Banco de Dados**: Importação e análise de dados financeiros das operadoras.
4. **API Web**: Interface web para busca textual de operadoras.

---

## 📁 Estrutura do Repositório

```
/
├── functions
│   ├── __init__.py
│   ├── compact.py               # script contendo uma function para compactar arquivos 
├── teste1
│   ├── python_web_scraping.py  # Script para baixar e compactar os arquivos
│   ├── downloaded_files/        # Pasta onde os arquivos baixados serão salvos
│
├── teste2
│   ├── pdf_to_csv.py           # Script para converter dados do PDF para CSV e compactar
│
├── teste3
│   ├── data/                   # Pasta contendo arquivos necessários
│   ├── healthcare_operators_financial_importer.py  # Script para inserir dados no banco
│   ├── top_10_insurers_largest_medical_expenses.py  # Script para analisar as maiores despesas
│
├── teste4
│   ├── backend/                # Backend em Python (API para busca textual)
│   ├── frontend/               # Frontend em Vue.js (Interface web)
│   ├── postman/                # Coleção do Postman para testes da API
│   ├── start.py                # Script para iniciar o servidor e o frontend
│
├── requirements.txt            # Dependências do backend em Python
├── .env-example                # Exemplo de arquivo .env para configuração
├── README.md                   # Documentação do projeto
```

---

## 🛠 Requisitos
- As dependências do backend estão listadas no arquivo `requirements.txt`.
- As dependências do frontend estão listadas no arquivo `teste4/frontend/package.json`.

---

## 🚀 Instruções de Uso

### 1️⃣ Teste de Web Scraping
```bash
cd teste1
python python_web_scraping.py
```
Os arquivos serão salvos na pasta `downloaded_files/` e compactados automaticamente.

### 2️⃣ Teste de Transformação de Dados
```bash
cd teste2
python pdf_to_csv.py
```
O CSV gerado será compactado no formato `teste{seu_nome}.zip`.

### 3️⃣ Teste de Banco de Dados
- Configure a conexão com o banco de dados no arquivo `.env`.
```bash
cd teste3
python healthcare_operators_financial_importer.py
python top_10_insurers_largest_medical_expenses.py
```
Os dados serão importados para o banco, e os 10 maiores gastos serão exibidos.

### 4️⃣ Teste de API
#### Inicialização do backend e frontend:
```bash
python teste4/start.py
```
A interface estará disponível para interação.

---

## ⚠️ Observações
- Para garantir a execução correta, preencha o `.env` com as credenciais adequadas.

## 📄 Exemplo de Configuração `.env`
Crie um arquivo `.env` na raiz do projeto com o seguinte formato:

```ini
# Configurações do Banco de Dados
# Informe o endereço do servidor do banco de dados (localhost ou IP do servidor)
DB_HOST="SEU HOSTNAME"  # Ex: localhost ou 192.168.1.100

# Informe a porta em que o banco de dados está escutando
# Para MySQL, a porta padrão é 3306
DB_PORT=3306  # Porta padrão do MySQL

# Informe o nome de usuário com acesso ao banco de dados
DB_USER="SEU NOME DE USUARIO"  # Ex: root ou admin

# Informe a senha do banco de dados
DB_PASSWORD="SUA SENHA"  # Ex: sua_senha_aqui

# Informe o nome do banco de dados que será utilizado
DB_NAME="NOME DO BANCO DE DADOS"  # Ex: minha_base_de_dados

```

---
---

## 📞 Contato
Caso tenha dúvidas ou sugestões, entre em contato com o responsável pelo repositório.

