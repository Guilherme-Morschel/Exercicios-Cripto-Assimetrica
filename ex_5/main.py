import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Diretórios
BASE_DIR = os.path.dirname(__file__)
OUT = os.path.join(BASE_DIR, "out")
os.makedirs(OUT, exist_ok=True)

# Caminhos
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "..", "ex_1", "out", "private.pem")
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "..", "ex_1", "out", "public.pem")
DOC_FILE = os.path.join(BASE_DIR, "doc.txt")
SIG_FILE = os.path.join(OUT, "doc.sig")
VERIFY_FILE = os.path.join(OUT, "verify.txt")

# --- Ler chaves ---
with open(PRIVATE_KEY_PATH, "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open(PUBLIC_KEY_PATH, "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# --- Ler documento ---
with open(DOC_FILE, "rb") as f:
    doc_data = f.read()

# --- Assinar documento ---
signature = private_key.sign(
    doc_data,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Salvar assinatura
with open(SIG_FILE, "wb") as f:
    f.write(signature)

# --- Verificar assinatura ---
try:
    public_key.verify(
        signature,
        doc_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    verify_result = "OK - assinatura válida"
except:
    verify_result = "FAIL - assinatura inválida"

# Salvar resultado
with open(VERIFY_FILE, "w") as f:
    f.write(verify_result + "\n")

print("EX5 concluído.")
print(verify_result)

# --- Alterar 1 byte para demonstrar falha ---
doc_data_altered = bytearray(doc_data)
doc_data_altered[0] ^= 0x01  # altera 1 bit no primeiro byte

try:
    public_key.verify(
        signature,
        doc_data_altered,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    altered_result = "OK - assinatura válida"
except:
    altered_result = "FAIL - assinatura inválida"

with open(VERIFY_FILE, "a") as f:
    f.write("Após alterar 1 byte: " + altered_result + "\n")

print("Após alterar 1 byte:", altered_result)
