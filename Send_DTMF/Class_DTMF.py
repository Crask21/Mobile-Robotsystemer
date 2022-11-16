
import numpy as np
import matplotlib.pyplot as plt
#import sounddevice as sd
import pygame 
import time
from random import randrange
import threading



dtmf_freq = [[1209,697], # 0
                    [1336,697],  # 1
                    [1477,697],  # 2
                    [1633,697],  # 3
                    [1209,770],  # 4
                    [1336,770],  # 5
                    [1477,770],  # 6
                    [1633,770],  # 7
                    [1209,852],  # 8
                    [1336,852],  # 9
                    [1477,852],  # A
                    [1633,852],  # B
                    [1209,941],  # C
                    [1336,941],  # D
                    [1477,941],  # E
                    [1633,941]]  # F



class DTMF:

    def __init__(data, fs, amplitude, p_fade, baud, sound_media = 'PyGame'):

        # DTMF setup
        data.fs = fs
        data.amplitude = amplitude
        data.p_fade = p_fade

        # User setting variables
        data.baud = baud
        data.duration = 1/baud
        data.sound_media = sound_media

        # Initialize sound array
        data.soundwave = np.array([])
        data.FFT = 0

        # Initialize DMTF tone list
        data.dtmf = []
        data.DTMF_init()



# Send package of hexi decimals
    def send_package(data, package):

        
        data.soundwave = np.arange(0,1)

        # Convert package into sound array
        for i in package:
            data.soundwave = [*data.soundwave, *data.dtmf[i]]

            # Delete end spike
            data.soundwave[-1] = 0

        

        # Play through PyGame
        if data.sound_media == 'PyGame':
            data.play_PyGame(data.soundwave)
        
        # Play through Sounddevice
        elif data.sound_media == 'SD':
            data.play_SD(data.soundwave)
           

# Plot the package as DTMF tones
    def plot_last_package(data):

        package_size = round(len(data.soundwave)/data.fs/data.duration)

        time = np.arange(0, data.duration * package_size, 1/data.fs)
        data.soundwave = np.delete(data.soundwave,-1)

        plt.plot(time,data.soundwave,'r--')
        plt.ylabel('some numbers')
        plt.show()


    def plot_fft(data):

        package_size = round(len(data.FFT)/data.fs/data.duration)

        time = np.arange(0, data.duration * package_size, 1/data.fs)
        #data.FFT = np.delete(data.FFT,-1)

        plt.plot(data.FFT,'r--')
        plt.ylabel('some numbers')
        plt.show()
    


        
# Make a DTMF tone
    def makeDTMF(data,amplitude,dur,freq1,freq2,f_sample, percentage_fade):
            
            # Turn frequencies into functions 
            time = np.arange(0, dur, 1/f_sample)
            xi = amplitude * np.sin(2*np.pi*freq2*time) + amplitude * np.sin(2*np.pi*freq1*time)   
            
            # Fadeeeeeee #
            number_of_faded_points = int(dur * percentage_fade * f_sample)
            fade = np.linspace(0,1,num=number_of_faded_points)
            fade_end = np.linspace(1,0,num=number_of_faded_points)

            data.FFT = np.fft.fft(xi)

            for j in np.arange(number_of_faded_points):
                xi[j] = xi[j] * fade[j]

            for j in np.arange(-1*number_of_faded_points,-1):    
                xi[j] = xi[j] * fade_end[j]    
            # Fadeeeeeee #
            

    
            return xi

# Setup DTMF tones in list
    def DTMF_init(data):


        # DTMF frequencies
        dtmf_freq = [[1209,697], # 0
                    [1336,697],  # 1
                    [1477,697],  # 2
                    [1633,697],  # 3
                    [1209,770],  # 4
                    [1336,770],  # 5
                    [1477,770],  # 6
                    [1633,770],  # 7
                    [1209,852],  # 8
                    [1336,852],  # 9
                    [1477,852],  # A
                    [1633,852],  # B
                    [1209,941],  # C
                    [1336,941],  # D
                    [1477,941],  # E
                    [1633,941]]  # F


        for i in np.arange(len(dtmf_freq)):
            data.dtmf.append(data.makeDTMF(data.amplitude, data.duration, dtmf_freq[i][0], dtmf_freq[i][1], data.fs, data.p_fade))

# Play the sound through either PyGame or Sounddevice
    def play_PyGame(data, soundwave):
        # Initialize PyGame mixer
        pygame.mixer.init(frequency=data.fs, size=-16, channels=1)

        # Convert list to numpy array
        buffer = np.array(soundwave,dtype=np.int16)

        # (Fixes and error) dublicate sound channel or something (it makes it work)
        buffer = np.repeat(buffer.reshape(len(soundwave), 1), 2, axis = 1)

        # Create sound object
        sound = pygame.sndarray.make_sound(buffer)

        # Play the sound
        sound.play()

        # Delay for the duration of the sound
        pygame.time.wait(int(sound.get_length() * 1000)) 
    #def play_SD(data, soundwave):
    #    wav_wave = np.array(soundwave, dtype=np.int16)
    #    sd.play(wav_wave, blocking=True)






# Synchroniazation
def synchroniazation(num):
    sync = []
    for i in range(num):
        sync.append(0xA)
        sync.append(0xB)
    sync.append(0xC)
    sync.append(0xC)
    return sync



# Random package
def rand_pack(num):
    size = 16
    random_data = []
    for i in range(num):
        random_data.append(randrange(size))
    return random_data
