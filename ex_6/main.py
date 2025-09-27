import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# Diretórios
BASE_DIR = os.path.dirname(__file__)
OUT = os.path.join(BASE_DIR, "out")
os.makedirs(OUT, exist_ok=True)

# Caminhos de arquivos
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "..", "ex_1", "out", "private.pem")
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "..", "ex_1", "out", "public.pem")
MSG_FILE = os.path.join(BASE_DIR, "msg.txt")
ENC_FILE = os.path.join(OUT, "msg.enc")
SIG_FILE = os.path.join(OUT, "msg.sig")
EXPLAIN_FILE = os.path.join(OUT, "explain.txt")

# --- Ler chaves ---
with open(PRIVATE_KEY_PATH, "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open(PUBLIC_KEY_PATH, "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# --- Ler mensagem ---
with open(MSG_FILE, "rb") as f:
    message = f.read()

# --- CIFRAR (confidencialidade) ---
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open(ENC_FILE, "wb") as f:
    f.write(ciphertext)

# --- ASSINAR (autenticidade) ---
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

with open(SIG_FILE, "wb") as f:
    f.write(signature)

# --- Explicação ---
explanation = """
Cifrar (msg.enc) com a chave pública garante que somente o dono da chave privada pode ler.
Assinar (msg.sig) com a chave privada permite que qualquer pessoa com a chave pública valide a origem.
Quem recebe msg.enc precisa da privada para decifrar, mas não precisa da assinatura.
Quem recebe msg.sig precisa da pública para verificar, mas não consegue ler o conteúdo secreto apenas com a assinatura.
Cifrar protege confidencialidade; assinar protege autenticidade e integridade.
"""

with open(EXPLAIN_FILE, "w") as f:
    f.write(explanation.strip())

print("EX6 concluído.")
print("Saídas geradas em out/: msg.enc, msg.sig e explain.txt")