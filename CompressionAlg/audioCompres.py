from pydub import AudioSegment
import soundfile as sf
import numpy as np
# import matplotlib.pyplot as plt

mp3File = input("Provide an mp3 file to be compressed:")
tempList = mp3File.split(".")
wavFile = tempList[0] + ".wav"

# Convert .wav to .mp3
audio = AudioSegment.from_mp3(mp3File)
audio.export(wavFile, format="wav")

# Retrieve the data from the wav file
data, samplerate = sf.read(wavFile)

n = len(data) #the length of the arrays contained in data
Fs = samplerate
ch1 = np.array([data[i][0] for i in range(n)]) #channel 1
ch2 = np.array([data[i][1] for i in range(n)]) #channel 2

ch1_Fourier = np.fft.fft(ch1) #performing Fast Fourier Transform
abs_ch1_Fourier = np.absolute(ch1_Fourier[:n//2]) #the spectrum

# plt.plot(np.linspace(0, Fs / 2, n//2), abs_ch1_Fourier)
# plt.ylabel('Spectrum')
# plt.xlabel('$f$ (Hz)')
# plt.show()

eps = 1e-5 #epsilon, small

# Boolean array where each value indicates whether we keep the corresponding frequency
frequenciesToRemove = (1 - eps) * np.sum(abs_ch1_Fourier) < np.cumsum(abs_ch1_Fourier) #The frequency for which we cut the spectrum
f0 = (len(frequenciesToRemove) - np.sum(frequenciesToRemove) )* (Fs / 2) / (n / 2)

# print("f0 : {} Hz".format(int(f0)))

# Displaying the spectrum with a vertical line for f0
# plt.axvline(f0, color='r')
# plt.plot(np.linspace(0, Fs / 2, n//2), abs_ch1_Fourier)
# plt.ylabel('Spectrum')
# plt.xlabel('$f$ (Hz)')
# plt.show()

wavCompressedFile = tempList[0] + "_compressed.wav"
mp3CompressedFile = tempList[0] + "_compressed.mp3"

D = int(Fs / f0)

# print("Downsampling factor : {}".format(D))
new_data = data[::D, :] #getting the downsampled data
# Writing the new data into a wav file
sf.write(wavCompressedFile, new_data, int(Fs / D), 'PCM_16') # Converting back to mp3
audioCompressed = AudioSegment.from_wav(wavCompressedFile)
audioCompressed.export(mp3CompressedFile, format="mp3")
