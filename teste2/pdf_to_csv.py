import os
import pdfplumber
import pypdf as pydf
import csv
from zipfile import ZipFile
import pandas as pd  # noqa


file = r"teste1/downloaded_files/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_file = r"output.csv"  # noqa E501

if os.path.exists(file):
    # Extrai texto com pypdf (como antes)
    all_tables = []
    reader = pydf.PdfReader(file)
    print(f"Total de páginas: {len(reader.pages)}")
    print(reader.pages[0].extract_text())

    # Extrai tabelas com pdfplumber
    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"\nTabelas na página {i+1}:")

            # Tenta extrair tabelas
            tables = page.extract_tables({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            })
            if tables:
                print(f'Encontradas {len(tables)} tabelas na página {i+1}')
                all_tables.extend(tables)

    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for table in all_tables:
            writer.writerows(table)

    print(f"\nExportadas {len(all_tables)} tabelas para output.csv")

    df = pd.read_csv(csv_file)
    df = df.rename(columns={
        'OD': 'Seg. Odontológica',
        'AMB': 'Seg. Ambulatoria'})
    df = df.replace({'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatoria'}, regex=True)  # noqa E501
    df.to_csv(csv_file, index=False)

    with ZipFile('Teste_Victor_Nogueira.zip', 'w') as zip:
        zip.write(csv_file)
        print(f'Arquivo {os.path.basename(csv_file)} compactado com sucesso!')
