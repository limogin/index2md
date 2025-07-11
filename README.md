# index2md 

## Objetivos 

Script en python que permite manipular y facilita la generación de documentación y prepara el proyecto de documentación para generar índices y prepara un script para poder generar un .odt, .pdf 

Por parámetro se le pasa la ruta donde está ubicada la documentación. En la raíz de la misma generará los archivos que necesite si procede, y también la operación a realizar. 

## Funciones

- Recorre una estructura de carpetas de forma recursiva y genera un archivo índice con referencias a todos los documentos markdown encontrados. 

- Crea un archivo yml con la relación de todos los archivos encontrados referenciados también por carpetas de forma jerárquica. 

- Genera un Makefile con la información necesaria para crear un build en odt y pdf en una carpeta build de salida de toda la información contenida en este documento yaml previamente generado. Para este proceso usa pandoc y usa el filtro mermaid para procesar todas las gráficas contenidas en la documentación. 

- Genera un archivo yml preparado para usar con mkdocs y usar la documentación con esta aplicación 

## Generación de documento indice 

Para generar el índice en markdown usará un título para cada carpeta encontrada (siempre que tenga contenido en markdown). Los títulos de las carpetas se generan con la primera letra en mayúscula.

Para cada archivo genera un índice de lista con un enlace relativo a la raíz de la carpeta de documentación y un título que corresponderá al título del documento encontrado. 

El archivo README.md de cada carpeta será el primero en cargar que corresponda a esa carpeta y sobre el que usará el titulo del mismo como referencia del capítulo que corresponde.

## Instalación

### Instalación rápida

```bash
# Clonar el repositorio
git clone https://github.com/yourusername/index2md.git
cd index2md

# Instalar dependencias y compilar
make install-deps build install
```

### Instalación manual

```bash
# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# Instalar dependencias de Python
pip3 install -r requirements.txt

# Compilar con PyInstaller
pyinstaller --onefile index2md.py

# Instalar en el sistema
sudo cp dist/index2md /usr/local/bin/
sudo chmod +x /usr/local/bin/index2md
```

### Usar con entorno virtual

```bash
# Crear entorno virtual
make venv

# Activar entorno virtual
source venv/bin/activate

# Instalar en entorno virtual
make install-venv

# Usar el script
python3 index2md.py --help
```

## Comandos 

### Generar un índice en markdown 

```bash
# Usando opciones cortas
python3 index2md.py -s ./source-folder -i -o=00index.md

# Usando opciones largas
python3 index2md.py --source ./source-folder --index --output=00index.md
```

### Generar un índice en yaml 

```bash
# Usando opciones cortas
python3 index2md.py -s ./source-folder -i -o=00index.yaml

# Usando opciones largas
python3 index2md.py --source ./source-folder --index --output=00index.yaml
```

### Generar un Makefile para la documentación

```bash
# Usando opciones cortas
en python3 index2md.py -s ./source-folder -m -f=00index.yaml
# Esto generará Makefile.docs por defecto

# Usando opciones largas
python3 index2md.py --source ./source-folder --makefile --index-file=00index.yaml
# Esto generará Makefile.docs por defecto

# Si quieres un nombre diferente:
python3 index2md.py -s ./source-folder -m -f=00index.yaml -o=OtroMakefile
```

> **Nota:** El Makefile generado para la documentación se llama por defecto `Makefile.docs` para no sobrescribir el Makefile principal del proyecto. Para compilar la documentación, usa:

```bash
make -f Makefile.docs pdf
make -f Makefile.docs odt
make -f Makefile.docs all
```

### Generar archivo YAML para MkDocs

```bash
# Usando opciones cortas
python3 index2md.py -s ./source-folder -k

# Usando opciones largas
python3 index2md.py --source ./source-folder --mkdocs
```

### Ejemplos de uso

```bash
# Crear estructura de ejemplo y generar índices
en make example-index

# Ejecutar tests básicos
make test

# Ver todos los comandos disponibles
en make help
```

### Ejemplo de salida

El script genera un índice markdown con esta estructura:

```markdown
# Índice de Documentación

Documentación generada desde: `./docs`

## Documentación Principal

- [Documentación del Proyecto](README.md)

## Introducción

- [Introducción al Proyecto](intro/01-introduccion.md)

## Instalación

- [Guía de Instalación](instalacion/02-instalacion.md)

## Uso

- [Guía de Uso](uso/03-uso.md)
```

### Ejemplo de archivo YAML para MkDocs

El script genera un archivo `mkdocs.yml` con esta estructura:

```yaml
site_name: Documentación del Proyecto
site_description: Documentación generada automáticamente
site_author: index2md
repo_url: https://github.com/yourusername/project
edit_uri: edit/main/docs/
docs_dir: ./docs
site_dir: site
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.highlight
    - search.share
nav:
  - Documentación del Proyecto: README.md
  - Introducción:
    - Introducción al Proyecto: intro/01-introduccion.md
  - Instalación:
    - Guía de Instalación: instalacion/02-instalacion.md
  - Uso:
    - Guía de Uso: uso/03-uso.md
```

## Diferencia entre Makefile principal y Makefile.docs

- El **Makefile** principal del proyecto sirve para compilar, instalar y gestionar la aplicación index2md.
- El **Makefile.docs** es generado automáticamente para compilar la documentación (PDF, ODT, etc.) y nunca sobrescribe el Makefile principal.

Para compilar la documentación, siempre usa:

```bash
make -f Makefile.docs pdf
```

## Comandos del Makefile

### Instalación y compilación

```bash
make install-deps          # Instalar dependencias de Python
make install-system-deps   # Instalar dependencias del sistema (Ubuntu/Debian)
make build                 # Compilar con PyInstaller
make build-optimized       # Compilar con optimizaciones
make install               # Instalar en el sistema (/usr/local/bin)
make install-local         # Instalar en directorio local (~/.local/bin)
```

### Desarrollo y testing

```bash
make venv                 # Crear entorno virtual
make install-venv         # Instalar en entorno virtual
make test                 # Ejecutar tests básicos
make clean                # Limpiar archivos generados
```

### Ejemplos

```bash
make create-example       # Crear estructura de ejemplo
make example-index        # Generar índices de ejemplo
```

## Dependencias

### Python
- PyYAML >= 6.0
- pathlib2 >= 2.3.7 (para Python < 3.4)

### Sistema (para compilar documentación)
- pandoc
- mermaid-filter

## Estructura del proyecto

```
index2md/
├── index2md.py          # Script principal
├── requirements.txt      # Dependencias de Python
├── setup.py             # Script de instalación
├── Makefile             # Makefile principal
├── index2md.spec        # Configuración de PyInstaller
├── .gitignore           # Archivos a ignorar
└── README.md            # Este archivo
```

## Licencia

GPL3.0 License








