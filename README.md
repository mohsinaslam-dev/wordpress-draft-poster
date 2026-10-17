# WordPress Draft Poster

**Platform:** WordPress REST API

Converts Markdown files (with optional front matter) to HTML and creates them as drafts on a WordPress site, never published automatically.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # then fill in your values
```
Environment variables: WP_SITE, WP_USER, WP_APP_PASSWORD (Users > Profile > Application Passwords)

Load them before running (for example `export $(grep -v '^#' .env | xargs)` on Linux/macOS, or set them in your shell on Windows).

## Usage
```bash
python app.py posts --dry-run
python app.py posts
```
Use `--dry-run` where available to see what would happen without calling the real API.

## Tests
The core logic is covered by tests that need no internet or credentials:
```bash
pip install pytest && pytest
```

## License
MIT
