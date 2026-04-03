import os
import shutil
from block_markdown import markdown_to_html_node, extract_title
from htmlnode import ParentNode

def copy_directory(src, dest):
    if os.path.exists(dest):
        print(f"Deleting existing directory: {dest}")
        shutil.rmtree(dest)

    print(f"Creating directory: {dest}")
    os.mkdir(dest)
    copy_recursive(src, dest)
    
def copy_recursive(src, dest):
    content_list = os.listdir(src)
    print(f"Content list: {content_list}")
    for item in content_list:
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} to {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_recursive(src_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)
    
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    content_list = os.listdir(dir_path_content)
    for item in content_list:
        item_path = os.path.join(dir_path_content, item)
        destination_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(item_path) and item.endswith(".md"):
            dest_file_path = destination_path.replace(".md", ".html")

            print(f"Generating page: {item_path} -> {dest_file_path}")
            generate_page(item_path, template_path, dest_file_path)
        
        elif os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, destination_path)