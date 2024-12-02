import hashlib

"""data = "Hello World"

md5_hash = hashlib.md5(data.encode()).hexdigest()

print(f"String: {data}")
print(f"MD5 Hash: {md5_hash}")"""


file_path = 'path/to/your/file.txt'

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

md5_hash = calculate_md5(file_path)
print(f"File: {file_path}")
print(f"MD5 Hash: {md5_hash}")