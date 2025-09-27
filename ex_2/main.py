import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# Diretórios
BASE_DIR = os.path.dirname(__file__)
OUT = os.path.join(BASE_DIR, "out")
os.makedirs(OUT, exist_ok=True)

# Caminhos de arquivos
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "..", "ex_1", "out", "public.pem")
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "..", "ex_1", "out", "private.pem")
INPUT_FILE = os.path.join(BASE_DIR, "in.txt")
CIPHER_FILE = os.path.join(OUT, "cipher.bin")
PLAIN_FILE = os.path.join(OUT, "plain.txt")

# Ler chave pública
with open(PUBLIC_KEY_PATH, "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Ler chave privada
with open(PRIVATE_KEY_PATH, "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Ler mensagem original
with open(INPUT_FILE, "rb") as f:
    message = f.read()

# --- CIFRAR ---
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Salvar ciphertext
with open(CIPHER_FILE, "wb") as f:
    f.write(ciphertext)

# --- DECIFRAR ---
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Salvar plaintext
with open(PLAIN_FILE, "wb") as f:
    f.write(plaintext)

print("EX2 concluído.")
print(f"Mensagem original: {message.decode(errors='ignore')}")
print(f"Mensagem decifrada: {plaintext.decode(errors='ignore')}")
