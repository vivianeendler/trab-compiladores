# Makefile para o Compilador Homi

PYTHON = python3
MAIN = main.py
ARQUIVO_TESTE = exemplo1_luz.homi

all: run

run:
	@echo "Iniciando o compilador Homi com $(ARQUIVO_TESTE)..."
	$(PYTHON) $(MAIN) $(ARQUIVO_TESTE)

clean:
	@echo "Limpando arquivos temporários do Python..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

help:
	@echo "Comandos disponíveis:"
	@echo "  make run   - Executa o compilador (main.py)"
	@echo "  make clean - Remove arquivos compilados do python"