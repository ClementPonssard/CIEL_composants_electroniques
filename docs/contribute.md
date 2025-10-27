# Contribuer

## Convention de nommage
- Dossiers composant : `dht22`, `mpu6050`, etc.
- Exemples : `example_minimal`, `example_i2c_advanced`, etc.

## Ajouter un composant
1. Copier le dossier `templates/component_skeleton/` vers `components/<nom>/`.
2. Remplir `README.md`, `tuto-1...md`, `tuto-2...md`, `references.md`.
3. Créer au moins un exemple PlatformIO compilable dans `code/`.
4. Ajouter le composant à `mkdocs.yml` (nav).

## Licences
- Code : MIT
- Docs & images : CC BY-SA 4.0
