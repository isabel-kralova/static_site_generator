from copystatic import copy_directory, generate_pages_recursive

def main():
    content_dir = "content"
    static_dir = "static"
    public_dir = "public"
    template_path = "template.html"

    copy_directory(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()