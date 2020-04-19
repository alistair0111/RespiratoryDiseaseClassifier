from os import listdir

import librosa
import numpy as np
import h5py

from tensorflow.keras.models import load_model


def extract_features(file_name):
    try:
            max_pad_len = 862
            audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast', duration=20) 
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            pad_width = max_pad_len - mfccs.shape[1]
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
    except Exception as e:
            print("Error encountered while parsing file: ", file_name)
            return None
    return mfccs


def prediction(file_name):
    path = "D:\MINI PROJECT\respiratory-sound-database\Respiratory_Sound_Database\Respiratory_Sound_Database\audio_and_text_files\{}".format(file_name)
    data = extract_features(path)
    model=load_model("mymodel2_268.h5",compile=False)
    np.set_printoptions(suppress=True)
    data = data.reshape([1,40,862,1])
    pred = model.predict([data])
    c_names = ['Bronchiectasis', 'Bronchiolitis', 'COPD', 'Healthy', 'Pneumonia', 'URTI']
    index = pred.index(max(pred))
    return c_names[index]

print(prediction('107_2b3_Ll_mc_AKGC417L.wav'))