from textnode import TextNode, TextType
from markdown import extract_title, markdown_to_html_node
import os
import shutil
import sys

#shutil.copytree() could be used instead, but for the purposes of practicing recursion the following was used
def copy_dir_to_public(source_dir, dest_dir):
    for filename in os.listdir(source_dir):
        from_path = os.path.join(source_dir, filename)
        to_dir = os.path.join(dest_dir, filename)
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_dir)
        if os.path.isdir(from_path):
            if not os.path.exists(to_dir):
                os.mkdir(f"{to_dir}")
            copy_dir_to_public(from_path, to_dir)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file_object:
        from_path_file_contents = file_object.read()

    with open(template_path) as file_object:
        template_path_file_contents = file_object.read()   

    html_string = markdown_to_html_node(from_path_file_contents).to_html()
    title = extract_title(from_path_file_contents)

    template_path_file_contents = template_path_file_contents.replace("{{ Title }}", title).replace("{{ Content }}", html_string).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if len(dest_dir_path) > 0:
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as file_object:
        file_object.write(template_path_file_contents)

def generate_pages(dir, basepath):
    home_dir_path = "/home/bwalla796/workspace/github.com/bwalla796/staticsite"
    content_root = home_dir_path + "/content"
    public_root = home_dir_path + "/docs"
    if os.path.isdir(dir):
        for filename in os.listdir(dir):
            path = os.path.join(dir, filename)
            if os.path.isdir(path):
                generate_pages(path, basepath)
            if os.path.isfile(path) and path.endswith(".md"):
                dest_path = path.replace("content", "docs", 1).rstrip(".md") + ".html"
                generate_page(path, f"{home_dir_path}/template.html", dest_path, basepath)    

def main():
    if len(sys.argv) > 0:
        basepath = sys.argv[1]
    else:
        basepath = "/"    

    home_dir_path = "/home/bwalla796/workspace/github.com/bwalla796/staticsite"
    content_root = home_dir_path + "/content"
    public_root = home_dir_path + "/docs"
    if os.path.isdir(public_root):
        shutil.rmtree(public_root)
    os.mkdir(public_root)
    copy_dir_to_public(content_root, public_root)

    generate_pages(f"{home_dir_path}/content", basepath)

main()    