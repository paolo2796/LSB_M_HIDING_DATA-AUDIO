# Librerie
from bitarray import bitarray # struttura dati bitarray
import fileinput # read from file
from pydub import AudioSegment # lettura file mp3
import sys #Exit
import array
import numpy as np

messaggio = input("Inserisci il messaggio da codificare (Sternocleidomastoideo): ") or "Sternocleidomastoideo"
messaggio_bitarray = bitarray() # Inizializzo array di bit vuoto
messaggio_bitarray.fromstring(messaggio) # Popolo array di bit con stringa in input

# Init
sample_da_nascondere = len(messaggio_bitarray) # grandezza sequenza

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


file_path = input("Inserisci il nome del file MP3 (sample.mp3): ") or "sample.mp3"
# Start processing della canzone
fake_song = AudioSegment.empty();
original_song = AudioSegment.from_mp3(file_path)

caratteri_rimanenti = int((len(original_song.get_array_of_samples()) -  len(messaggio_bitarray))/8)
messaggio = messaggio + (caratteri_rimanenti *'#')
messaggio_bitarray = bitarray()
messaggio_bitarray.fromstring((messaggio))
samples = original_song.get_array_of_samples()
#for i in range(0,len(samples)):
        #samples[i] = bit_selection_replaced(samples[i],int(messaggio_bitarray[i]))


print((original_song.get_array_of_samples()[23000000]))
print((original_song.get_array_of_samples()[23000001]))
print((original_song.get_array_of_samples()[23000002]))

# Example operation on audio data
#shifted_samples = np.left_shift(samples, 1)

# now you have to convert back to an array.array
#shifted_samples_array = array.array(original_song.array_type, shifted_samples)


# Export original songsample_width=2, frame_rate=44100, channels=1
original_song.export("original_modified.mp3",format="mp3", codec='mp3', bitrate="320k")
new_sound = AudioSegment.from_mp3("original_modified.mp3")
print(new_sound.get_array_of_samples()[23000000])
print(new_sound.get_array_of_samples()[23000001])
print(new_sound.get_array_of_samples()[23000002])


