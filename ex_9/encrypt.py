from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import os

OUT = "ex9_import_keys/out"
os.makedirs(OUT, exist_ok=True)

with open("ex1_rsa_gen/out/public.pem","rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

msg = open("ex9_import_keys/produto.txt","rb").read()

cipher = public_key.encrypt(msg,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

open(f"{OUT}/produto.enc","wb").write(cipher)
print("Encrypt concluído. Arquivo em out/produto.enc")
