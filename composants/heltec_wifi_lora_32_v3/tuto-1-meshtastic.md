# Tuto 1 — Découverte et utilisation de Meshtastic

## 🎯 Objectif du TP
Découvrir la configuration et l’usage du protocole **Meshtastic** sur un module Heltec WiFi LoRa 32 (V3).  
Comprendre les bases du réseau maillé LoRa et échanger des messages entre nœuds.

## 🧠 Compétences visées
- Mettre en œuvre une carte **ESP32 LoRa**
- Flasher un firmware via navigateur Web
- Configurer une liaison LoRa maillée
- Utiliser les outils Web et mobiles Meshtastic

## 🔧 Matériel nécessaire
- 1 module **Heltec WiFi LoRa 32 (V3)**
- 1 antenne **868 MHz**
- 1 câble **USB-C**
- 1 ordinateur (navigateur **Chrome** ou **Edge**)
- 1 seconde module **Heltec WiFi LoRa 32 (V3)** ou autre noeud Meshtastic pour tester le réseau maillé

> ⚠️ **Toujours connecter l’antenne hors tension !**

## 🔗 Ressources utiles
- **Guide vidéo :** [Découverte Meshtastic (YouTube)](https://www.youtube.com/watch?v=Cs5Z7rP_eUo)  
- **Flasheur Web :** [https://flasher.meshtastic.org/](https://flasher.meshtastic.org/)  
- **Client Web :** [https://client.meshtastic.org](https://client.meshtastic.org)  

## 🧩 Procédure d’installation

1. **Connecter l’antenne** au module **hors tension**  
2. **Brancher** le module via câble **USB-C**  
3. Ouvrir le **Gestionnaire de périphériques** (Windows) → section **Ports (COM et LPT)**
      - Vérifier la présence de **Silicon Labs CP210X USB to UART Bridge**  
      - Si absent → installer les **drivers CP210X** depuis le site Meshtastic  
4. Ouvrir le **Web Flasher** sur *Chrome ou Edge*  : [https://flasher.meshtastic.org/](https://flasher.meshtastic.org/)
      - Sélectionner la carte **Heltec WiFi LoRa 32 (V3)**  
      - Selectionner le dernier micrologiciel en beta
      - Cliquer sur **Flash** pour installer le firmware  
      - Activer l'option **Effacement complet et installation**. 
      - Si le module ne répond pas, voir l'astuce ci-dessous.
5. Une fois le flash terminé, **redémarrer le module**.  

📘 **Astuce :**  
Si un module semble bloqué après un flash raté, maintenir le bouton **BOOT** enfoncé au branchement USB pour le relancer en mode récupération, puis reflasher via le Web Flasher.

## ⚙️ Configuration initiale

1. Ouvrir le **client Meshtastic** :
      - soit via le **Web Client** sur *Chrome ou Edge* → [client.meshtastic.org](https://client.meshtastic.org)  
      - soit via l’application **Android/iOS**
2. Choisir le mode de connexion :
      - **USB/Série** :  
        - Connecter directement le module à l’ordinateur  
      - **Bluetooth (BT)** :  
        - Demander le **jumelage**  
        - Entrer le **code affiché sur l’écran** du module  
3. Dans le menu **Changer le nom de l'appareil**, modifier :
      - **Nom complet :** `CIEL HHMM` (ex : *CIEL 1425*)  
      - **Nom court :** `CIHH` (ex : *CI14*)  
4. Dans le menu **Configuration → LoRa** :
      - **Région :** `EU_868`  
      - **MQTT :** *activé* (permet de transférer la position sur le réseau Meshtastic)  
      - **Sauvegarder les modifications**  
5. Redémarrer le module et **reconnecter** le client si nécessaire.  

## ✅ Vérification du bon fonctionnement

1. **Débrancher et rebrancher** l'alimentationc du module
2. Sur le client (Web, téléphone...), **attendre un peu** qu'un second noeud apparaisse dans "Noeuds"
      - Si vous avez connecté deux modules dans la même pièce, ils devraient se découvrir très rapidement.
3. **Envoyer un message** sur le **canal principal**  
      - Ce canal est **public et non chiffré**  
      - Le message sera **relayé** à tous les nœuds du réseau maillé  
4. **Envoyer un message privé** à un autre nœud (ex : *de 01 vers 02*)  
      - Accessible uniquement par le destinataire  
5. Si un nœud nommé **Prof** est visible, lui **envoyer un message privé**  
6. Observer les échanges :
      - Sur l’**écran OLED** du module  
      - Ou sur le **client Web / application mobile**

## 🚀 Pour aller plus loin

- Tester la **portée radio** en extérieur et en intérieur  
- Associer plusieurs modules (Heltec, T-Beam, etc.)  
- Observer la **topologie du réseau maillé**  
- Expérimenter l’envoi de **positions GPS** ou de **messages MQTT**  

## 🧰 Dépannage / erreurs fréquentes

| Problème | Cause possible | Solution |
|-----------|----------------|-----------|
| **Le module n’apparaît pas dans le Web Flasher** | Mauvais câble (charge uniquement) ou drivers manquants | Utiliser un câble **données**, installer les **drivers CP210X** |
| **Pas de port COM visible** | Mauvais port USB ou driver absent | Changer de port, vérifier le Gestionnaire de périphériques |
| **Le flash échoue à mi-parcours** | Port COM instable | Débrancher/rebrancher, relancer le flash |
| **Le client ne se connecte pas** | Mauvais mode (BT / USB) ou reboot du module | Choisir le bon mode de connexion, patienter après le reboot |
| **Pas de communication LoRa entre modules** | Mauvaise région ou antenne défectueuse | Vérifier la **région EU_868**, vérifier l’antenne et la puissance |
| **Message MQTT non visible** | Option MQTT désactivée | Activer **MQTT** dans la configuration LoRa |
| **Le module ne redémarre pas après flash** | Mauvaise carte sélectionnée | Reflasher en choisissant **Heltec WiFi LoRa 32 (V3)** |




**Auteur :** Clément Ponssard  
**Version :** 1.1 — octobre 2025
