import hashlib

def calculate_hash(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
        return hashlib.sha256(file_data).hexdigest()

file_path = "malware_sample.exe"
print(f"SHA-256 Hash: {calculate_hash(file_path)}")
