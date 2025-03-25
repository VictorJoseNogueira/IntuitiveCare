from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from zipfile import ZipFile
import os
import time

# Configurações
DOWNLOAD_DIR = r"C:\Users\T-GAMER\Desktop\DEV pastas\IntuitiveCare\IntuitiveCare\teste1\downloaded_files"  # noqa E501
TIMEOUT = 300

URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"  # noqa E501

# Configuração do ChromeDriver
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument("--log-level=3")

# Configurar preferências para download de PDF
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True,
    "profile.default_content_settings.popups": 0
}

chrome_options.add_experimental_option("prefs", prefs)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


def wait_for_downloads(directory, timeout):
    """
    Aguarda a conclusão dos downloads dentro de um tempo limite.
    """
    elapsed_time = 0
    while elapsed_time < timeout:
        time.sleep(1)
        files = os.listdir(directory)
        if files and not any(f.endswith('.crdownload') for f in files):
            return True
        elapsed_time += 1
    return False


def click_anexo():
    try:
        print("Procurando o Anexo I...")
        # Usando CSS Selector combinando href e data-mce-href
        locator1 = (By.CSS_SELECTOR, "a[href*='Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf']")  # noqa E501
        locator2 = (By.CSS_SELECTOR, "a[href*='Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf']")  # noqa E501
        elements = [locator1, locator2]
        for i in elements:
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(i))  # noqa E501
            # Scroll para o elemento e clique
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});",  # noqa E501
                element
            )

            # Clique via JavaScript para evitar interceptação
            driver.execute_script("arguments[0].click();", element)

            print(f"Clique no Anexo {i} realizado com sucesso!")
        return True

    except Exception as e:
        print(f"Falha ao clicar no Anexo I: {str(e)}")
        return False


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


def main():
    try:
        driver.get(URL)
        if click_anexo():
            if wait_for_downloads(DOWNLOAD_DIR, TIMEOUT):
                print("Download concluído com sucesso!")
            else:
                print("Timeout ao aguardar download.")
    finally:
        time.sleep(3)
        driver.quit()

    compactar_arquivos(DOWNLOAD_DIR)


if __name__ == "__main__":
    main()
