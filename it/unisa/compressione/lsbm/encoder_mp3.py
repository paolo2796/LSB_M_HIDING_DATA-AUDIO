import array
import numpy as np
import struct
from pydub import AudioSegment
import sys
# CONSTANTS DEF
PATH_PROJ = sys.path[1]
PATH_INPUT_FILE_AUDIO2 = PATH_PROJ + "/file_audio/audio2.mp3"

original_song = AudioSegment.from_mp3(PATH_INPUT_FILE_AUDIO2)



# get raw data from the wav file
samples = original_song.get_array_of_samples()
# iterate over the data
for i in range (0, len(samples)):
    # convert to 16bit (?)
    sixteen = struct.unpack('H', struct.pack('h', samples[i]))
    samples[i] = 136


new_sound = original_song._spawn(samples)
new_sound.export(PATH_PROJ + "/file_audio/encoded/audio1_lsbm.mp3", format="wav")