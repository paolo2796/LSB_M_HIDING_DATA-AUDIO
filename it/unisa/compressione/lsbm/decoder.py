import sys
# Use wave package (native to Python) for reading the received audio file
import wave

from pyo import *


# CONSTANTS
PATH_PROJ = sys.path[1]
PATH_INPUT_FILE_AUDIO1_MODIFIED = PATH_PROJ + "/file_audio/encoded/audio1_lsbm.wav"


# FUNCTIONS
def most_significant_bit(frame):
    var_bin = format(frame,'#010b')
    return var_bin[2:4]


def bit_selection_extracted(frame):
    msb = most_significant_bit(frame)
    frame_list = list(format(frame,'#010b'))
    if(msb == "00"):
        return frame_list[len(frame_list) - 3]
    elif(msb  == "01"):
        return frame_list[len(frame_list) - 2]
    elif(msb  == "10" or msb  == "11"):
        return frame_list[len(frame_list) - 1]
    return frame_list[len(frame_list) - 1]

song = wave.open(PATH_INPUT_FILE_AUDIO1_MODIFIED, mode='rb')
# Convert audio to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

extracted = list()
# Extract the LSB of each byte
for frame in frame_bytes:
    extracted.append(bit_selection_extracted(frame))

# Convert byte array back to string
string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# Cut off at the filler characters
decoded = string.split("#")[0]

# Print the extracted text
print("Sucessfully decoded:")
print(decoded)
song.close()