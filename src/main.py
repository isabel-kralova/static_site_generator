from copystatic import copy_directory, generate_page

def main():
    src = "static"
    dest = "public"

    from_path = "content/index.md"
    template_path = "template.html"
    dest_path = "public/index.html"

    copy_directory(src, dest)

    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()