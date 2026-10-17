"""Turn Markdown files into WordPress DRAFT posts through the REST API (Application Password auth)."""
import argparse
import glob
import os

import markdown
import requests


def parse_front_matter(text):
    """Split optional '---' key: value front matter from the body."""
    meta = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip().lower()] = v.strip()
            text = parts[2]
    return meta, text.strip()


def to_html(md_text):
    return markdown.markdown(md_text, extensions=["fenced_code", "tables"])


def build_post(path):
    with open(path, encoding="utf-8") as f:
        meta, body = parse_front_matter(f.read())
    title = meta.get("title") or os.path.splitext(os.path.basename(path))[0].replace("-", " ").title()
    post = {"title": title, "content": to_html(body), "status": "draft"}
    if meta.get("slug"):
        post["slug"] = meta["slug"]
    return post


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("folder", help="folder containing .md files")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    site, user, pw = os.environ.get("WP_SITE"), os.environ.get("WP_USER"), os.environ.get("WP_APP_PASSWORD")
    if not a.dry_run and not (site and user and pw):
        raise SystemExit("Set WP_SITE, WP_USER, WP_APP_PASSWORD (or use --dry-run)")
    for path in sorted(glob.glob(os.path.join(a.folder, "*.md"))):
        post = build_post(path)
        if a.dry_run:
            print("DRY:", post["title"])
            continue
        r = requests.post(f"{site.rstrip('/')}/wp-json/wp/v2/posts", json=post, auth=(user, pw), timeout=30)
        r.raise_for_status()
        print("draft created:", post["title"], "->", r.json().get("link"))


if __name__ == "__main__":
    main()
