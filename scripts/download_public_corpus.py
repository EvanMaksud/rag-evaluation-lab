from __future__ import annotations

import argparse
import re
from pathlib import Path

import requests

PAGES = [
    "Retrieval-augmented generation",
    "Large language model",
    "Information retrieval",
    "Bangladesh",
    "Dhaka",
    "Floods in Bangladesh",
    "Climate change in Bangladesh",
    "Machine learning",
    "Computer vision",
]

API_URL = "https://en.wikipedia.org/w/api.php"


def main() -> int:
    parser = argparse.ArgumentParser(description="Download a reproducible public text corpus.")
    parser.add_argument("--output", default="data/wikipedia_corpus")
    args = parser.parse_args()

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    for title in PAGES:
        page = fetch_page(title)
        slug = slugify(title)
        body = [
            f"# {title}",
            "",
            f"Source: https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
            "License note: Wikipedia text is available under CC BY-SA; see the source page for full attribution and revision history.",
            "",
            page,
            "",
        ]
        (output / f"{slug}.md").write_text("\n".join(body), encoding="utf-8")

    print(f"Wrote {len(PAGES)} documents to {output}")
    return 0


def fetch_page(title: str) -> str:
    response = requests.get(
        API_URL,
        params={
            "action": "query",
            "prop": "extracts",
            "explaintext": "1",
            "format": "json",
            "titles": title,
            "redirects": "1",
        },
        timeout=30,
    )
    response.raise_for_status()
    pages = response.json()["query"]["pages"]
    page = next(iter(pages.values()))
    extract = page.get("extract", "").strip()
    if not extract:
        raise RuntimeError(f"No extract returned for {title}")
    return extract


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


if __name__ == "__main__":
    raise SystemExit(main())

