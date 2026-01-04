from flask import Flask, render_template, request, send_file, redirect, url_for
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.secret_key = "minor_project_secret"


UPLOAD_FOLDER = 'uploads'
ENCRYPTED_FOLDER = 'encrypted'
DECRYPTED_FOLDER = 'decrypted'
KEY_FOLDER = 'keys'
KEY_PATH = os.path.join(KEY_FOLDER, 'key.key')

# Create required folders
for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER, KEY_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Generate key once
if not os.path.exists(KEY_PATH):
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)

with open(KEY_PATH, "rb") as k:
    key = k.read()

fernet = Fernet(key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    if "file" not in request.files or request.files["file"].filename == "":
        return redirect(url_for("index"))

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)
    enc_path = os.path.join(ENCRYPTED_FOLDER, file.filename + ".enc")

    with open(enc_path, "wb") as e:
        e.write(encrypted)

    return send_file(enc_path, as_attachment=True)

@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "file" not in request.files or request.files["file"].filename == "":
        return redirect(url_for("index"))

    file = request.files["file"]
    enc_path = os.path.join(ENCRYPTED_FOLDER, file.filename)
    file.save(enc_path)

    with open(enc_path, "rb") as f:
        encrypted = f.read()

    decrypted = fernet.decrypt(encrypted)
    dec_filename = file.filename.replace(".enc", "")
    dec_path = os.path.join(DECRYPTED_FOLDER, "decrypted_" + dec_filename)

    with open(dec_path, "wb") as d:
        d.write(decrypted)

    return send_file(dec_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
