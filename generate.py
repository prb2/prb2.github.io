#!/usr/bin/python3

import os
import re
import subprocess


def main():
    print("Building blog index...")

    with open("./src/blog.md", "w") as blog_index:
        blog_index.write("---\ntitle: Blog\n---\n\n")
        for f in sorted(os.listdir("src/posts"), reverse=True):
            if f.endswith(".md"):
                file_path = os.path.join("src/posts", f)
                print(f"\t{file_path}")
                with open(file_path, "r") as post_file:
                    content = post_file.read()
                    title = re.search(r"^title:\s*(.*)", content, re.MULTILINE).group(1)
                    date = re.search(r"^date:\s*(.*)", content, re.MULTILINE).group(1)
                    fname = file_path.replace("src", "").replace(".md", ".html")
                    blog_index.write(f"- `{date}` [{title}]({fname})\n")

    print("Removing old html files...")
    for root, dirs, files in os.walk("./build"):
        for file in files:
            if file.endswith(".html"):
                os.remove(os.path.join(root, file))

    print("Generating html...")
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                fname = file_path.replace("src", "build").replace(".md", ".html")
                print(f"\tgenerating {fname}")
                with open(fname, "w") as html_file:
                    with open("src/sidebar.template", "r") as sidebar:
                        html_file.write(sidebar.read())
                    result = subprocess.run(
                        [
                            "pandoc",
                            "-s",
                            "-c",
                            "/style.css",
                            "-f",
                            "markdown-smart",
                            "-t",
                            "html",
                            file_path,
                        ],
                        capture_output=True,
                        text=True,
                    )
                    html_content = result.stdout.replace("↩", "&#x21A9;")
                    html_file.write(html_content)

    print("Done")


if __name__ == "__main__":
    main()
