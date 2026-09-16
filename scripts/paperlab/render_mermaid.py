#!/usr/bin/env python3
"""Render Mermaid sources to tight SVG and cropped PDF publication assets.

Requires the locally available Mermaid CLI (`npx @mermaid-js/mermaid-cli`) and
TeX Live's `pdfcrop`. Source files remain the single source of truth.

Usage:
  python3 scripts/paperlab/render_mermaid.py \
      --src-dir docs/figs/mermaid_v0.3
"""
import argparse
import subprocess
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-dir", default="docs/figs/mermaid_v0.3")
    args = ap.parse_args()
    src_dir = Path(args.src_dir)
    if not src_dir.is_absolute():
        src_dir = Path.cwd() / src_dir
    sources = sorted(src_dir.glob("*.mmd"))
    if not sources:
        raise SystemExit(f"no Mermaid sources in {src_dir}")

    for source in sources:
        svg = source.with_suffix(".svg")
        raw_pdf = source.with_name(source.stem + ".raw.pdf")
        pdf = source.with_suffix(".pdf")
        subprocess.run(
            ["npx", "--no-install", "@mermaid-js/mermaid-cli",
             "-i", str(source), "-o", str(svg), "-b", "transparent"],
            check=True,
        )
        subprocess.run(
            ["npx", "--no-install", "@mermaid-js/mermaid-cli",
             "-i", str(source), "-o", str(raw_pdf), "-b", "white"],
            check=True,
        )
        subprocess.run(
            ["pdfcrop", "--margins", "12", str(raw_pdf), str(pdf)],
            check=True,
        )
        raw_pdf.unlink()
        print(f"{source.name} -> {svg.name}, {pdf.name}")


if __name__ == "__main__":
    main()