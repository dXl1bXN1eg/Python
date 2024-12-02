def decode(encoded):
    decoded = ""
    count = 0

    for i in range(0, len(encoded), 2):  
        hex_pair = encoded[i:i+2]
        char_code = int(hex_pair, 16)
        original_char = chr(char_code - count % 10)
        decoded += original_char
        count += 1

    return decoded  

encoded_text = "636275777377"  
decoded_text = decode(encoded_text)
print(f"Decoded Text: {decoded_text}")  
