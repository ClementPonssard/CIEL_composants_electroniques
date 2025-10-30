# Tuto 2 — Communication LoRa point-à-point sans Meshtastic

## 🎯 Objectif du TP
Mettre en œuvre la communication **LoRa** entre deux modules Heltec WiFi LoRa 32 (V3) sans utiliser Meshtastic, en programmant directement la carte avec l’IDE Arduino ou sous PlatformIO.

## 🧠 Compétences visées
- Programmer une carte **ESP32 LoRa**
- Flasher et configurer des exemples de transmission
- Mesurer la qualité de réception radio (**RSSI**)
- Tester la portée et documenter les résultats

## 🔧 Matériel nécessaire
- 2 modules **Heltec WiFi LoRa 32 (V3)**
- 2 antennes **868 MHz**
- 2 câbles **USB-C**
- 1 ordinateur avec **PlatformIO** ou **Arduino IDE**

> ⚠️ **Toujours connecter l’antenne hors tension !**

## 🔗 Ressources utiles

- **Guide vidéo :** [Communication LoRa sans Meshtastic](https://www.youtube.com/watch?v=7BlPcQgJay8)  
- **Documentation officielle :** [https://github.com/HelTecAutomation/Heltec_ESP32](https://github.com/HelTecAutomation/Heltec_ESP32)  
- **Calculateur LoRa Semtech :** [https://www.semtech.fr/design-support/lora-calculator](https://www.semtech.fr/design-support/lora-calculator)  
- **Activation de licence Heltec :** [https://docs.heltec.org/general/how_to_use_license.html](https://docs.heltec.org/general/how_to_use_license.html)  
- **Recherche de clé de licence :** [https://resource.heltec.cn/search](https://resource.heltec.cn/search)

## 🧩 Étapes principales

### 1️⃣ Installation de l’environnement

1. Ouvrir **Arduino IDE**
2. Si les cartes ESP32 ne sont pas disponibles :
      - Aller dans **Fichier → Préférences**
      - Ajouter l’URL suivante dans *Gestionnaire de cartes supplémentaires* :  
        ```
        https://dl.espressif.com/dl/package_esp32_index.json
        ```
      - Puis installer la carte **ESP32 by Espressif Systems**
3. Installer la **librairie Heltec ESP32** et ses dépendances :

### 2️⃣ Configuration de l’émetteur (*LoRaSender*)

1. Sélectionner la carte :  
   **Tools → Board → Heltec WiFi LoRa 32 (V3)**
2. Vérifier dans **Tools → LoRaWan Region** que la région est **EU868**
3. Ouvrir l’exemple :
   ```
   File → Examples → Heltec ESP32 Dev-Boards → LoRaBasic → LoRaSender
   ```
4. Régler la puissance d’émission :
   ```cpp
   TX_OUTPUT_POWER = 20;  // max 20 dBm
   ```
   > Pour ajuster les paramètres LoRa, utiliser le **LoRa Calculator** de Semtech.
5. **Compiler et flasher** la carte.  
6. Ouvrir le **Moniteur Série** à **115200 bauds**.  
   Le module doit afficher :
   ```
   sending packet "Hello world number 0.01", length 23
   TX done...
   ```

### 3️⃣ Activation de la licence Heltec (si demandée)

Si le message suivant apparaît :
```
Please provide a correct license! For more information:
http://www.heltec.cn/search/
ESP32ChipID=E422EB9E139C
```

➡️ Aller sur [https://resource.heltec.cn/search](https://resource.heltec.cn/search)  
➡️ Entrer l’**ESP32ChipID** affiché  
➡️ Copier la licence générée (sans les virgules ni “0x”)

Dans le **Moniteur Série**, envoyer la commande :
```
AT+CDKEY=43444B71A80A6BD6A2B39242AF7D71F3
```

Si tout est correct, le message suivant apparaît :
```
The board is actived
```

### 4️⃣ Configuration du récepteur (*LoRaReceiver*)

1. Ouvrir l’exemple :
   ```
   File → Examples → Heltec ESP32 Dev-Boards → LoRaBasic → LoRaReceiver
   ```
2. Sélectionner la même carte et région (**Heltec WiFi LoRa 32 (V3)** / **EU868**)  
3. **Flasher** la carte réceptrice  
4. Ouvrir le **Moniteur Série (115200 bauds)** pour observer les messages reçus.


## ✅ Vérification de la communication

1. Alimenter les deux modules (émetteur et récepteur)  
2. Sur le moniteur du **Receiver**, on doit voir :
   ```
   received packet "Hello world number 0.59" with rssi -4, length 23
   ```
3. Le **RSSI** indique la puissance du signal reçu :
   - Plus la valeur est **proche de 0**, plus le signal est fort.
   - Exemple :

     | RSSI (dBm) | Qualité du signal |
     |-------------|------------------|
     | -40 à -60   | Excellent |
     | -60 à -80   | Bon / moyen |
     | -80 à -100  | Faible |
     | < -110      | Très faible / perdu |


## 📊 Test de portée

- Déplacer les modules pour tester différentes distances et obstacles  
- Noter les **valeurs de RSSI** obtenues selon la distance et la configuration  
- Jouer sur :
    - La **puissance d’émission** (`TX_OUTPUT_POWER`, max 20 dBm)
    - Le **masquage des antennes** (attention, elles sont fragiles)
    - L’**orientation** des antennes

## 🚀 Pour aller plus loin

- Intégrer d’autres équipements LoRa (stations de réception, gateways, etc.)  
- Ajuster les paramètres LoRa : bande, *spreading factor*, débit, puissance  
- Sécuriser la communication (cryptage, filtrage d’adresses)  
- Utiliser les autres fonctions du module :
    - **Écran OLED** pour afficher les données reçues
    - **Batterie LiPo** pour des tests en extérieur  

## 🧰 Dépannage / erreurs fréquentes

| Problème | Cause probable | Solution |
|-----------|----------------|-----------|
| **Carte non détectée** | Drivers USB manquants | Installer les **drivers CP210X** |
| **Erreur de compilation** | Librairies manquantes | Réinstaller la **lib Heltec ESP32** et **Adafruit GFX** |
| **Message “Please provide a correct license”** | Licence non activée | Récupérer la licence sur [resource.heltec.cn](https://resource.heltec.cn/search) et l’envoyer via le Moniteur Série |
| **Pas de message reçu** | Mauvaise région ou fréquence | Vérifier que les deux cartes sont en **EU868** |
| **RSSI très faible ou nul** | Antenne mal fixée ou endommagée | Vérifier le connecteur SMA et l’intégrité de l’antenne |
| **Port COM non visible** | Mauvais câble ou port USB défectueux | Essayer un autre câble **USB-C** (avec données) |
| **Communication instable** | TX power trop faible ou interférences | Augmenter `TX_OUTPUT_POWER`, éloigner des sources de bruit RF |

---

## 🧾 Compte rendu élève

### 🔍 Objectif du test
Déterminer la portée maximale et la qualité de communication LoRa entre deux modules Heltec WiFi LoRa 32 (V3).

### 📋 Tableau de mesures

| Distance (m) | Environnement | Obstacles | RSSI (dBm) | Qualité du signal | Observations |
|---------------|----------------|------------|-------------|------------------|---------------|
| 1 | Intérieur | Aucun | | | |
| 5 | Intérieur | Cloison légère | | | |
| 10 | Intérieur | 2 cloisons | | | |
| 25 | Extérieur | Libre | | | |
| 50 | Extérieur | Libre | | | |
| 100 | Extérieur | Libre | | | |

> Ajouter d'autres lignes si nécessaire.

### 📈 Analyse

- Décrire l’évolution du **RSSI** en fonction de la distance.  
- Identifier les **facteurs influençant** la qualité du signal (distance, obstacles, orientation…).  
- Comparer les performances **intérieur / extérieur**.  
- Expliquer l’intérêt du protocole **LoRa** pour les communications longue portée à faible débit.

### 🧩 Conclusion

- Résumer les performances observées.  
- Proposer des pistes d’amélioration (antenne, puissance, paramètres LoRa, etc.).  
- Répondre à la question : *jusqu’où peut-on communiquer efficacement en LoRa avec ces modules ?*


📘 **Astuce :**
Pour une meilleure portée, placer les modules en hauteur et éviter les obstacles métalliques.  
En extérieur dégagé, une portée de **plusieurs centaines de mètres** est facilement atteignable.

---

**Auteur :** Clément Ponssard  
**Version :** 1.1 — octobre 2025
