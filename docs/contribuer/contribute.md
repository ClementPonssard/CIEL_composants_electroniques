# 🤝 Contribuer au dépôt

Ce dépôt est collaboratif : il regroupe des **tutoriels, exemples de code et fiches techniques** pour les composants électroniques utilisés en Bac Pro et BTS CIEL.  
Chacun peut contribuer en ajoutant un nouveau composant, en améliorant la documentation ou en partageant des exemples.

---

## 🧩 Convention de nommage

Pour garder une structure claire et homogène :

| Type | Exemple | Règle |
|------|----------|-------|
| **Dossier composant** | `dht22`, `mpu6050`, `heltec_wifi_lora_32_v3` | tout en minuscules, séparateurs `_` |
| **Exemples** | `example_minimal`, `example_i2c_advanced` | préfixe `example_`, nom explicite et concis |

---

## 🆕 Ajouter un composant

1. **Copier le squelette** :
   ```bash
   cp -r templates/component_skeleton composants/<nom_du_composant>
   ```

2. **Compléter les fichiers Markdown** :
   - `README.md` : présentation générale du composant  
   - `tuto-1-*.md`, `tuto-2-*.md` : tutoriels pas à pas  
   - `references.md` : fiches techniques, liens, documentation fabricant  

3. **Créer au moins un exemple fonctionnel** dans `code/` :  
   - Projet **PlatformIO** compilable  
   - Inclure un fichier `platformio.ini` et un dossier `src/` contenant le code (`.ino`, `.cpp`, etc.)

4. **Ajouter le composant à la navigation** dans `mkdocs.yml` :
   ```yaml
   nav:
     - Composants:
         - Heltec WiFi LoRa 32 V3: composants/heltec_wifi_lora_32_v3/README.md
   ```

---

## 🗂️ Structure type d’un composant

```ini
composants/
└── heltec_wifi_lora_32_v3/
    ├── README.md
    ├── tuto-1-meshtastic.md
    ├── tuto-2-lora-sans-meshtastic.md
    ├── references.md
    ├── code/
    │   ├── platformio.ini 
    │   └── src/
    │       └── LoRaReceiver.ino
    └── images/
        └── heltec_wifi_lora_32_v3.png
```

!!! note
    - Les sous-répertoires autres que `images` sont **ignorés par la génération de la documentation**.  
    - Chaque fichier `.md` à la racine du composant génère **une page HTML** dans la doc.  
    - Le code embarqué est idéalement conçu pour être compilé avec **PlatformIO**.

---

## 🧱 Générer et visualiser la documentation en local

### 🔧 Installation des outils

```bash
# Installer Python et pip
sudo apt update
sudo apt install python3 python3-pip -y

# Installer MkDocs et les extensions utilisées
pip3 install mkdocs-material mkdocs-include-markdown-plugin mkdocs-exclude
```

---

### 🪄 Génération automatique des pages

Chaque fois que vous ajoutez un composant, exécutez :

```bash
python ./synchro_docs.py
```

Cela met à jour la documentation à partir des fichiers présents dans `composants/`.

---

### 🌐 Visualiser le site en local

```bash
mkdocs serve
```

Le site est alors accessible sur :  
➡️ [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

!!! note
    - La page [**Mise en page**](./MiseEnPage.md) illustre les différents styles et rendus disponibles dans MkDocs.  
    - Le **rechargement est automatique** : toute modification d’un fichier `.md` dans `docs/` actualise le site instantanément.  
    - En revanche, le script `synchro_docs.py` **doit être relancé manuellement** si vous modifiez un fichier dans `composants/`.

!!! warning "Attention"
    Ne modifiez **pas directement les fichiers dans `docs/`**.  
    Le contenu principal est généré à partir du dossier `composants/`.  
    Si vous travaillez sur un tutoriel, pensez à rapatrier le `.md` correspondant dans le répertoire du composant avant de lancer `synchro_docs.py`.

---

## ⚖️ Licences

| Type | Licence |
|-------|----------|
| 💻 **Code source** | [CeCILL-B](https://cecill.info/licences/Licence_CeCILL-B_V1-fr.html) |
| 📄 **Documentation & images** | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr) |

---

✍️ **Merci à tous les contributeurs !**  
Votre participation permet d’enrichir ce dépôt et de le rendre utile à toute la communauté CIEL.

---
