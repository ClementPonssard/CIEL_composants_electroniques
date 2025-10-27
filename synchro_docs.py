#!/usr/bin/env python3
"""
sync_docs.py
-----------------------------------
Synchronise automatiquement la documentation MkDocs à partir du dossier 'composants/'.

Fonctions :
- Supprime entièrement 'docs/composants/' (reconstruction complète)
- Recrée les wrappers pour tous les fichiers .md de chaque composant
- Copie les images locales pour un rendu correct
- Met à jour automatiquement la section 'Composants:' dans mkdocs.yml
"""

import shutil
import yaml
from pathlib import Path

# Dossiers source / destination / config
SRC = Path("composants")
DST = Path("docs/composants")
MKDOCS_FILE = Path("mkdocs.yml")

print("🔄 Reconstruction complète de la documentation des composants...")

# 1️⃣ Suppression du dossier docs/composants/
if DST.exists():
    shutil.rmtree(DST)
DST.mkdir(parents=True, exist_ok=True)

components_nav = []  # pour la section "Composants" du mkdocs.yml

# 2️⃣ Parcours des composants sources
for comp in sorted(SRC.iterdir()):
    if not comp.is_dir():
        continue

    print(f"  ➜ {comp.name}")
    target = DST / comp.name
    target.mkdir(parents=True, exist_ok=True)

    # Création des wrappers pour chaque fichier Markdown
    pages = []
    for md in sorted(comp.glob("*.md")):
        relpath = f"../../{md.as_posix()}"
        wrapper_path = target / md.name
        wrapper_path.write_text(f'{{% include-markdown "{relpath}" rewrite_relative_urls=false %}}\n', encoding="utf-8")
        title = md.stem.replace("-", " ").capitalize()
        pages.append({title: f"composants/{comp.name}/{md.name}"})

    # Copie des images locales (pour rendu MkDocs)
    img_src = comp / "images"
    if img_src.exists():
        img_dst = target / "images"
        img_dst.mkdir(parents=True, exist_ok=True)
        for img in img_src.glob("*"):
            if img.is_file():
                shutil.copy(img, img_dst / img.name)


    # Ajout dans la nav
    if pages:
        components_nav.append({comp.name.replace("_", " ").capitalize(): pages})

# 3️⃣ Mise à jour du fichier mkdocs.yml
if not MKDOCS_FILE.exists():
    raise FileNotFoundError("mkdocs.yml introuvable à la racine du dépôt !")

with open(MKDOCS_FILE, "r", encoding="utf-8") as f:
    mkdocs_data = yaml.safe_load(f)

nav = mkdocs_data.get("nav", [])
new_nav = []
components_inserted = False

for item in nav:
    if isinstance(item, dict) and "Composants" in item:
        new_nav.append({"Composants": components_nav})
        components_inserted = True
    else:
        new_nav.append(item)

if not components_inserted:
    new_nav.append({"Composants": components_nav})

mkdocs_data["nav"] = new_nav

# 4️⃣ Sauvegarde du mkdocs.yml mis à jour
with open(MKDOCS_FILE, "w", encoding="utf-8") as f:
    yaml.dump(mkdocs_data, f, allow_unicode=True, sort_keys=False)

print("✅ Reconstruction terminée : wrappers, images et mkdocs.yml mis à jour.")
