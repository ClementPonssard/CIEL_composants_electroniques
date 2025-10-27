#!/usr/bin/env python3
"""
synchro_docs.py
Rebuild total de docs/composants à partir de composants/.

- Supprime docs/composants/
- Pour chaque dossier composants/<nom> :
  - Copie images/ -> docs/composants/<nom>/images/
  - Convertit README.md -> docs/composants/<nom>/index.md
  - Copie tous les *.md en corrigeant les liens internes :
      * liens vers README.md -> index.md
      * liens "composants/<nom>/<fichier>.md" -> "<fichier>.md"
      * liens relatifs ../../../composants/<nom>/<fichier>.md -> "<fichier>.md"
      * conserve "images/..." tel quel (on a copié les images à l’identique)
- Met à jour la section "Composants:" dans mkdocs.yml à partir des fichiers générés.
"""

import re
import shutil
from pathlib import Path
import yaml

SRC = Path("composants")
DST = Path("docs/composants")
MKDOCS = Path("mkdocs.yml")

# ---------- utilitaires ----------

MD_LINK_RE = re.compile(r'(\!?)\[(?P<text>[^\]]*)\]\((?P<url>[^)]+)\)')

def normalize_md_links(text: str, comp_name: str) -> str:
    """
    Corrige les liens dans un markdown provenant de composants/<comp_name>/ :
    - README.md -> index.md
    - */composants/<comp_name>/*.md -> fichier local *.md
    - chemins relatifs vers composants/<comp_name>/*.md -> fichier local *.md
    - laisse "images/..." tel quel
    - ne touche pas aux http(s):// ni aux ancres (#...) ni aux chemins absolus commençant par /
    """

    def repl(m):
        bang = m.group(1)  # "!" si image
        text_label = m.group('text')
        url = m.group('url').strip()

        # Pas touche aux urls externes, ancres, ou absolues
        if url.startswith("http://") or url.startswith("https://") or url.startswith("#") or url.startswith("/"):
            return m.group(0)

        # Nettoie éventuellement des angles <...>
        if url.startswith("<") and url.endswith(">"):
            url_core = url[1:-1]
        else:
            url_core = url

        # Normalise les anti-slash éventuels
        url_core = url_core.replace("\\", "/")

        # README.md -> index.md (même dossier)
        if re.fullmatch(r"(?:\./)?README\.md", url_core, re.IGNORECASE):
            url_new = "index.md"
            return f"{bang}[{text_label}]({url_new})"

        # images/... -> garder tel quel (on a copié le dossier images/)
        if url_core.startswith("images/"):
            return f"{bang}[{text_label}]({url_core})"

        # Cas où l'auteur a mis un chemin complet vers composants/<comp_name>/...
        pattern_same_comp = rf"^(?:\./|\.{1,3}/)*composants/{re.escape(comp_name)}/(.+)$"
        m_same = re.match(pattern_same_comp, url_core, re.IGNORECASE)
        if m_same:
            url_rel = m_same.group(1)
            # README.md ciblé -> index.md
            if url_rel.lower() == "readme.md":
                url_rel = "index.md"
            return f"{bang}[{text_label}]({url_rel})"

        # liens relatifs du style ../tuto-1.md, ./tuto-1.md, tuto-1.md -> on laisse
        # mais si cible README.md -> index.md
        if url_core.lower().endswith("readme.md"):
            url_core = re.sub(r"(?i)readme\.md$", "index.md", url_core)

        return f"{bang}[{text_label}]({url_core})"

    return MD_LINK_RE.sub(repl, text)

def first_heading_as_title(md_text: str, fallback: str) -> str:
    """
    Récupère le premier titre markdown (#, ##, …). Sinon fallback formaté.
    """
    for line in md_text.splitlines():
        if line.strip().startswith("#"):
            return line.strip().lstrip("#").strip()
    # fallback : nom de fichier sans extension, avec jolis espaces
    name = fallback.rsplit(".", 1)[0]
    return name.replace("_", " ").replace("-", " ").strip().capitalize()

# ---------- reconstruction docs/composants ----------

print("🔄 Reconstruction complète de docs/composants ...")
if DST.exists():
    shutil.rmtree(DST)
DST.mkdir(parents=True, exist_ok=True)

components_nav = []

for comp_dir in sorted(SRC.iterdir()):
    if not comp_dir.is_dir():
        continue
    comp_name = comp_dir.name
    print(f"  ➜ {comp_name}")

    out_dir = DST / comp_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Images (copie brute si présentes)
    img_src = comp_dir / "images"
    if img_src.exists():
        shutil.copytree(img_src, out_dir / "images", dirs_exist_ok=True)

    # 2) Traite tous les .md
    pages_for_nav = []
    md_files = sorted(p for p in comp_dir.glob("*.md"))

    # Assure que README est traité en premier si présent
    readme = comp_dir / "README.md"
    if readme.exists() and readme in md_files:
        md_files.remove(readme)
        md_files.insert(0, readme)

    for md_path in md_files:
        raw = md_path.read_text(encoding="utf-8")
        fixed = normalize_md_links(raw, comp_name=comp_name)

        out_name = "index.md" if md_path.name.lower() == "readme.md" else md_path.name
        (out_dir / out_name).write_text(fixed, encoding="utf-8")

        # --- titre menu ---
        if out_name == "index.md":
            title = "Présentation"           # ✅ force ce libellé pour le README
        else:
            title = first_heading_as_title(fixed, fallback=out_name)

        pages_for_nav.append({title: f"composants/{comp_name}/{out_name}"})

    # 3) ajoute la rubrique de ce composant dans la nav
    if pages_for_nav:
        comp_title = comp_name.replace("_", " ").strip()
        components_nav.append({comp_title: pages_for_nav})

# ---------- mise à jour mkdocs.yml ----------

if not MKDOCS.exists():
    raise FileNotFoundError("mkdocs.yml introuvable à la racine.")

with MKDOCS.open("r", encoding="utf-8") as f:
    mk = yaml.safe_load(f)

nav = mk.get("nav", [])
new_nav = []
inserted = False
for item in nav:
    if isinstance(item, dict) and "Composants" in item:
        new_nav.append({"Composants": components_nav})
        inserted = True
    else:
        new_nav.append(item)

if not inserted:
    new_nav.append({"Composants": components_nav})

mk["nav"] = new_nav

with MKDOCS.open("w", encoding="utf-8") as f:
    yaml.dump(mk, f, allow_unicode=True, sort_keys=False)

print("✅ Terminé : docs/composants reconstruit et nav mise à jour.")
