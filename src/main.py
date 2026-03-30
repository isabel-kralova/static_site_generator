import os
import shutil
from textnode import TextNode, TextType

def main():
    node = TextNode(
        "This is some anchor text",
        TextType.LINK,
        "https://www.boot.dev"
    )
    print(node)

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


if __name__ == "__main__":
    copy_directory("static", "public")
    main()