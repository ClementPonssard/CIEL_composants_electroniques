# Catalogue composants — CIEL (Arduino + PlatformIO)

Monorepo pédagogique : tutoriels et exemples **Arduino Uno** (PlatformIO) pour composants électroniques courants.
Le site est publié via **MkDocs Material** ici https://clementponssard.github.io/CIEL_composants_electroniques

## Démarrer
1. **Installer PlatformIO** (VS Code ou `pip install platformio`).
2. Cloner le dépôt puis tester un exemple :
   ```bash
   pio run -d composants/dht22/code/example_minimal && pio run -d components/dht22/code/example_minimal -t upload
   ```
3. Lancer la doc en local :
   ```bash
   pip install mkdocs-material mkdocs-include-markdown-plugin
   mkdocs serve
   ```

## Structure
```
components/
  dht22/
    README.md, tuto-1..., tuto-2..., references.md
    code/example_minimal/ (PlatformIO)
  mpu6050/
docs/  -> site MkDocs
templates/ -> gabarits
.github/workflows -> CI + Pages
```

## Licences
- **Code** : MIT (voir `LICENSE`)
- **Docs/Images** : CC BY-SA 4.0
