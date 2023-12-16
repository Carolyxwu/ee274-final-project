from bil.m import rigS
import numpy as np
import pandas as pd
import argparse
import os
import matplotlib.pyplot as plt
import h5py
import gzip
import sys
from pathlib import Path
import skvideo.io

parser = argparse.ArgumentParser()
parser.add_argument("runID", type=str, help="run ID", default=None)
args = parser.parse_args()

runID = args.runID
# runID = os.environ['RUNID']
derivpath = os.environ['DM_D']


runID_data = rigS.study(runID)
print('the number of trials in runID_data is',len(runID_data))
c_quality_list = [0, 10, 20, 30, 40, 50]

icr_matrix = np.zeros((len(runID_data)-2, len(c_quality_list)))
d_matrix = np.zeros((len(runID_data)-2, len(c_quality_list)))
for idx in range(len(runID_data)-2):
    if not idx%50:
        # raster = runID_data[idx][0:len(runID_data[idx])].raster()
        # M1_raster=raster.iloc[:, :96]
        csv_path = os.path.join(derivpath,runID[0],'h5','h5_'+runID,'neural','M1_raster_%04d.csv'%idx) 
        # os.path.join(derivpath,runID[0],'h5','h5_'+runID,'neural','M1_raster_%04d.csv'%idx)
        # "/scratch/data_m/deriv/U/h5/h5_U201209_01/neural/M1_raster_%04d.csv"%idx 
        # M1_raster.to_csv(csv_path) 
        df = pd.read_csv(csv_path)
        numpy_array = df.to_numpy()
        numpy_array = numpy_array[:,1:]
        for c_idx, c_quality in enumerate(c_quality_list):
            mp4_path = os.path.join(derivpath,runID[0],'h5','h5_'+runID,'neural','M1_raster_%04d_%02d.mp4'%(idx,c_quality)) 
            writer = skvideo.io.FFmpegWriter(mp4_path, outputdict={'-vcodec': 'libx264', '-crf': str(c_quality)})
            for t in range(numpy_array.shape[0]):
                data = numpy_array[t,:]
                indices_to_insert = [0, 8, 87, 96]
                values_to_insert = np.array([0, 0, 0, 0])
                frame = np.insert(data, indices_to_insert, values_to_insert)
                frame = frame.reshape(10,10)
                frame = (frame*255).astype(np.uint8)
                writer.writeFrame(frame)
            writer.close()
            data = Path(csv_path).read_bytes()
            compressed=Path(mp4_path).read_bytes()
            rate = len(compressed)/len(data)
            icr_matrix[idx,c_idx] = rate

            videogen = skvideo.io.vreader(mp4_path)
            distortion = 0
            for t, frame in enumerate(videogen):
                data = numpy_array[t,:]
                indices_to_insert = [0, 8, 87, 96]
                values_to_insert = np.array([0, 0, 0, 0])
                o_frame = np.insert(data, indices_to_insert, values_to_insert)
                o_frame = o_frame.reshape(10,10).astype(np.uint8)
                frame = np.round(frame/255).astype(np.uint8)
                frame = frame[:,:,0]
                distortion += np.sum(o_frame != frame)

            distortion = distortion/(len(runID_data)-2)/96.0
            d_matrix[idx,c_idx] = distortion
 
np.save(runID+"_icr_h264_rates.npy",icr_matrix) 
np.save(runID+"_distortion_h264_rates.npy",d_matrix) 