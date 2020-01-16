import sys
from pydub import AudioSegment
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


# CONSTANTS
PATH_PROJ = sys.path[1]
PATH_INPUT_FILE_AUDIO1 = "./file_audio/audio1.wav"
PATH_OUTPUT_FILE_AUDIO1 = "./file_audio/encoded/audio1_stego.wav"
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


# restituisce i due bit più significativi del campione
def most_significant_bit(frame):
    var_bin = format(frame,'#0b')
    if(var_bin[0]=='-' and len(var_bin)<7):
        var_bin = format(frame,'#019b')
    elif(var_bin[0]=='0' and len(var_bin)<6):
        var_bin = format(frame,'#018b')
    return var_bin[3:5] if var_bin[0]=='-' else var_bin[2:4]

# sostituisco uno dei tre bit meno significativi del campione a seconda del valore dei due bit più significativi
def bit_selection_replaced(sample,bit_message):
    msb = most_significant_bit(sample)
    sample_list = list(format(sample,'#018b'))
    if(sample_list[0]=='-'):
        sample_list = list(format(sample,'#019b'))

    if(msb == "00"):
        sample_list[len(sample_list) - 3] = bit_message
    elif(msb  == "01"):
        sample_list[len(sample_list) - 2] = bit_message
    elif(msb  == "10" or msb  == "11"):
        sample_list[len(sample_list) - 1] = bit_message

    string = ""
    for character in sample_list:
        string = string + str(character)

    return int('-' + string[3:] if string[0]=='-' else string[2:], 2)



#read wave audio file
song = AudioSegment.from_wav(PATH_INPUT_FILE_AUDIO1)
#samples of audio wav
samples = song.get_array_of_samples()
# secret message
string = input("inserisci testo segreto: ")
#chiave simmetrica per cifrare il testo (AES-256)
password = input("Inserisci password per la cifratura del testo: ")
# Eseguo cifratura del testo segreto
encrypted = encrypt(string, password)
string_enc = bytes.decode(encrypted)

# Numero minimo di campioni richiesti per l'iniezione del messaggio segreto
num_min_samples = len(string_enc)*8

# Calcolo campioni rimanenti per aggiungere bit di padding al messaggio segreto
dif_samples_padding = len(samples) - num_min_samples
# Divido per 8 in modo tale da calcolare il numero di caratteri di padding da aggiungere al messaggio segreto
num_char_padding = int(dif_samples_padding/8)
# testo segreto con padding
string_enc = string_enc + (num_char_padding *'#')
# Convert text to bit array
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string_enc])))

# Applico tecnica lsbm
for i, bit in enumerate(bits):
    try:
        samples[i] = bit_selection_replaced(samples[i],bit)
    except:
        # hack avoid underflow and overflow
        if(samples[i]>0):
            samples[i] = samples[i] - 1
        else:
            samples[i] = samples[i] + 1

        samples[i] = bit_selection_replaced(samples[i],bit)

# Get the modified bytes
stego_song = song._spawn(samples)
stego_song.export(PATH_OUTPUT_FILE_AUDIO1,format="wav")
print("File stego salvato!")



