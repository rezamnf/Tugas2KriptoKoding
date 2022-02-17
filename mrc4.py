import struct

key = None

#-----UTILITIES-----
def str_to_ints(input_text: str):
# Mengkonversi string menjadi list of integer
    return [ord(char) for char in input_text]

def str_to_strbinaries(input_text: str) -> str:
# Mengkonversi string menjadi biner dari string tersebut
    result = ""
    for char in input_text:
        result += format(ord(char), "08b")
    return "".join(result)

def readfile_bin(filename: str = "blue.png"):
# Membaca file menjadi biner
    from pathlib import Path
    path = filename
    
    with open(path, 'rb') as file:
        temp = []
        byte = file.read(1)
        while byte:
            temp.append(int.from_bytes(byte, "big"))
            byte = file.read(1)
        
        temp = [bin(bits)[2:] for bits in temp]
        result = []
        for e in temp:
            if len(e) < 8:
                e = (8 - len(e)) * "0" + e
            result.append(e)

        return "".join([chr(int(e, 2)) for e in result])

def writefile_bin(filename: str="output.png", content: str=""):
# Menulis biner ke dalam file
    from pathlib import Path

    path = filename
    
    with open(path, 'wb') as file:
        bytes = []
        for char in content:
            byte = int.to_bytes(ord(char), 1, "big")
            bytes.append(byte)
        file.write(b"".join(bytes))

#-----MODIFIED RC4-----
def acquire_key(input_key):
    global key
    key = input_key

def xor_message(message: str, keystream) -> str:
# Melakukan XOR antara message (string) dengan keystream list of integer 0-255
    result = ""
    n_keystream = len(keystream)
    message_ints = str_to_ints(message)
    for idx in range(len(message_ints)):
        result += chr(message_ints[idx] ^ keystream[idx%n_keystream])
    return result

def lfsr(input_message: str, subkey: str):
# Membentuk keystream dengan algoritma linear feedback register key
    def xor_bits(bits):
        result = 0
        for bit in bits:
            result ^= bit
        return result
    
    n_input_message = len(input_message)
    register = [1 if bit == "1" else 0 for bit in subkey]
    keystream = []
    i = 0
    while i < n_input_message:
        temp = "0b"
        for _ in range(8):
            register.append(xor_bits(register))
            temp += str(register.pop(0))
        keystream.append(int(temp, 2))
        i += 1
    return keystream

def KSA(key: str):
# Inisialisasi array dengan permutasi untuk algoritma RC4
    key = str_to_strbinaries(key)
    temp = [i for i in range(256)]
    lk = len(key)
    j = 0
    for i in range(256):
        j = (j + temp[i] + int(key[i%lk])) % 256
        temp[i], temp[j] = temp[j], temp[i]
    return temp

def encrypt_text(P: str) -> str:
# Melakukan enkripsi plaintext sesuai array permutasi berdasarkan algoritma RC4, kemudian hasil eknripsi dikenakan XOR dan LFSR
    global key
    S = KSA(key)
    i = j = 0
    C = ""
    for idx in range(len(P)):
        i = (i + 1) % 256     
        j = (j + S[i]) % 256  
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        u = S[t] 
        c_bytes = u ^ ord(P[idx])
        C += chr(c_bytes)

    return xor_message(C, lfsr(C,S))

def decrypt_text(C: str) -> str:
# Melakukan deskripsi menggunakan XOR dan LFSR, kemudian dilanjutkan dengan dekripsi sesuai array permutasi berdasarkan algoritma RC4
    global key
    S = KSA(key)
    C = xor_message(C, lfsr(C,S))
    i = j = 0
    P = ""
    for idx in range(len(C)):
        i = (i + 1) % 256 
        j = (j + S[i]) % 256  
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        u = S[t]  
        p_bytes = u ^ ord(C[idx]) 
        P += chr(p_bytes)

    return P