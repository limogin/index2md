#!/usr/bin/env python3
"""
index2md - Script para generar índices y documentación
Permite manipular y facilitar la generación de documentación y prepara el proyecto
para generar índices y prepara un script para poder generar un .odt, .pdf
"""

import argparse
import os
import yaml
import glob
from pathlib import Path
from typing import List, Dict, Any


class Index2MD:
    def __init__(self, source_path: str):
        self.source_path = Path(source_path)
        self.md_files = []
        self.yaml_structure = {}
    
    def scan_markdown_files(self) -> List[Path]:
        """Recorre recursivamente la estructura de carpetas y encuentra archivos markdown"""
        self.md_files = []
        for md_file in self.source_path.rglob("*.md"):
            if md_file.is_file():
                self.md_files.append(md_file)
        return self.md_files
    
    def get_chapter_title(self, dir_path: Path) -> str:
        """Obtiene el título del capítulo para una carpeta"""
        # Buscar README.md en la carpeta
        readme_path = self.source_path / dir_path / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith('#'):
                            title = line.strip().lstrip('#').strip()
                            return title
            except Exception:
                pass
        
        # Si no hay README.md o no se puede leer, usar el nombre de la carpeta
        dir_name = str(dir_path)
        if dir_name == '.':
            return "Documentación Principal"
        else:
            return dir_name[0].upper() + dir_name[1:] if dir_name else dir_name

    def generate_markdown_index(self, output_file: str) -> None:
        """Genera un índice en formato markdown"""
        self.scan_markdown_files()
        
        # Ordenar archivos por ruta
        self.md_files.sort(key=lambda x: str(x))
        
        content = "# Índice de Documentación\n\n"
        content += f"Documentación generada desde: `{self.source_path}`\n\n"
        
        # Agrupar archivos por directorio
        files_by_dir = {}
        for md_file in self.md_files:
            relative_path = md_file.relative_to(self.source_path)
            dir_path = md_file.parent.relative_to(self.source_path)
            
            if dir_path not in files_by_dir:
                files_by_dir[dir_path] = []
            files_by_dir[dir_path].append(md_file)
        
        # Generar contenido organizado por carpetas
        for dir_path in sorted(files_by_dir.keys()):
            # Solo mostrar carpetas que tengan contenido markdown
            if files_by_dir[dir_path]:
                # Usar título del README.md de la carpeta como título del capítulo
                chapter_title = self.get_chapter_title(dir_path)
                content += f"## {chapter_title}\n\n"
                
                # Para cada archivo generar un índice de lista con enlace relativo
                for md_file in sorted(files_by_dir[dir_path]):
                    relative_path = md_file.relative_to(self.source_path)
                    
                    # Leer título del documento (primera línea que empiece con #)
                    title = md_file.stem
                    try:
                        with open(md_file, 'r', encoding='utf-8') as f:
                            for line in f:
                                if line.strip().startswith('#'):
                                    title = line.strip().lstrip('#').strip()
                                    break
                    except Exception:
                        pass
                    
                    # Generar enlace relativo a la raíz de la carpeta de documentación
                    content += f"- [{title}]({relative_path})\n"
                
                content += "\n"
        
        # Escribir archivo de salida
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Índice markdown generado: {output_file}")
    
    def generate_yaml_index(self, output_file: str) -> None:
        """Genera un índice en formato YAML con estructura jerárquica"""
        self.scan_markdown_files()
        
        # Crear estructura jerárquica
        structure = {}
        
        for md_file in self.md_files:
            relative_path = md_file.relative_to(self.source_path)
            parts = relative_path.parts
            
            current_level = structure
            for i, part in enumerate(parts[:-1]):
                if part not in current_level:
                    current_level[part] = {'type': 'directory', 'children': {}}
                current_level = current_level[part]['children']
            
            # Agregar archivo
            filename = parts[-1]
            title = md_file.stem
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip().startswith('#'):
                            title = line.strip().lstrip('#').strip()
                            break
            except Exception:
                pass
            
            current_level[filename] = {
                'type': 'file',
                'title': title,
                'path': str(relative_path)
            }
        
        # Escribir archivo YAML
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(structure, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"Índice YAML generado: {output_file}")
        self.yaml_structure = structure
    
    def concatenate_markdown_from_yaml(self, yaml_file: str, output_file: str = "all_docs.md") -> None:
        """Concatena todos los archivos Markdown en el orden especificado en el YAML"""
        # Leer el archivo YAML
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_structure = yaml.safe_load(f)
        
        concatenated_content = ""
        
        def process_structure(structure, level=0):
            nonlocal concatenated_content
            for key, value in structure.items():
                if isinstance(value, dict):
                    if value.get('type') == 'file':
                        # Es un archivo, agregarlo al contenido concatenado
                        file_path = value.get('path', key)
                        full_path = self.source_path / file_path
                        if full_path.exists():
                            try:
                                with open(full_path, 'r', encoding='utf-8') as f:
                                    file_content = f.read()
                                concatenated_content += f"\n\n{file_content}\n\n"
                                print(f"Agregado: {file_path}")
                            except Exception as e:
                                print(f"Error leyendo {file_path}: {e}")
                    elif value.get('type') == 'directory':
                        # Es un directorio, procesar sus hijos
                        children = value.get('children', {})
                        process_structure(children, level + 1)
                    else:
                        # Procesar recursivamente
                        process_structure(value, level + 1)
        
        # Procesar la estructura YAML
        process_structure(yaml_structure)
        
        # Escribir el archivo concatenado
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(concatenated_content)
        
        print(f"Archivo concatenado generado: {output_file}")

    def generate_makefile(self, index_file: str, output_file: str = "Makefile.docs") -> None:
        """Genera un Makefile para compilar la documentación"""
        # Leer el archivo YAML si existe
        yaml_structure = {}
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                yaml_structure = yaml.safe_load(f)
        
        # Determinar el archivo de entrada para Pandoc
        if index_file.endswith('.yaml') or index_file.endswith('.yml'):
            # Si es YAML, usar el archivo concatenado
            pandoc_input = "all_docs.md"
            concat_step = f"""# Concatenar archivos Markdown desde YAML
{pandoc_input}:
	python3 index2md.py -s {self.source_path} --concat-yaml {index_file} -o {pandoc_input}"""
        else:
            # Si es Markdown, usarlo directamente
            pandoc_input = index_file
            concat_step = ""
        
        makefile_content = f"""# Makefile generado por index2md
# Para compilar documentación a PDF y ODT

# Variables
SOURCE_DIR = {self.source_path}
BUILD_DIR = build
INDEX_FILE = {index_file}
PANDOC_INPUT = {pandoc_input}
PANDOC = pandoc
MERMAID_FILTER = mermaid-filter

# Crear directorio de build si no existe
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Concatenar archivos Markdown desde YAML (si es necesario)
{concat_step}
# Compilar a PDF
pdf: $(BUILD_DIR) {pandoc_input}
	$(PANDOC) $(PANDOC_INPUT) \\
		--from markdown \\
		--to pdf \\
		--output $(BUILD_DIR)/documentacion.pdf \\
		--filter $(MERMAID_FILTER) \\
		--toc \\
		--number-sections

# Compilar a ODT
odt: $(BUILD_DIR) {pandoc_input}
	$(PANDOC) $(PANDOC_INPUT) \\
		--from markdown \\
		--to odt \\
		--output $(BUILD_DIR)/documentacion.odt \\
		--filter $(MERMAID_FILTER) \\
		--toc

# Compilar todo
all: pdf odt

# Limpiar archivos generados
clean:
	rm -rf $(BUILD_DIR) {pandoc_input}

# Instalar dependencias (Ubuntu/Debian)
install-deps:
	sudo apt-get update
	sudo apt-get install -y pandoc
	pip install mermaid-filter

# Instalar dependencias (macOS)
install-deps-macos:
	brew install pandoc
	pip install mermaid-filter

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make -f Makefile.docs pdf      - Generar PDF"
	@echo "  make -f Makefile.docs odt      - Generar ODT"
	@echo "  make -f Makefile.docs all      - Generar PDF y ODT"
	@echo "  make -f Makefile.docs clean    - Limpiar archivos generados"
	@echo "  make -f Makefile.docs install-deps - Instalar dependencias (Ubuntu/Debian)"
	@echo "  make -f Makefile.docs install-deps-macos - Instalar dependencias (macOS)"
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(makefile_content)
        
        print(f"Makefile generado: {output_file}")
    
    def generate_mkdocs_yaml(self, output_file: str = "mkdocs.yml") -> None:
        """Genera un archivo YAML preparado para usar con MkDocs"""
        self.scan_markdown_files()
        
        # Ordenar archivos por ruta
        self.md_files.sort(key=lambda x: str(x))
        
        # Estructura base de MkDocs
        mkdocs_config = {
            'site_name': 'Documentación del Proyecto',
            'site_description': 'Documentación generada automáticamente',
            'site_author': 'index2md',
            'repo_url': 'https://github.com/yourusername/project',
            'edit_uri': 'edit/main/docs/',
            'docs_dir': str(self.source_path),
            'site_dir': 'site',
            'theme': {
                'name': 'material',
                'features': [
                    'navigation.tabs',
                    'navigation.sections',
                    'navigation.expand',
                    'navigation.top',
                    'search.highlight',
                    'search.share'
                ]
            },
            'nav': []
        }
        
        # Agrupar archivos por directorio
        files_by_dir = {}
        for md_file in self.md_files:
            relative_path = md_file.relative_to(self.source_path)
            dir_path = md_file.parent.relative_to(self.source_path)
            
            if dir_path not in files_by_dir:
                files_by_dir[dir_path] = []
            files_by_dir[dir_path].append(md_file)
        
        # Generar navegación para MkDocs
        navigation = []
        
        # Procesar archivos en la raíz primero
        if Path('.') in files_by_dir and files_by_dir[Path('.')]:
            root_files = []
            for md_file in sorted(files_by_dir[Path('.')]):
                relative_path = md_file.relative_to(self.source_path)
                title = md_file.stem
                
                # Leer título del documento
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip().startswith('#'):
                                title = line.strip().lstrip('#').strip()
                                break
                except Exception:
                    pass
                
                root_files.append({title: str(relative_path)})
            
            if root_files:
                navigation.extend(root_files)
        
        # Procesar archivos en subdirectorios
        for dir_path in sorted(files_by_dir.keys()):
            if dir_path == Path('.'):
                continue
                
            if files_by_dir[dir_path]:
                # Usar título del README.md de la carpeta como título del capítulo
                chapter_title = self.get_chapter_title(dir_path)
                
                section_files = []
                for md_file in sorted(files_by_dir[dir_path]):
                    relative_path = md_file.relative_to(self.source_path)
                    title = md_file.stem
                    
                    # Leer título del documento
                    try:
                        with open(md_file, 'r', encoding='utf-8') as f:
                            for line in f:
                                if line.strip().startswith('#'):
                                    title = line.strip().lstrip('#').strip()
                                    break
                    except Exception:
                        pass
                    
                    section_files.append({title: str(relative_path)})
                
                if section_files:
                    navigation.append({chapter_title: section_files})
        
        mkdocs_config['nav'] = navigation
        
        # Escribir archivo YAML
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(mkdocs_config, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        print(f"Archivo YAML de MkDocs generado: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="index2md - Generador de índices y documentación",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 index2md.py -s ./source-folder -i -o=00index.md
  python3 index2md.py --source ./source-folder --index --output=00index.yaml
  python3 index2md.py -s ./source-folder -m -f=00index.yaml
  python3 index2md.py -s ./source-folder -m -f=00index.yaml -o=Makefile.docs
  python3 index2md.py -s ./source-folder -k
        """
    )
    
    parser.add_argument(
        '-s', '--source',
        required=True,
        help='Ruta de la carpeta fuente con documentación'
    )
    
    parser.add_argument(
        '-i', '--index',
        action='store_true',
        help='Generar índice'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Archivo de salida para el índice'
    )
    
    parser.add_argument(
        '-m', '--makefile',
        action='store_true',
        help='Generar Makefile'
    )
    
    parser.add_argument(
        '-f', '--index-file',
        help='Archivo de índice YAML para usar en el Makefile'
    )
    
    parser.add_argument(
        '-k', '--mkdocs',
        action='store_true',
        help='Generar archivo YAML para MkDocs'
    )
    
    parser.add_argument(
        '--concat-yaml',
        help='Concatenar archivos Markdown desde archivo YAML'
    )
    
    args = parser.parse_args()
    
    # Verificar que la carpeta fuente existe
    if not os.path.exists(args.source):
        print(f"Error: La carpeta fuente '{args.source}' no existe")
        return 1
    
    index2md = Index2MD(args.source)
    
    # Generar índice markdown
    if args.index and args.output and args.output.endswith('.md'):
        index2md.generate_markdown_index(args.output)
    
    # Generar índice YAML
    elif args.index and args.output and args.output.endswith('.yaml'):
        index2md.generate_yaml_index(args.output)
    
    # Generar Makefile
    elif args.makefile:
        index_file = args.index_file or "00index.yaml"
        output_file = args.output or "Makefile.docs"
        index2md.generate_makefile(index_file, output_file)
    
    # Generar archivo YAML para MkDocs
    elif args.mkdocs:
        index2md.generate_mkdocs_yaml()
    
    # Concatenar archivos Markdown desde YAML
    elif args.concat_yaml:
        output_file = args.output or "all_docs.md"
        index2md.concatenate_markdown_from_yaml(args.concat_yaml, output_file)
    
    else:
        print("Error: Especifica una operación válida")
        print("  --index --output=archivo.md  para generar índice markdown")
        print("  --index --output=archivo.yaml para generar índice YAML")
        print("  --makefile --index-file=archivo.yaml para generar Makefile")
        print("  --mkdocs para generar archivo YAML para MkDocs")
        print("  --concat-yaml archivo.yaml --output=salida.md para concatenar archivos")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main()) 