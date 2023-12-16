from bil.m import rigS
import numpy as np
import pandas as pd
import argparse
import os
import matplotlib.pyplot as plt
import h5py
import gzip
from pathlib import Path
import skvideo.io
from scipy.io import loadmat

parser = argparse.ArgumentParser()
parser.add_argument("runID", type=str, help="run ID", default=None)
args = parser.parse_args()

runID = args.runID
data_path = os.path.join('/scratch/AblationData',runID,'profile.mat') 
# print(data_path)
variable_names = ['profile_all']
data = loadmat(data_path, variable_names=variable_names)
data = data['profile_all']
min_val = np.min(data)
max_val = np.max(data)
scaled_array = 255 * (data - min_val) / (max_val - min_val)
scaled_array = scaled_array.astype(np.uint8)

l = data.shape[0]
sqrt_l = int(np.sqrt(l))
rows = int(np.floor(np.sqrt(l)))
cols = int(np.ceil(l/rows))

mp4_path = os.path.join('/scratch/AblationData',runID,'profile.mp4') 
writer = skvideo.io.FFmpegWriter(mp4_path, outputdict={'-vcodec': 'libx264'})
for t in range(data.shape[1]):
    array = scaled_array[:,t]
    reshaped_array = np.zeros(rows*cols, dtype=np.uint8)
    reshaped_array[:l] = array
    frame = reshaped_array.reshape(rows,cols)
    writer.writeFrame(frame)
writer.close()
data=data.tobytes()
compressed=Path(mp4_path).read_bytes()
rate = len(compressed)/len(data)
np.save(runID+"_compression_rate_h264_n.npy",rate) 