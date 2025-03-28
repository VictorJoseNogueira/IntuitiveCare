import subprocess
import os


def main():
    frontend_path = os.path.abspath("teste4/frontend")

    # Iniciar o backend
    backend = subprocess.Popen(["py", "teste4/backend/testes.py"])

    # Iniciar o frontend
    frontend = subprocess.Popen(["npm", "run", "serve"], cwd=frontend_path, shell=True)  # noqa E501

    # Aguardar os processos terminarem
    backend.wait()
    frontend.wait()


if __name__ == "__main__":
    main()
