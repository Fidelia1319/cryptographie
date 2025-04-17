📜 Description

CryptoTool est un outil en ligne de commande offrant des fonctions cryptographiques essentielles via une interface intuitive. Il utilise OpenSSL en backend pour les opérations cryptographiques.
✨ Fonctionnalités

    🔑 Génération de paires de clés RSA

    🔐 Chiffrement/déchiffrement (AES-256, 3DES, RSA)

    📝 Signature et vérification de documents

    🔎 Calcul d'empreintes numériques (SHA256, MD5)

📦 Prérequis

    Python 3.8+

    OpenSSL installé sur le système

    Paquets Python : rich, pyfiglet

🛠 Installation


Installation manuelle :

    Clonez le dépôt :


git clone https://github.com/Mahery19/cryptographie.git
cd cryptotool


🚀 Utilisation

Lancez simplement :

cryptotool

Menu principal :

1. Génération de clé privée (RSA)
2. Chiffrement d'une clé privée (AES/3DES)
3. Génération de clé publique (RSA)
4. Chiffrement de données (RSA/AES/3DES)
5. Déchiffrement de données (RSA/AES/3DES)
6. Calcul d'empreinte (MD5/SHA256)
7. Signature d'empreinte (RSA)
8. Vérification de signature (RSA)
99. Quitter

🔐 Guide des Fonctions
1. Génération de clé privée RSA

Crée une clé privée RSA 2048 bits :

Nom de la clé privée : ma_cle.prv

2. Chiffrement de clé privée

Protège une clé privée avec AES ou 3DES :


Nom de la clé à chiffrer : ma_cle.prv
Algorithme (aes256, des3) : aes256

3. Génération de clé publique

Extrait la clé publique d'une clé privée :


Clé privée : ma_cle.prv
Nom de la clé publique : ma_cle.pub

4. Chiffrement de données

Chiffre un fichier avec différents algorithmes :


Fichier à chiffrer : document.txt
Algorithme (RSA, AES-256, 3-DES) : AES-256

5. Déchiffrement de données

Déchiffre un fichier précédemment chiffré :


Fichier à déchiffrer : document.enc
Algorithme (RSA, AES-256, 3-DES) : AES-256

6. Calcul d'empreinte

Calcule le hash d'un fichier :


Fonction de hashage (md5, sha256) : sha256
Fichier source : document.txt

7. Signature numérique

Signe un fichier avec une clé privée :


Fichier à signer : document.txt
Clé privée : ma_cle.prv

8. Vérification de signature

Vérifie l'authenticité d'un fichier signé :


Fichier original : document.txt
Fichier de signature : document.sig
Clé publique : ma_cle.pub

🛠 Développement
Structure du code :

    main.py : Point d'entrée principal

    crypto_operations.py : Fonctions cryptographiques

    ui.py : Interface utilisateur

Tests :


python -m pytest tests/

📄 Licence

MIT License - Libre d'utilisation et modification
🤝 Contribution

Les pull requests sont les bienvenues !