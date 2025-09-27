from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import os

OUT = "ex9_import_keys/out"
os.makedirs(OUT, exist_ok=True)

with open("ex1_rsa_gen/out/private.pem","rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

cipher = open("ex9_import_keys/out/produto.enc","rb").read()

plain = private_key.decrypt(cipher,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

open(f"{OUT}/produto.dec.txt","wb").write(plain)
print("Decrypt concluído. Arquivo em out/produto.dec.txt")
