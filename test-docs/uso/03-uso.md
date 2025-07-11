# Guía de Uso

Cómo usar la herramienta index2md.

## Comandos Básicos

### Generar índice markdown

```bash
python3 index2md.py -s ./docs -i -o=00index.md
```

### Generar índice YAML

```bash
python3 index2md.py -s ./docs -i -o=00index.yaml
```

### Generar Makefile

```bash
python3 index2md.py -s ./docs -m -f=00index.yaml
```

## Opciones Disponibles

- `-s, --source`: Carpeta fuente con documentación
- `-i, --index`: Generar índice
- `-o, --output`: Archivo de salida
- `-m, --makefile`: Generar Makefile
- `-f, --index-file`: Archivo de índice YAML
- `-k, --mkdocs`: Generar archivo YAML para MkDocs 