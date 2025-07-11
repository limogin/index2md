# Makefile principal para el proyecto index2md

# Variables
PYTHON = python3
PIP = pip3
PYINSTALLER = pyinstaller
PROJECT_NAME = index2md
SCRIPT_NAME = index2md.py
DIST_DIR = dist
BUILD_DIR = build
SPEC_FILE = $(PROJECT_NAME).spec

# Comandos principales
.PHONY: all install-deps build install clean help test

all: install-deps build

install-deps:
	$(PIP) install -r requirements.txt

build: install-deps
	$(PYINSTALLER) --onefile --name $(PROJECT_NAME) $(SCRIPT_NAME)

install: build
	sudo cp $(DIST_DIR)/$(PROJECT_NAME) /usr/local/bin/
	sudo chmod +x /usr/local/bin/$(PROJECT_NAME)

install-local: build
	mkdir -p ~/.local/bin
	cp $(DIST_DIR)/$(PROJECT_NAME) ~/.local/bin/
	chmod +x ~/.local/bin/$(PROJECT_NAME)

uninstall:
	sudo rm -f /usr/local/bin/$(PROJECT_NAME)
	rm -f ~/.local/bin/$(PROJECT_NAME)

clean:
	rm -rf $(DIST_DIR) $(BUILD_DIR) __pycache__ *.spec venv

venv:
	$(PYTHON) -m venv venv

install-venv: venv
	venv/bin/pip install -r requirements.txt
	@echo "Activa el entorno con: source venv/bin/activate"
	@echo "Ejecuta: python3 index2md.py --help"

help:
	@echo "Comandos disponibles:"
	@echo "  make install-deps      - Instalar dependencias de Python"
	@echo "  make build             - Compilar con PyInstaller"
	@echo "  make install           - Instalar en el sistema (/usr/local/bin)"
	@echo "  make install-local     - Instalar en ~/.local/bin"
	@echo "  make uninstall         - Desinstalar"
	@echo "  make clean             - Limpiar archivos generados"
	@echo "  make venv              - Crear entorno virtual"
	@echo "  make install-venv      - Instalar en entorno virtual"
	@echo "  make help              - Mostrar esta ayuda"
