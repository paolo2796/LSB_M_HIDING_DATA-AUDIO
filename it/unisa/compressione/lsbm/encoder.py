import sys
# We will use wave package available in native Python installation to read and write .wav audio file
import wave
import array
import numpy as np
import struct
from pydub import AudioSegment


# CONSTANTS DEF
PATH_PROJ = sys.path[1]
PATH_INPUT_FILE_AUDIO1 = PATH_PROJ + "/file_audio/audio1.wav"
PATH_OUTPUT_FILE_AUDIO1 = PATH_PROJ + "/file_audio/encoded/audio1_lsbm.wav"



# FUNCTIONS
def most_significant_bit(frame):
    var_bin = format(frame,'#010b')
    return var_bin[2:4]

def bit_selection_replaced(frame,bit_message):
    msb = most_significant_bit(frame)
    frame_list = list(format(frame,'#010b'))
    if(msb == "00"):
        frame_list[len(frame_list) - 3] = bit_message
    elif(msb  == "01"):
        frame_list[len(frame_list) - 2] = bit_message
    elif(msb  == "10" or msb  == "11"):
        frame_list[len(frame_list) - 1] = bit_message
    string = ""
    for character in frame_list:
        string = string + str(character)

    return int(string[2:], 2)



# read wave audio file
song = wave.open(PATH_INPUT_FILE_AUDIO1, mode='rb')
# Read frames and convert to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# The "secret" text message
string="MESSAGGIO NASCOSTO DA PAOLETTO"
# Numero minimo di campioni richiesti per l'iniezione del messaggio segreto
num_min_samples = len(string)*8*8
# Calcolo campioni rimanenti per aggiungere bit di padding al messaggio segreto
dif_samples_padding = len(frame_bytes) - num_min_samples
# Divido per 8 in modo tale da calcolare il numero di caratteri di padding da aggiungere al messaggio segreto
num_char_padding = int(dif_samples_padding/8)


# Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
string = string + num_char_padding *'#'
# Convert text to bit array
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
# Replace LSB of each byte of the audio data by one bit from the text bit array
for i, bit in enumerate(bits):
        frame_bytes[i] = bit_selection_replaced(frame_bytes[i],bit)


# Get the modified bytes
frame_modified = bytes(frame_bytes)

# Write bytes to a new wave audio file
with wave.open(PATH_OUTPUT_FILE_AUDIO1, 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)

song.close()




