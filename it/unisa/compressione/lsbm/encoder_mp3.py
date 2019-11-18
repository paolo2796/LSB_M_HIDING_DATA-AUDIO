# Librerie
from bitarray import bitarray # struttura dati bitarray
import fileinput # read from file
from pydub import AudioSegment # lettura file mp3
import sys #Exit
import array
import numpy as np


messaggio = "Hello"
messaggio_bitarray = bitarray() # Inizializzo array di bit vuoto
messaggio_bitarray.fromstring(messaggio) # Popolo array di bit con stringa in input

messaggio_list = list()
for char in messaggio:
    messaggio_list.append(ord(char))


# FUNCTIONS
def most_significant_bit(frame):
    var_bin = format(frame,'#034b')
    if(var_bin[0]=='-'):
        var_bin = format(frame,'#35b')
    return var_bin[3:5] if var_bin[0]=='-' else var_bin[2:4]

def bit_selection_replaced(sample,bit_message):

    msb = most_significant_bit(sample)
    sample_list = list(format(sample,'#034b'))
    if(sample_list[0]=='-'):
        sample_list = list(format(sample,'#035b'))

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



filepath = "sample.mp3"
from pydub import effects
_sound = AudioSegment.from_mp3(filepath)

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)



# 2 bytes == 16 bits
sample_width = 2

# 2 channels, aka stereo
channels = 2

# CD quality: 44.1kHz sample rate
frame_rate = 44100

# one frame of stereo, 16-bit silence (2 bytes per channel, left channel first)
audio_data = b"\0\0\0\0\0\0\0\0"

sound = AudioSegment(audio_data,
                     sample_width=sample_width,
                     frame_rate=frame_rate,
                     channels=channels,
                     )


_samples = sound.get_array_of_samples()
_samples[1]=100
_samples[2]=103

from pydub import AudioSegment
from pydub.utils import mediainfo


original_bitrate = mediainfo(filepath)['bit_rate']
sound = AudioSegment.from_mp3(filepath)
print(sound.get_array_of_samples()[30000])

sound.export("sample.mp3", format="mp3", bitrate=original_bitrate)
sound = AudioSegment.from_mp3("audio_stego.mp3")
print(sound.get_array_of_samples()[30000])
