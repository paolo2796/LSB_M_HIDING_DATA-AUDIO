import sys
from pydub import AudioSegment # lettura file mp3
from pyo import *
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


# CONSTANTS
PATH_PROJ = sys.path[1]
PATH_INPUT_FILE_AUDIO1_MODIFIED = "./file_audio/encoded/audio1_stego.wav"

# FUNCTIONS
def most_significant_bit(frame):
    var_bin = format(frame,'#0b')
    if(var_bin[0]=='-' and len(var_bin)<7):
        var_bin = format(frame,'#019b')
    elif(var_bin[0]=='0' and len(var_bin)<6):
        var_bin = format(frame,'#018b')
    return var_bin[3:5] if var_bin[0]=='-' else var_bin[2:4]

def bit_selection_extracted(sample):
    msb = most_significant_bit(sample)
    sample_list = list(format(sample,'#018b'))
    if(sample_list[0]=='-'):
        sample_list = list(format(sample,'#019b'))
    if(msb == "00"):
        return sample_list[len(sample_list) - 3]
    elif(msb  == "01"):
        return sample_list[len(sample_list) - 2]
    elif(msb  == "10" or msb  == "11"):
        return sample_list[len(sample_list) - 1]



password = input("Inserisci password per decifrare il testo: ")

# open audio file .wav
stego_song = AudioSegment.from_wav(PATH_INPUT_FILE_AUDIO1_MODIFIED)

# campioni audio
samples = stego_song.get_array_of_samples()

extracted = list()
# Estrazione testo segreto
for sample in samples:
    extracted.append(bit_selection_extracted(sample))

# Convert byte array back to string
string_enc = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# Cut off at the filler characters
decoded = string_enc.split("#")[0]
decrypted = decrypt(decoded, password)
string_dec = bytes.decode(decrypted)
# Print the extracted text
print("Sucessfully decoded:")
print(string_dec)