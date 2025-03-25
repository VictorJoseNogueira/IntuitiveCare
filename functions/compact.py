import os
from zipfile import ZipFile


def compactar_arquivos(diretorio, nome_arquivo):
    if not os.path.exists(diretorio):
        print(f"O diretório {diretorio} não existe!")
        return
    arquivos = os.listdir(diretorio)

    if not arquivos:
        print("nenhum arquivo encontrado para compactar")
        return
    with ZipFile(f'{nome_arquivo}.zip', 'a') as zip:
        for arquivo in arquivos:
            caminho_completo = os.path.join(diretorio, arquivo)
            if os.path.isfile(caminho_completo):
                try:
                    zip.write(caminho_completo, arquivo)
                    print(f'Arquivo {arquivo} adicionado ao ZIP')
                except Exception as e:
                    print(f'Erro ao compactar {arquivo}: {str(e)}')
            else:
                print(f'{arquivo} não é um arquivo (ignorado)')

    print('Compactação concluída com sucesso!')
