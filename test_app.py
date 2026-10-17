from app import build_post, parse_front_matter, to_html


def test_front_matter():
    meta, body = parse_front_matter("---\ntitle: Hello\nslug: hello-world\n---\n# Hi\ntext")
    assert meta == {"title": "Hello", "slug": "hello-world"} and body.startswith("# Hi")
    assert parse_front_matter("no meta") == ({}, "no meta")


def test_html_and_post(tmp_path):
    assert "<h1>" in to_html("# Title")
    f = tmp_path / "my-first-post.md"
    f.write_text("Just **bold** text")
    post = build_post(str(f))
    assert post["title"] == "My First Post" and post["status"] == "draft" and "<strong>" in post["content"]
