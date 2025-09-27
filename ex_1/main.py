from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import hashlib, os

OUT = "ex_1/out"
os.makedirs(OUT, exist_ok=True)

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pub = key.public_key()

with open(f"{OUT}/private.pem","wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open(f"{OUT}/public.pem","wb") as f:
    f.write(pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

fp = hashlib.sha256(pub.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)).hexdigest()

with open(f"{OUT}/info.txt","w") as f:
    f.write(f"mod_bits={key.key_size}\nsha256_fp={fp}\n")

print("EX1 concluído. Chaves em", OUT)
