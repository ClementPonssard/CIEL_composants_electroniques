#!/usr/bin/env python3
import os
from pathlib import Path

SRC = Path("composants")
DST = Path("docs/composants")

for comp in SRC.iterdir():
    if not comp.is_dir():
        continue

    target = DST / comp.name
    os.makedirs(target, exist_ok=True)

    for md in comp.glob("*.md"):
        wrapper = target / md.name
        relpath = f"../../{md.as_posix()}"
        wrapper.write_text(f'{{% include-markdown "{relpath}" rewrite_relative_urls=false %}}\n', encoding="utf-8")

    # Copie optionnelle des images pour un aperçu local
    img_src = comp / "images"
    if img_src.exists():
        img_dst = target / "images"
        os.makedirs(img_dst, exist_ok=True)
        for img in img_src.glob("*"):
            img_dst.write_bytes(img.read_bytes())

print("✅ Synchronisation terminée.")
