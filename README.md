# 🔐 Secure File Vault

A password-based file encryption and decryption web application built using Flask and modern cryptographic standards.

## 🔒 Features
- Password-based encryption & decryption
- AES-128 encryption using Fernet
- PBKDF2 key derivation with SHA-256
- Random salt per file
- HMAC-based integrity verification

## 🛠️ Technology Stack
- Python
- Flask
- Cryptography Library
- HTML, CSS

## ⚙️ How It Works
1. User uploads a file and provides a password
2. A cryptographic key is derived using PBKDF2 + SHA-256
3. File is encrypted using AES (Fernet)
4. Salt is stored with encrypted data
5. Same password is required for decryption

## 🚀 Run Locally
```bash
pip install -r requirements.txt
python app.py
