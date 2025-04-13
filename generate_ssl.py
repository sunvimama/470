from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import Name, NameAttribute, CertificateBuilder
from cryptography.x509.oid import NameOID
from cryptography.x509 import SubjectAlternativeName, DNSName
import datetime
from cryptography.hazmat.primitives import hashes

def generate_self_signed_cert(cert_file, key_file):
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Create the subject and issuer names
    subject = issuer = Name([NameAttribute(NameOID.COMMON_NAME, "localhost")])

    # Build the certificate
    cert = CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
        private_key.public_key()).serial_number(1000).not_valid_before(datetime.datetime.now(datetime.timezone.utc)).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)).add_extension(
        SubjectAlternativeName([DNSName("localhost")]), critical=False).sign(private_key, hashes.SHA256(), default_backend())

    # Save private key to file
    with open(key_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save certificate to file
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

# Generate self-signed certificate and key
generate_self_signed_cert("server.crt", "server.key")

