import sys
from copystatic import copy_directory, generate_pages_recursive

def main():
    content_dir = "content"
    static_dir = "static"
    public_dir = "docs"
    template_path = "template.html"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_directory(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_path, public_dir, basepath)


if __name__ == "__main__":
    main()

# https://isabel-kralova.github.io/static_site_generator/