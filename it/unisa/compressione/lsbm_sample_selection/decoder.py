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


# FUNCTIONS
def most_significant_bit_three(frame):
    var_bin = format(frame,'#0b')
    if(var_bin[0]=='-' and len(var_bin)<7):
        var_bin = format(frame,'#019b')
    elif(var_bin[0]=='0' and len(var_bin)<6):
        var_bin = format(frame,'#018b')
    return var_bin[3:6] if var_bin[0]=='-' else var_bin[2:5]

def sample_exploitable():
    count=[]
    i=0
    while i<len(samples):
        msb = most_significant_bit_three(samples[i])
        if (msb == "000"):
            i=i+1
        elif (msb == "001"):
            i=i+2
        elif (msb == "010"):
            i=i+3
        elif (msb == "011"):
            i=i+4
        elif (msb == "100"):
            i=i+5
        elif (msb == "101"):
            i=i+6
        elif (msb == "110"):
            i=i+7
        elif (msb == "111"):
            i=i+8

        if(i< len(samples))==True:
            count.append(i)
    return count


# CONSTANTS
PATH_PROJ = sys.path[1]
PATH_INPUT_FILE_AUDIO1_MODIFIED = "./file_audio/encoded/audio1_stego.wav"


def bit_selection_extracted(sample):
    sample_list = list(format(sample,'#018b'))
    if(sample_list[0]=='-'):
        sample_list = list(format(sample,'#019b'))
    return sample_list[len(sample_list) - 1]




password = input("Inserisci password per decifrare il testo: ")
# open audio file .wav
stego_song = AudioSegment.from_wav(PATH_INPUT_FILE_AUDIO1_MODIFIED)

# campioni audio
samples = stego_song.get_array_of_samples()

extracted = list()

# Ottengo campioni dove sono nascosti i bit del testo segreto
samples_exploitable_arr =  sample_exploitable()
#print("lunghezza samples exploitable_arr " + len(samples_exploitable_arr).__str__())
#print("lunghezza samples " + len(samples).__str__())
# Estrazione testo segreto
i=0
while i < len(samples_exploitable_arr):
    extracted.append(bit_selection_extracted(samples[samples_exploitable_arr[i]]))
    i=i+1


# Convert byte array back to string
string_enc = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# Cut off at the filler characters
decoded = string_enc.split("#")[0]
decrypted = decrypt(decoded, password)
string_dec = bytes.decode(decrypted)
# Print the extracted text
print("Decifratura eseguita con successo:")
print(string_dec)