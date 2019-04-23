# Module used to smooth audio signal from wav file
# It saves as mp3 file
import librosa.display
import scipy.signal as sig
from pydub import AudioSegment

print("Enter path to the file")
filename = input()
y, sr = librosa.load(filename)
print("Set the L parameter (recomended 41)")
L = int(input())  # Set parameter used to filter(increase L to get more smooth signal)
Filtered_SG = sig.savgol_filter(y, L, 3)  # Filter of Sawicki-Golaya
librosa.output.write_wav("Filtered_SG.wav", Filtered_SG, sr)
wav_audio = AudioSegment.from_file("Filtered_SG.wav", format="wav")
wav_audio.export("Filtered_SG.mp3", format="mp3")


