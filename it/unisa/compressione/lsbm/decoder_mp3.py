import sys
# Use wave package (native to Python) for reading the received audio file
import wave
# Librerie
from bitarray import bitarray # struttura dati bitarray
import fileinput # read from file
from pydub import AudioSegment # lettura file mp3
import sys #Exit

PATH_PROJ = sys.path[1]
#PATH_INPUT_FILE_AUDIO1_MODIFIED = PATH_PROJ + "/file_audio/encoded/audio2_lsbm.wav"
PATH_INPUT_FILE_AUDIO1_MODIFIED = PATH_PROJ + "/it/unisa/compressione/lsbm/original_modified.mp3"

# FUNCTIONS
def most_significant_bit(frame):
    var_bin = format(frame,'#018b')
    if(var_bin[0]=='-'):
        var_bin = format(frame,'#19b')
    return var_bin[3:5] if var_bin[0]=='-' else var_bin[2:4]

def bit_selection_extracted(sample):

    msb = most_significant_bit(sample)
    sample_list = list(format(sample,'#018b'))
    if(sample_list[0]=='-'):
        sample_list = list(format(sample,'#019b'))
    return sample_list[len(sample_list) - 3]

    if(msb == "00"):
        return sample_list[len(sample_list) - 3]
    elif(msb  == "01"):
        return sample_list[len(sample_list) - 2]
    elif(msb  == "10" or msb  == "11"):
        return sample_list[len(sample_list) - 1]


audio_stego = AudioSegment.from_mp3(PATH_INPUT_FILE_AUDIO1_MODIFIED)

extracted = list()
# Extract the LSB of each byte
samples = audio_stego.get_array_of_samples()
for i in range(0,len(samples)):
    extracted.append(bit_selection_extracted(samples[i]))

# Convert byte array back to string
string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# Cut off at the filler characters
decoded = string.split("€")[0]

# Print the extracted text
print("Sucessfully decoded:")
print(decoded)
