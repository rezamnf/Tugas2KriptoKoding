key = None

#-----UTILITIES-----
def str2bin(text):
# Mengkonversi string menjadi string biner
    if type(text) == str:
        return ''.join(format(ord(i), '08b') for i in text)
    return

def binstr2bin(binstr):
# Mengkonversi string biner menjadi biner
    in_bytes = bytes('', 'utf-8')
    split8 = [binstr[i:i+8] for i in range(0, len(binstr), 8)]
    for byte in split8:
        in_bytes += struct.pack('B', int(byte, 2))
    return in_bytes

def file2binstr(path):
# Mengkonversi file menjadi string biner
    file = open(path, 'rb')
    content = file.read()
    file.close()
    return ''.join([format(i, "08b") for i in content])

def str_to_ints(input_text: str):
# Mengkonversi string menjadi list of integer
    return [ord(char) for char in input_text]

def str_to_strbinaries(input_text: str) -> str:
# Mengkonversi string menjadi biner dari string tersebut
    result = ""
    for char in input_text:
        result += format(ord(char), "08b")
    return "".join(result)

def strbinaries_to_char(content) -> str:
# Mengkonversi list of string yang merepresentasikan biner ke string
    result = ""
    for i in range(len(content)//8):
        byte = content[i*8 : (i+1)*8]
        result += chr(int(byte, 2))
    return result

def cr4_convert_char_to_binstr(content):
# Mengkonversi string text menjadi list of string yang merepresentasikan biner setiap karakter dari string text
    result = []
    for char in content:
        result.append(format(ord(char), "08b"))
    return result

def readfile_txt(filename: str = "plaintext.txt"):
# Membaca file menjadi string
    from pathlib import Path

    path = filename
    
    with open(path, "r") as file:
        return file.readlines()

def writefile_txt(filename: str="output.txt", content:str=""):
# Menulis string ke dalam file
    from pathlib import Path

    path = filename

    with open(path, 'wb') as file:
        file.write(content)

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

def savefile(content, filename, ext):
    path = "output_decode/" + filename + "." + ext
    file = open(path, 'wb')
    file.write(content)
    file.close 


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

def cr4_encrypt_message(message):
# Melakukan enkripsi dengan modified RC4
    global key
    
    message_text = strbinaries_to_char(message)
    
    enc_message_text = encrypt_text(message_text)
    
    enc_message = str_to_strbinaries(enc_message_text)
    
    return enc_message

def cr4_decrypt_file(filename, extension):
# Membaca file dan melakukan dekripsi dengan modified RC4   
    path = "output_decode/" + filename + "." + extension
    content_binstr = file2binstr(path)

    content_text = strbinaries_to_char(content_binstr)

    content_text = decrypt_text(content_text)

    decr_content = binstr2bin(str2bin(content_text))

    savefile(decr_content, filename, extension)

def feistel(input_message: str, input_key: str, encrypt: bool, num_of_steps: int = 25) -> str:
# Melakukan enkripsi dengan algoritma feistel cipher
    n_message_part = len(input_message)//2
    n_key = len(input_key)
    if num_of_steps != 0:
        n_key_part = n_key//num_of_steps
    subpart1 = input_message[:n_message_part]
    subpart2 = input_message[n_message_part:]

    if encrypt:
        iterate_key = range(num_of_steps)
    else:
        iterate_key = range(num_of_steps)[::-1]

    for i in iterate_key:
        subkey_i = input_key[i*n_key_part:(i+1)*n_key_part]

        keystream_i = lfsr_txt(subpart2, subkey_i)
        func_result = xor_message(subpart2, keystream_i)

        xor_result = xor_message(subpart1, str_to_ints(func_result))
        
        subpart1, subpart2 = subpart2, xor_result
        
    subpart1, subpart2 = subpart2, subpart1
    return subpart1 + subpart2

def lfsr_txt(input_message: str, subkey: str):
# Membentuk keystream dengan algoritma linear shift register key
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
# Melakukan enkripsi plaintext sesuai array permutasi berdasarkan algoritma RC4, kemudian dilanjutkan enkripsi dengan algoritma feistel
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
    
    C = feistel(C, str_to_strbinaries(key), encrypt=True)
    return C

def decrypt_text(C: str) -> str:
# Melakukan deskripsi dengan algoritma feister, kemudian dilanjutkan dengan dekripsi sesuai array permutasi berdasarkan algoritma RC4
    global key
    S = KSA(key)

    C = feistel(C, str_to_strbinaries(key), encrypt=False)

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