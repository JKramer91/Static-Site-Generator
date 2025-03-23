import shutil
import os
from copy_directory import source_to_destination
from generate import generate_page, generate_pages_recursive

static_path = "./static"
public_path = "./public"

def main():
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
    source_to_destination(static_path, public_path)
    generate_pages_recursive("./content", "./template.html", "./public")

main()