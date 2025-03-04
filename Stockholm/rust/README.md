# 🔐 Rust File Encryptor

## Description
Ce projet est un outil de chiffrement et de déchiffrement de fichiers en **Rust**, utilisant l'algorithme **ChaCha20** avec un **HMAC-SHA256** pour garantir l'intégrité des données.  
Il permet d'ajouter une extension `.ft` aux fichiers chiffrés et de les restaurer à leur état d'origine.

## 📦 Installation et Compilation
Aucune dépendance supplémentaire n'est requise pour compiler le projet.  
Assurez-vous simplement d'avoir **Rust** et **Make** installés sur votre machine.

## Lancer le programme
Apres avoir fais make vous pouvez simplement faire ./exe pour lancer le chiffrement des donnees

## Comment l'utiliser
Utilisation: exe [OPTIONS]

Options:
  -s, --silent             
  -r, --reverse <REVERSE>  
  -h, --help               Print help
  -V, --version            Print version