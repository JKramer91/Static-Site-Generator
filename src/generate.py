import os
import shutil
from pathlib import Path
from blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown_content = file.read()
    
    with open(template_path, 'r') as file:
        template = file.read()

    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    if basepath != "/" and not basepath.endswith("/"):
        basepath += "/"
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(dest_path, 'w') as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    directory = os.listdir(dir_path_content)

    for file in directory:
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.splitext(from_path)[1].lower() == ".md":
            html_extension = Path(file).with_suffix(".html")
            dest_path_html = os.path.join(dest_dir_path, html_extension)
            generate_page(from_path, template_path, dest_path_html, basepath)
        elif os.path.isfile(from_path):
            shutil.copy(from_path, dest_dir_path)
        else:
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            print(line[2:])
            return line[2:]
    raise Exception
    