#!/usr/bin/python3

import os
import re
import subprocess
from email.utils import formatdate
from datetime import datetime


def cleanup():
    print("Removing old html files...")
    for root, dirs, files in os.walk("./build"):
        for file in files:
            if file.endswith(".html"):
                os.remove(os.path.join(root, file))


def build_blog_index() -> list[tuple[str, str, str]]:
    print("Building blog index...")
    posts = []
    with open("./src/blog.md", "w") as blog_index:
        blog_index.write("---\ntitle: Blog\n---\n\n")
        for root, dirs, files in os.walk("src/posts"):
            if len(files) == 0:
                # skip the post dir; we only want the per-year sub dirs
                continue
            year = root[-4:]
            blog_index.write(f"\n## {year}\n\n")
            files.sort(reverse=True)  # we want reverse chrono ordering
            for f in files:
                if f.endswith(".md"):
                    file_path = os.path.join(f"src/posts/{year}", f)
                    print(f"\t{file_path}")
                    with open(file_path, "r") as post_file:
                        content = post_file.read()
                        title = re.search(
                            r"^title:\s*(.*)", content, re.MULTILINE
                        ).group(1)
                        date = re.search(r"^date:\s*(.*)", content, re.MULTILINE).group(
                            1
                        )
                        fname = file_path.replace("src", "").replace(".md", ".html")
                        posts.append((fname, title, date))
                        blog_index.write(f"- [{title}]({fname})\n")
    return posts


def generate_html():
    print("Generating html...")

    navbar_html = ""
    with open("src/navbar.template", "r") as navbar_file:
        navbar_html = navbar_file.read()
    footer_html = ""
    with open("src/footer.template", "r") as footer_file:
        footer_html = footer_file.read()

    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                fname = file_path.replace("src", "build").replace(".md", ".html")
                base_dir = os.path.dirname(fname)
                if not os.path.exists(base_dir):
                    os.makedirs(base_dir)
                with open(fname, "w") as html_file:
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
                            "--highlight-style",
                            "pygments",
                            file_path,
                        ],
                        capture_output=True,
                        text=True,
                    )
                    html_content = (
                        result.stdout.replace("↩", "&#x21A9;")
                        .replace("<body>", "<body>\n" + navbar_html)
                        .replace("</body>", footer_html + "\n</body>")
                    )
                    html_file.write(html_content)


def generate_rss_feed(posts: list[tuple[str, str, str]]):
    print("Generating RSS feed...")

    items = ""
    for fname, title, date in posts:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        rfc822_date = formatdate(date_obj.timestamp())
        url = f"https://prudhviboyapalli.com{fname}"
        items += f"""
        <item>
            <title>{title}</title>
            <link>{url}</link>
            <guid>{url}</guid>
            <pubDate>{rfc822_date}</pubDate>
        </item>"""
        # TODO: <description></description>

    with open("build/rss.xml", "w") as rss_file:
        rss_file.write(f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>Prudhvi Boyapalli</title>
        <description>Prudhvi Boyapalli's Blog</description>
        <link>https://prudhviboyapalli.com</link>
        <atom:link href="https://prudhviboyapalli.com/rss.xml" rel="self" type="application/rss+xml" />
        {items}
    </channel>
</rss>
""")


def main():
    cleanup()  # remove old html files first
    posts = build_blog_index()
    generate_html()
    generate_rss_feed(posts)
    print("Done")


if __name__ == "__main__":
    main()
