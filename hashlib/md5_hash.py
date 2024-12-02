import hashlib

def find_ip_from_md5(target_hash):
    for i in range(256):  
        for j in range(256):
            for k in range(256):
                for l in range(256):
                    ip = f"{i}.{j}.{k}.{l}"
                    # IP adresini MD5 ile hashle
                    hash_object = hashlib.md5(ip.encode())
                    ip_hash = hash_object.hexdigest()
                    
                    # Eğer hash değeri eşleşirse, IP'yi döndür
                    if ip_hash == target_hash:
                        return ip
    return None

# Verilen MD5 hash
target_md5_hash = "fc4d88b57d57592a256c636634a10c6a"

ip_address = find_ip_from_md5(target_md5_hash)

if ip_address:
    print(f"Hash değeri {target_md5_hash} IP adresine karşılık gelir: {ip_address}")
else:
    print("Hash ile eşleşen IP adresi bulunamadı.")
