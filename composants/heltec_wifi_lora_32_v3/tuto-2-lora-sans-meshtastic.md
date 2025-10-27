# Tuto 2 — Communication LoRa point-à-point sans Meshtastic

## 🎯 Objectif du TP
Mettre en œuvre la communication **LoRa** entre deux modules Heltec WiFi LoRa 32 (V3) sans utiliser Meshtastic, en programmant directement sous PlatformIO ou l’IDE Arduino.

## 🧠 Compétences visées
- Programmer une carte **ESP32 LoRa**
- Flasher et configurer des exemples de transmission
- Mesurer la qualité de réception radio (RSSI)
- Tester la portée et documenter les résultats

## 🔧 Matériel nécessaire
- 2 modules Heltec WiFi LoRa 32 (V3)
- 2 antennes 868 MHz
- 2 câbles USB-C
- Un ordinateur avec PlatformIO ou Arduino IDE

> ⚠️ **Toujours connecter l’antenne hors tension.**

---

## Étapes principales

1. Installer la carte **Heltec ESP32** dans l’IDE Arduino  
2. Installer la bibliothèque **Heltec ESP32** (+ dépendances : *Adafruit GFX*, etc.)  
3. Ouvrir les exemples :  
   - `File → Examples → Heltec ESP32 Dev-Boards → LoRaBasic → LoRaSender`
   - `File → Examples → Heltec ESP32 Dev-Boards → LoRaBasic → LoRaReceiver`
4. Sélectionner la carte **Heltec WiFi LoRa 32 (V3)** et la région **EU868**
5. Régler `TX_OUTPUT_POWER` selon besoin (max 20 dBm)
6. Flasher l’émetteur et le récepteur
7. Vérifier sur le moniteur série (115200 bauds)

## Vérification de la communication

- Le **sender** envoie périodiquement “Hello world”  
- Le **receiver** affiche les paquets reçus et le **RSSI**  
- Exemples :
  - `sending packet "Hello world number 0.01"`  
  - `received packet "Hello world number 0.59" with rssi -4`

| RSSI (dBm) | Qualité du signal |
|-------------|------------------|
| -40 à -60   | Excellent |
| -60 à -80   | Bon / moyen |
| -80 à -100  | Faible |
| < -110      | Très faible / perdu |

## Pour aller plus loin

- Ajouter une batterie pour test en extérieur  
- Tester d’autres antennes et orientations  
- Utiliser l’écran OLED pour afficher les données  
- Explorer les paramètres LoRa (Bande, Spreading Factor, etc.)
