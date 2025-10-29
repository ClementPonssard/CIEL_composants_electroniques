# 🧰 Comment compiler les exemples fournis dans ce dépôt

Ce dépôt contient différents **tutoriels et exemples de code** associés aux composants électroniques utilisés en Bac Pro et BTS CIEL.  
Chaque composant possède un ou plusieurs exemples de programmes prêts à être compilés avec **Arduino IDE** ou **PlatformIO (PIO)**.

---

## 📂 Où trouver les exemples

Les exemples sont rangés dans le dossier :

```
composants/Nom_composant/code/
```

Par exemple :
```
composants/heltec_wifi_lora_32_v3/code/LoRaSender
```

Tu peux soit :
- **cloner le dépôt complet** dans VS Code :  
  ```bash
  git clone https://github.com/<ton-repo>.git
  ```
- soit **récupérer uniquement le dossier** du composant qui t’intéresse.

---

## ⚙️ Option 1 : Compilation via l’IDE Arduino

1. Ouvre le fichier `.ino` correspondant à l’exemple.  
2. Installe les **librairies nécessaires** :
   - Elles sont listées dans le tutoriel correspondant au composant,  
     ou dans le fichier `platformio.ini` (rubrique `[env] → lib_deps`).
3. Sélectionne la **carte cible** (ex. Heltec WiFi LoRa 32 V3, ESP32, Arduino Uno…).
4. Sélectionne le **port série** correspondant à la carte.
5. Clique sur **→ Téléverser** pour compiler et envoyer le programme.

> 💡 Si l’exemple ne compile pas, vérifie la version des librairies et la carte sélectionnée.

---

## 🧑‍💻 Option 2 : Compilation avec PlatformIO (PIO)

### 1. Installer PlatformIO

Tu peux l’utiliser :
- soit **dans VS Code** (extension *PlatformIO IDE*),
- soit en **ligne de commande** (Linux/macOS/Windows) :
  ```bash
  pip install platformio
  ```

---

### 2. Cloner le dépôt

```bash
git clone https://github.com/<ton-repo>.git
cd <ton-repo>
```

---

### 3. Compiler un exemple

Utilise la commande suivante pour compiler un exemple :

```bash
pio run -d composants/heltec_wifi_lora_32_v3/code/LoRaSender
```

> L’option `-d` indique à PlatformIO le dossier du projet à compiler.

---

### 4. Compiler et téléverser sur la carte

```bash
pio run -d composants/heltec_wifi_lora_32_v3/code/LoRaSender -t upload
```

> 💡 PlatformIO détecte automatiquement la carte (si elle est connectée en USB).  
> Si besoin, configure le bon port série dans le fichier `platformio.ini` :
> ```ini
> upload_port = /dev/ttyUSB0
> ```

---

### 5. Ouvrir le moniteur série

Pour visualiser les messages envoyés par le programme :

```bash
pio device monitor -d composants/heltec_wifi_lora_32_v3/code/LoRaSender
```

---

## 🧩 Astuce : tester tous les exemples d’un composant

Tu peux rapidement tester tous les exemples d’un même composant avec :

```bash
for d in composants/heltec_wifi_lora_32_v3/code/*; do pio run -d "$d"; done
```

---

## 📘 En résumé

| Méthode | Avantages | Inconvénients |
|----------|------------|----------------|
| **Arduino IDE** | Simple, visuel, idéal pour débuter | Gestion manuelle des bibliothèques |
| **PlatformIO** | Automatisation, gestion des dépendances, intégration VS Code | Demande une première configuration |

---

> 🧠 **Conseil :**  
> Pour un usage régulier en Bac Pro ou BTS, **PlatformIO** est recommandé : il permet de versionner les projets, d’intégrer le code dans GitHub et de travailler plus efficacement en équipe.

---
