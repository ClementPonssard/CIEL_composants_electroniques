#!/usr/bin/env python3
# synchro_docs.py
# Rebuild total de docs/composants a partir de composants/ + synchronise la page d'accueil MkDocs.
#
# - Supprime docs/composants/
# - Pour chaque dossier composants/<nom> :
#   - Copie images/ -> docs/composants/<nom>/images/
#   - Convertit README.md -> docs/composants/<nom>/index.md
#   - Copie tous les *.md en corrigeant les liens internes :
#       * liens vers README.md -> index.md
#       * liens "composants/<nom>/<fichier>.md" -> "<fichier>.md"
#       * liens relatifs ../../../composants/<nom>/<fichier>.md -> "<fichier>.md"
#       * conserve "images/..." tel quel (on a copie les images a l’identique)
# - Met a jour la section "Composants:" dans mkdocs.yml a partir des fichiers generes.
# - NOUVEAU : Copie automatiquement le README.md racine vers docs/index.md
#   afin que la page d’accueil du site MkDocs soit le README du depot.

import re
import shutil
from pathlib import Path
import yaml

SRC = Path("composants")
DOCS = Path("docs")
DST = DOCS / "composants"
MKDOCS = Path("mkdocs.yml")
ROOT_README = Path("README.md")

# ---------- utilitaires ----------

MD_LINK_RE = re.compile(r'(\!?)\[(?P<text>[^\]]*)\]\((?P<url>[^)]+)\)')

def normalize_md_links(text: str, comp_name: str) -> str:
    """
    Corrige les liens dans un markdown provenant de composants/<comp_name>/ :
    - README.md -> index.md
    - */composants/<comp_name>/*.md -> fichier local *.md
    - chemins relatifs vers composants/<comp_name>/*.md -> fichier local *.md
    - laisse "images/..." tel quel
    - ne touche pas aux http(s):// ni aux ancres (#...) ni aux chemins absolus commencant par /
    """

    def repl(m):
        bang = m.group(1)  # "!" si image
        text_label = m.group('text')
        url = m.group('url').strip()

        # Pas touche aux urls externes, ancres, ou absolues
        if url.startswith("http://") or url.startswith("https://") or url.startswith("#") or url.startswith("/"):
            return m.group(0)

        # Nettoie eventuellement des angles <...>
        if url.startswith("<") and url.endswith(">"):
            url_core = url[1:-1]
        else:
            url_core = url

        # Normalise les anti-slash eventuels
        url_core = url_core.replace("\\", "/")

        # README.md -> index.md (meme dossier)
        if re.fullmatch(r"(?:\./)?README\.md", url_core, re.IGNORECASE):
            url_new = "index.md"
            return f"{bang}[{text_label}]({url_new})"

        # images/... -> garder tel quel (on a copie le dossier images/)
        if url_core.startswith("images/"):
            return f"{bang}[{text_label}]({url_core})"

        # Cas ou l'auteur a mis un chemin complet vers composants/<comp_name>/...
        pattern_same_comp = rf"^(?:\./|\.{1,3}/)*composants/{re.escape(comp_name)}/(.+)$"
        m_same = re.match(pattern_same_comp, url_core, re.IGNORECASE)
        if m_same:
            url_rel = m_same.group(1)
            # README.md cible -> index.md
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
    Recupere le premier titre markdown (#, ##, …). Sinon fallback formate.
    """
    for line in md_text.splitlines():
        if line.strip().startswith("#"):
            return line.strip().lstrip("#").strip()
    # fallback : nom de fichier sans extension, avec jolis espaces
    name = fallback.rsplit(".", 1)[0]
    return name.replace("_", " ").replace("-", " ").strip().capitalize()

# ---------- reconstruction docs/composants ----------

print("🔄 Reconstruction complete de docs/composants ...")
if DST.exists():
    shutil.rmtree(DST)
DST.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

components_nav = []

if not SRC.exists():
    print("⚠️  Dossier 'composants/' introuvable. Rien a synchroniser pour les composants.")
else:
    for comp_dir in sorted(SRC.iterdir()):
        if not comp_dir.is_dir():
            continue
        comp_name = comp_dir.name
        print(f"  ➜ {comp_name}")

        out_dir = DST / comp_name
        out_dir.mkdir(parents=True, exist_ok=True)

        # 1) Images (copie brute si presentes)
        img_src = comp_dir / "images"
        if img_src.exists():
            shutil.copytree(img_src, out_dir / "images", dirs_exist_ok=True)

        # 2) Traite tous les .md
        pages_for_nav = []
        md_files = sorted(p for p in comp_dir.glob("*.md"))

        # Assure que README est traite en premier si present
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
                title = "Presentation"           # force ce libelle pour le README
            else:
                title = first_heading_as_title(fixed, fallback=out_name)

            pages_for_nav.append({title: f"composants/{comp_name}/{out_name}"})

        # 3) ajoute la rubrique de ce composant dans la nav
        if pages_for_nav:
            comp_title = comp_name.replace("_", " ").strip()
            components_nav.append({comp_title: pages_for_nav})

# ---------- synchronise la page d'accueil : README.md -> docs/index.md ----------
try:
    if ROOT_README.exists():
        print("📄 Synchronisation de README.md -> docs/index.md ...")
        (DOCS / "index.md").write_text(ROOT_README.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        print("ℹ️ Aucun README.md trouve a la racine — index.md non mis a jour.")
except Exception as e:
    print(f"❌ Erreur lors de la copie du README vers docs/index.md : {e}")

# ---------- mise a jour mkdocs.yml ----------

if not MKDOCS.exists():
    raise FileNotFoundError("mkdocs.yml introuvable a la racine.")

with MKDOCS.open("r", encoding="utf-8") as f:
    mk = yaml.safe_load(f) or {}

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

print("✅ Termine : docs/index.md synchronise, docs/composants reconstruit et nav mise a jour.")
