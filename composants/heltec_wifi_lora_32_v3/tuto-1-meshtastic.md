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
- 1 module Heltec WiFi LoRa 32 (V3)
- 1 antenne 868 MHz
- 1 câble USB-C
- 1 ordinateur (Chrome/Edge)
- Éventuellement : un second module pour les tests de réseau

> ⚠️ **Antenne obligatoire avant toute mise sous tension !**

---

## Procédure d'installation et d'utilisation

1. Connecter l’antenne au module **hors tension**  
2. Brancher la carte en **USB-C**  
3. Vérifier dans le **Gestionnaire de périphériques** la présence d’un module *Silicon Labs CP210X*
4. Si absent, installer les **drivers CP210X USB to UART Bridge**  
5. Ouvrir le **Web Flasher** : [https://flasher.meshtastic.org/](https://flasher.meshtastic.org/)  
6. Sélectionner la carte Heltec WiFi LoRa 32 (V3) et flasher le firmware  
7. Configurer ensuite via :
   - [Client Web](https://client.meshtastic.org)
   - ou l’application Android/iOS
8. Dans *Configuration → LoRa* :
   - **Région :** EU_868  
   - **MQTT :** activé  
   - Enregistrer puis redémarrer

## Utilisation de base

- Envoyer un message sur le **canal principal** (public, non chiffré)
- Envoyer un message **privé** à un autre nœud
- Vérifier la propagation sur le réseau maillé

## Pour aller plus loin

- Tester les portées en environnement réel  
- Associer plusieurs modules Heltec / T-Beam  
- Observer les échanges sur la carte OLED
