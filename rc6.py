""""All the opretaion used in the coding and decoding."""

def generate_key(key,r=20,w=32,):
    r=12
    w=32
    b=len(key)
    modulo = 2**32
    s=(2*r+4)*[0]
    s[0]=0xB7E15163
    for i in range(1,2*r+4):
        s[i]=(s[i-1]+0x9E3779B9)%(2**w)
    encoded = convert_to_block(key)

    enlength = len(encoded)
    l = enlength*[0]
    for i in range(1,enlength+1):
        l[enlength-i]=int(encoded[i-1],2)
    
    v = 3*max(enlength,2*r+4)
    A=B=i=j=0
    
    for k in range(0,v):
        A = s[i] = rotl((s[i] + A + B)%modulo,3,32)
        B = l[j] = rotl((l[j] + A + B)%modulo,(A+B)%32,32) 
        i = (i + 1) % (2*r + 4)
        j = (j + 1) % enlength
    return s

def rotl(x,n,bits = 32):
    return rotr(x, bits - n,bits)

def rotr(x,n,bits=32):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))

def convert_to_block(sentence):
    result = []
    aux = ""
    for i in range(0,len(sentence)):
        if i != 0 and i%4 == 0:
            result.append(aux)
            aux = ""
        temp = bin(ord(sentence[i]))[2:]
        if len(temp) < 8:
            temp = "0"*(8- len(temp)) + temp
        aux = aux + temp
    
    result.append(aux)
    return result

def convert_to_array(blocks):
    s = ""
    for ele in blocks:
        temp =bin(ele)[2:]
        if len(temp) <32:
            temp = "0"*(32-len(temp)) + temp
        for i in range(0,4):
            s=s+chr(int(temp[i*8:(i+1)*8],2))
    return s

def encrypt(sentence, s, r=12, w=32):
    block_sentence = convert_to_block(sentence)
    block_sentence_l = len(block_sentence)

    A = int(block_sentence[0],2)
    B = int(block_sentence[1],2)
    C = int(block_sentence[2],2)
    D = int(block_sentence[3],2)
    print(A)
    original = []
    original.append(A)
    original.append(B)
    original.append(C)
    original.append(D)

    modulo = 2**32
    lgw = 5

    modulo = 2**32
    lgw = 5
    B = (B + s[0])%modulo
    D = (D + s[1])%modulo 
    for i in range(1,r+1):
        t_temp = (B*(2*B + 1))%modulo 
        t = rotl(t_temp,lgw,32)
        u_temp = (D*(2*D + 1))%modulo
        u = rotl(u_temp,lgw,32)
        tmod=t%32
        umod=u%32
        A = (rotl(A^t,umod,32) + s[2*i])%modulo 
        C = (rotl(C^u,tmod,32) + s[2*i+ 1])%modulo
        (A, B, C, D)  =  (B, C, D, A)
    A = (A + s[2*r + 2])%modulo 
    C = (C + s[2*r + 3])%modulo
    ciphered_message = []
    ciphered_message.append(A)
    ciphered_message.append(B)
    ciphered_message.append(C)
    ciphered_message.append(D)
    return ciphered_message
                                                                                    
def decrypt(esentence,s):
    encoded = convert_to_block(esentence)
    enlength = len(encoded)
    A = int(encoded[0],2)
    B = int(encoded[1],2)
    C = int(encoded[2],2)
    D = int(encoded[3],2)
    cipher = []
    cipher.append(A)
    cipher.append(B)
    cipher.append(C)
    cipher.append(D)
    r=12
    w=32
    modulo = 2**32
    lgw = 5
    C = (C - s[2*r+3])%modulo
    A = (A - s[2*r+2])%modulo
    for j in range(1,r+1):
        i = r+1-j
        (A, B, C, D) = (D, A, B, C)
        u_temp = (D*(2*D + 1))%modulo
        u = rotl(u_temp,lgw,32)
        t_temp = (B*(2*B + 1))%modulo 
        t = rotl(t_temp,lgw,32)
        tmod=t%32
        umod=u%32
        C = (rotr((C-s[2*i+1])%modulo,tmod,32)  ^u)  
        A = (rotr((A-s[2*i])%modulo,umod,32)   ^t) 
    D = (D - s[1])%modulo 
    B = (B - s[0])%modulo
    orgi = []
    orgi.append(A)
    orgi.append(B)
    orgi.append(C)
    orgi.append(D)
    return orgi

