# -*- coding: utf-8 -*-
"""Tu.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jC2n0ei-cWEfm2CXO2nwzt0qO72H_Fc8
"""

import argparse
import glob
import librosa
import torchaudio
from speechbrain.pretrained import EncoderClassifier
import numpy as np
from scipy.io import wavfile
import numpy as np
from scipy.io.wavfile import write
import torch
import os
from scipy import linalg, mat, dot
import pandas as pd
import seaborn as sns
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--wav_dir', type=str,
                        help='wav_dir')
parser.add_argument('-f', '--file_csv', type=str,
                        help='file_csv')
args = parser.parse_args()
print("Load wav from " + str(args.wav_dir))

try:
  x = glob.glob(str(args.wav_dir + "/*.wav"))
except:
  print("No dir name" + str(args.wav_dir))
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

#define cospair function

def cos_pair(a,b):
  return dot(a,b.T)/linalg.norm(a)/linalg.norm(b)

#min_mat save min cosine pair of 1 wav; min_path save path of wav
min_mat = []
min_path = []
for _ in range(len(x)):
  frequency, signal = wavfile.read(x[_])
  slice_length = 1.2 # in seconds
  overlap = 0.2 # in seconds
  slices = np.arange(0, len(signal)/frequency, slice_length-overlap, dtype=np.int)
  i = 0
  audio = []
  matrix_audio = []
  for start, end in zip(slices[:-1], slices[1:]):
      i = i + 1
      start_audio = start * frequency
      end_audio = (end + overlap)* frequency
      audio_slice = signal[int(start_audio): int(end_audio)]
      audio_slice = audio_slice.reshape(1,-1)
      audio_slice = torch.tensor(audio_slice)
      #Encode a audio_slice
      audio_slice = classifier.encode_batch(audio_slice)
      audio_slice = audio_slice.squeeze()
      audio.append(audio_slice)
  #matrix cosine of a audio
  matrix_audio = [ [0]*(len(audio)) for i in range(len(audio))]
  for i in range(len(audio)):
    for j in range(len(audio)):
      matrix_audio[i][j]=(cos_pair(audio[i], audio[j]))
  mymin = min([min(r) for r in matrix_audio])
  #append mincosine and path
  min_mat.append(mymin)
  min_path.append(x[_])
  if (_%100==0):
    print(str(_))
    print("____________________________________________________________________________________")
    # print(matrix_audio)
    print(str(x[_]))
    print("Min matrix:" + str(mymin))

#   import numpy as np
#   import matplotlib.pyplot as plt


#   fig = plt.figure(figsize=(6, 3.2))

#   ax = fig.add_subplot(111)
#   ax.set_title('color')
#   plt.imshow(matrix_audio)
#   ax.set_aspect('equal')

#   cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
#   cax.get_xaxis().set_visible(False)
#   cax.get_yaxis().set_visible(False)
#   cax.patch.set_alpha(0)
#   cax.set_frame_on(False)
#   plt.colorbar(orientation='vertical')
#   plt.show()



data = []
for i in range(len(min_mat)):
    data.append([min_mat[i],min_path[i]])
print(data)


data = pd.DataFrame([min_mat,min_path]) #Each list would be added as a row
data = data.transpose() #To Transpose and make each rows as columns
data.columns=['MinCos','Path'] #Rename the columns
print("Save csv to " + str(args.file_csv))
my_file = Path(args.file_csv)
try:
  data.to_csv(args.file_csv)
except:
  print("No dir name " + str(args.file_csv))

  

