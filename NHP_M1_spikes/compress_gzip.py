from bil.m import rigS
import numpy as np
import pandas as pd
import argparse
import os
import matplotlib.pyplot as plt
import h5py
import gzip
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("runID", type=str, help="run ID", default=None)
args = parser.parse_args()

runID = args.runID
# runID = os.environ['RUNID']
derivpath = os.environ['DM_D']


runID_data = rigS.study(runID)
print('the number of trials in runID_data is',len(runID_data))
compression_rate = []
for idx in range(len(runID_data)-2):
    # raster = runID_data[idx][0:len(runID_data[idx])].raster()
    # M1_raster=raster.iloc[:, :96]
    csv_path = os.path.join(derivpath,runID[0],'h5','h5_'+runID,'neural','M1_raster_%04d.csv'%idx) 
    # os.path.join(derivpath,runID[0],'h5','h5_'+runID,'neural','M1_raster_%04d.csv'%idx)
    # "/scratch/data_m/deriv/U/h5/h5_U201209_01/neural/M1_raster_%04d.csv"%idx 
    # M1_raster.to_csv(csv_path) 
    data = Path(csv_path).read_bytes()
    compressed=gzip.compress(data)
    rate = len(compressed)/len(data)
    compression_rate.append(rate)

cr=np.array(compression_rate)
np.save(runID+"compression_rate_gzip.npy",cr) 