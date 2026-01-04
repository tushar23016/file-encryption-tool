from flask import Flask, render_template, request, send_file
import os
import io
import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

"""
---------------------------------------------------------
Secure File Vault – Backend Logic
---------------------------------------------------------
Encryption Algorithm : AES-128 (Fernet)
Key Derivation       : PBKDF2 with SHA-256
Salt                : Random 16 bytes (per file)
Iterations           : 100,000
Encryption Type      : Symmetric Encryption
Integrity            : HMAC Authentication
---------------------------------------------------------
"""

app = Flask(__name__)
app.secret_key = "minor_project_secret"

# Create upload directory (not mandatory, but safe)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def generate_key(password: str, salt: bytes) -> bytes:
    """
    Generates a cryptographic key from a password using PBKDF2.

    Parameters:
    - password: User-provided password
    - salt: Random salt (16 bytes)

    Returns:
    - Base64 encoded 32-byte key suitable for Fernet
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,              # Fernet requires 32-byte key
        salt=salt,
        iterations=100000       # Industry-recommended iteration count
    )
    return base64.urlsafe_b64encode(
        kdf.derive(password.encode())
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    file = request.files["file"]
    password = request.form["password"]

    # Read original file data
    data = file.read()

    # Generate random salt for this file
    salt = os.urandom(16)

    # Derive encryption key from password + salt
    key = generate_key(password, salt)
    fernet = Fernet(key)

    # Encrypt data
    encrypted_data = fernet.encrypt(data)

    # Store salt + encrypted content together
    final_data = salt + encrypted_data

    return send_file(
        io.BytesIO(final_data),
        as_attachment=True,
        download_name=file.filename + ".enc"
    )


@app.route("/decrypt", methods=["POST"])
def decrypt():
    file = request.files["file"]
    password = request.form["password"]

    # Read encrypted file
    file_data = file.read()

    # Extract salt and encrypted payload
    salt = file_data[:16]
    encrypted_data = file_data[16:]

    # Regenerate key using same password + salt
    key = generate_key(password, salt)
    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception:
        # Authentication failed (wrong password or tampered file)
        return "❌ Wrong password or corrupted file"

    return send_file(
        io.BytesIO(decrypted_data),
        as_attachment=True,
        download_name=file.filename.replace(".enc", "")
    )


if __name__ == "__main__":
    # For local testing
    app.run(host="0.0.0.0", port=5000)
