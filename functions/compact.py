from zipfile import ZipFile
import os


def compactar_arquivos(diretorio):
    if os.path.exists(diretorio):
        arquivos = os.listdir(diretorio)
        for arquivo in arquivos:
            print(f'- {arquivo}')
        caminho_completo = os.path.join(diretorio, arquivo)
        # Verifica se é um arquivo (não subdiretório)
        if os.path.isfile(caminho_completo):
            try:
                with ZipFile('anexos_compactados.zip', 'a') as zip:
                    zip.write(caminho_completo, arquivo)
                print(f'Arquivo {arquivo} adicionado ao ZIP')
            except Exception as e:
                print(f'Erro ao compactar {arquivo}: {str(e)}')
        else:
            print(f'{arquivo} não é um arquivo (ignorado)')

    print('Compactação concluída com sucesso!')
