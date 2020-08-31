# Importing General Packages
import numpy as np
import os
    
## Importing Visualization Pakcages
import seaborn
import matplotlib.pyplot as plt
import IPython.display as ipd
import skimage                # Saving the spectrogram image
import skimage.io
import pylab

## Importing Audio Processing Pakcages
import librosa, librosa.display

def scale_minmax(X, Xmin=0.0, Xmax=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std  * (Xmax - Xmin) + Xmin
    return X_scaled

def AMT(filename_):
    # View Spectrogram of the Audio File.. 

    # Define Variable Q-Transform Parameters for Audio Signals Processing
    fs = 44100  # Sampling frequency 
    hop_length=512  # number of samples between successive VQT columns
    fmin=None # Minimum frequency. Defaults to C1 ~= 32.70 Hz
    n_bins=84 # Number of frequency bins
    gamma=20 # Bandwidth offset for determining filter lengths (If Gamma=0 then => CQT computation)
    bins_per_octave=12 # Number of frequency bins per octave
    tuning=0.0 # Tuning offset in fractions of a bin(None, tuning will be automatically estimated from the signal)
    filter_scale=1 # Filter scale factor. Small values (<1) use shorter windows for improved time resolution.
    norm=1 # Type of norm to use for basis function normalization
    sparsity=0.01 # Sparsify the VQT basis by discarding up to sparsity fraction of the energy
    window='hann' # Using Hann Window 
    scale=True # Scale the VQT response by square-root the length of each channel’s filter
    pad_mode='reflect'  # Padding mode for centered frame analysis
    res_type=None # The resampling mode for recursive downsampling 
    dtype=None # The dtype of the output array. By default, this is inferred to match the numerical precision of the input signal

    # Audio Processing
    ## Loading the Audio
    ### Path Configuration 
    path = os.getcwd() + '/' + filename_
    filename = "{}".format(filename_)
    x, fs = librosa.load(filename, sr=None, mono=True, duration=12)
    
    ###### Playback audio file
    # ipd.Audio(x, rate=fs)
    
    # VQT Computation 
    V = librosa.vqt(x,sr= fs,hop_length=hop_length,fmin=fmin,n_bins=n_bins,gamma=20,bins_per_octave=bins_per_octave,tuning=tuning,filter_scale=filter_scale,norm=norm ,sparsity=0.01 ,window='hann',scale=scale,pad_mode=pad_mode,res_type=res_type,dtype=dtype)
    
    ## Display the VQT spectrogram
    #logV = librosa.amplitude_to_db(np.abs(V))
    #plt.figure(figsize=(15, 5))
    #librosa.display.specshow(logV, sr=fs, x_axis='time', y_axis='cqt_note', fmin=fmin, cmap='coolwarm')
    
    ### Conversion into the Mel-Scale to display and save Mel-spectrogram
    n_mels = 128          # Bins 
    V_mel = np.abs(V)  # Mapping Magnitude spectrogram to the Mel Scale
    mels = librosa.feature.melspectrogram(S=V_mel,sr=fs,n_mels=n_mels,n_fft=hop_length*2, hop_length=hop_length)  
    Smels = librosa.display.specshow(mels, sr=fs, x_axis='time', y_axis='mel', fmin=fmin, fmax=8000, cmap="coolwarm")
    
    # CONVERSION 
    mels = np.log(mels + 1e-9) # add small number to avoid log(0)
    out = 'out.png'
    
    # min-max scale to fit inside 8-bit range
    img = scale_minmax(mels, 0, 255).astype(np.uint8)
    img = np.flip(img, axis=0) # put low frequencies at the bottom in image
    img = 255-img # invert. make black==more energy

    # save as PNG
    skimage.io.imsave(out, img)