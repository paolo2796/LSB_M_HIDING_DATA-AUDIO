import sys
# Use wave package (native to Python) for reading the received audio file
import wave

PATH_PROJ = sys.path[1]
PATH_INPUT_FILE_AUDIO1_MODIFIED = PATH_PROJ + "/file_audio/audio1_lsbm.wav"

song = wave.open(PATH_INPUT_FILE_AUDIO1_MODIFIED, mode='rb')
# Convert audio to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# Extract the LSB of each byte
extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
# Convert byte array back to string
string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# Cut off at the filler characters
decoded = string.split("#")[0]

# Print the extracted text
print("Sucessfully decoded: "+decoded)
song.close()