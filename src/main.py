import shutil
import os
import sys
from copy_directory import source_to_destination
from generate import generate_page, generate_pages_recursive

static_path = "./static"
public_path = "./public"

def main():
    basepath = ""
    if sys.argv[0]:
        basepath = sys.argv[0]
    else:
        basepath = "/"
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
    source_to_destination(static_path, public_path)
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

main()