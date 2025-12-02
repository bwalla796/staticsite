from textnode import TextNode, TextType
from markdown import extract_title, markdown_to_html_node
import os
import shutil

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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file_object:
        from_path_file_contents = file_object.read()

    with open(template_path) as file_object:
        template_path_file_contents = file_object.read()   

    html_string = markdown_to_html_node(from_path_file_contents).to_html()
    title = extract_title(from_path_file_contents)

    template_path_file_contents = template_path_file_contents.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    dest_dir_path = os.path.dirname(dest_path)
    if len(dest_dir_path) > 0:
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as file_object:
        file_object.write(template_path_file_contents)

def generate_pages(dir):
    home_dir_path = "/home/bwalla796/workspace/github.com/bwalla796/staticsite"
    content_root = home_dir_path + "/content"
    public_root = home_dir_path + "/public"
    if os.path.isdir(dir):
        for filename in os.listdir(dir):
            path = os.path.join(dir, filename)
            if os.path.isdir(path):
                generate_pages(path)
            if os.path.isfile(path) and path.endswith(".md"):
                dest_path = path.replace("content", "public", 1).rstrip(".md") + ".html"
                generate_page(path, f"{home_dir_path}/template.html", dest_path)    

def main():
    home_dir_path = "/home/bwalla796/workspace/github.com/bwalla796/staticsite"
    if os.path.isdir(f"{home_dir_path}/public"):
        shutil.rmtree(f"{home_dir_path}/public")
    os.mkdir(f"{home_dir_path}/public")
    copy_dir_to_public(f"{home_dir_path}/static", f"{home_dir_path}/public")

    generate_pages(f"{home_dir_path}/content")

main()    