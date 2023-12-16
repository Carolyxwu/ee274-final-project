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
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

def rgba_to_grayscale(rgba):
    r, g, b, a = rgba
    gray_value = 0.299 * r + 0.587 * g + 0.114 * b
    return int(gray_value * 255)

parser = argparse.ArgumentParser()
parser.add_argument("runID", type=str, help="run ID", default=None)
args = parser.parse_args()

runID = args.runID
data_path = os.path.join('/scratch/AblationData',runID,'profile.mat') 
# print(data_path)
variable_names = ['profile_all','x','y','z']
data = loadmat(data_path, variable_names=variable_names)

postion = np.hstack((data['x'],data['y'],data['z']))
projection_matrix = np.array([
    [1, 0, 0],
    [0, 1, 0]
])
points_2d = postion.dot(projection_matrix.T)

data = data['profile_all']
min_val = np.min(data)
max_val = np.max(data)
scaled_array = 255 * (data - min_val) / (max_val - min_val)
scaled_array = scaled_array.astype(np.uint8)

# l = data.shape[0]
# sqrt_l = int(np.sqrt(l))
# rows = int(np.floor(np.sqrt(l)))
# cols = int(np.ceil(l/rows))

mp4_path = runID+'_profile.mp4'
writer = skvideo.io.FFmpegWriter(mp4_path, outputdict={'-vcodec': 'libx264'})
for t in range(data.shape[1]):
    array = scaled_array[:,t]
    # plt.scatter(points_2d[:, 0], points_2d[:, 1], c=array, cmap='gray', edgecolors='none')
    
    fig = Figure()
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)
    ax.scatter(points_2d[:, 0], points_2d[:, 1], c=array, cmap='gray', edgecolors='none')

    # 不显示坐标轴
    ax.axis('off')

    # 设置背景为黑色
    # plt.gca().set_facecolor('black')

    canvas.draw()
    buf = canvas.buffer_rgba()

    X = np.asarray(buf)
    plt.close(fig)
    
    frame = (0.299 * X[:,:,0] + 0.587 * X[:,:,1] + 0.114 * X[:,:,2])* 255
    frame = frame.astype(np.uint8)
    writer.writeFrame(frame)
writer.close()
data=data.tobytes()
compressed=Path(mp4_path).read_bytes()
rate = len(compressed)/len(data)
np.save(runID+"_compression_rate_h264.npy",rate) 