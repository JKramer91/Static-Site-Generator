import shutil
import os
import sys
from copy_directory import source_to_destination
from generate import generate_page, generate_pages_recursive

static_path = "./static"
public_path = "./docs"
content_path = "./content"
template_path = "./template.html"
default_path = "/"

def main():
    basepath = default_path
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
    source_to_destination(static_path, public_path)
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

main()