#!/usr/bin/env python
# coding: utf-8

# In[1]:


# general packages
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import math
from tqdm import tqdm
import random
from scipy import stats

# packages to read data
import scipy.io
from pathlib import Path

# packages for compression
import zstd
import gzip
import skvideo.io


# In[4]:


## LOAD DATA
# neuropixel data from five mice
# from Masuda et al., 2023: https://figshare.com/articles/dataset/Ketamine_evoked_disruption_of_entorhinal_and_hippocampal_spatial_maps/22696309
sub1mat = "../G4_190624_baseline1+controlinjx1+ketamine1_fr+corr.mat"
sub2mat = "../G1_190818_baseline1+controlinjx1+ketamine1_fr+corr.mat"
sub3mat = "../G5_190705_baseline1+controlinjx1+ketamine1_fr+corr.mat"
sub4mat = "../HCNd1_190812_baseline1+controlinjx1+ketamine1_fr+corr.mat"
sub5mat = "../HCNe2_190912_baseline1+controlinjx1+ketamine1_fr+corr.mat"

sub1 = scipy.io.loadmat(sub1mat)
sub2 = scipy.io.loadmat(sub2mat)
sub3 = scipy.io.loadmat(sub3mat)
sub4 = scipy.io.loadmat(sub4mat)
sub5 = scipy.io.loadmat(sub5mat)

data = [sub1, sub2, sub3, sub4, sub5]


# In[5]:


## LOSSLESS COMPRESSION RATIOS
# get compression ratio for trials

gzip_icr = np.zeros((5,300)) 
zstd_icr = np.zeros((5,300))
count = -1

for file in data:
    d = file['all_fr']
    count = count + 1

    for i in tqdm(range(d.shape[1])):
        temp = d[:,i,:]
        temp = temp.copy(order='C')
        
        z_compressed = zstd.compress(temp)
        z_compressed_size = len(z_compressed)
        
        g_compressed = gzip.compress(temp)
        g_compressed_size = len(g_compressed)
        
        raw_size = temp.size * temp.itemsize
        
        curr_zstd_icr = z_compressed_size / raw_size
        
        curr_gzip_icr = g_compressed_size / raw_size

        zstd_icr[count,i] = curr_zstd_icr 
        gzip_icr[count,i] = curr_gzip_icr


# In[6]:


## FIGURES
fig, ax = plt.subplots(nrows=2, ncols=1,figsize = (10,10))

z = ax[0].vlines(100,0,0.5,'k',label='ketamine injection');
ax[0].legend(('ketamine injection',));
ax[1].vlines(100,0,0.5,'k',label='ketamine time');

ax[0].plot(gzip_icr.T);
ax[0].set_ylabel('GZIP ICR');
ax[0].set_title('Lossless ICR and Epilepsy Data');

ax[1].plot(zstd_icr.T);
ax[1].set_ylabel('ZSTD ICR')
ax[1].set_xlabel('trial')


# In[7]:


## FIGURES
# zoom in to see more detail

fig, ax = plt.subplots(nrows=2, ncols=1,figsize = (5,10))

z = ax[0].vlines(50,0,0.5,'k',label='ketamine injection');
ax[0].legend(('ketamine injection',));
ax[1].vlines(50,0,0.5,'k',label='ketamine time');

ax[0].plot(gzip_icr[:,50:150].T);
ax[0].set_ylabel('GZIP ICR');
ax[0].set_title('Lossless ICR and Epilepsy Data');

ax[1].plot(zstd_icr[:,50:150].T);
ax[1].set_ylabel('ZSTD ICR')
ax[1].set_xlabel('trial')


# In[8]:


## FIGURES
# bar chart of average 
subjects = ("Subject 1", "Subject 2", "Subject 3","Subject 4","Subject 5")
to_plot = {
    'Ketamine': np.mean(gzip_icr[:,100:-1], axis = 1),
    'Control': np.mean(gzip_icr[:,0:100], axis = 1),
}

x = np.arange(len(subjects))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in to_plot.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    multiplier += 1

ax.set_ylabel('GZIP ICR')
ax.set_title('GZIP Lossless Compression')
ax.set_xticks(x + width, subjects)
ax.legend(loc='upper left', ncols=2)

plt.show()


# In[9]:


## FIGURES
# bar chart of average 
subjects = ("Subject 1", "Subject 2", "Subject 3","Subject 4","Subject 5")
to_plot = {
    'Ketamine': np.mean(zstd_icr[:,100:-1], axis = 1),
    'Control': np.mean(zstd_icr[:,0:100], axis = 1),
}

x = np.arange(len(subjects))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in to_plot.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    multiplier += 1

ax.set_ylabel('ZSTD ICR')
ax.set_title('ZSTD Lossless Compression')
ax.set_xticks(x + width, subjects)
ax.legend(loc='upper left', ncols=2)

plt.show()


# In[10]:


## LOSSY COMPRESSION RATIOS
count = 1
crf = 22
conrates =[]
ketrates= []

#control
for file in data:
    da = file['all_fr']
    
    # sort according to spike depth
    depth = file['spike_depth']
    ind = np.argsort(depth.flatten())
    d = np.take(da, ind, axis=0)
    
    cells = d.shape[0]
    time = d.shape[2]
    
    filename = "outputcont" + str(count) + ".mp4"
    count = count + 1
    
    writer = skvideo.io.FFmpegWriter(filename, outputdict={'-vcodec': 'libx264','-crf': str(crf),})
    for t in range(100):
        dat = d[:,t,:].reshape((cells, time))
        img = dat.astype(np.uint8)
        writer.writeFrame(img)
    writer.close()
    
    x=d[:,0:100,:].tobytes()
    compressed=Path(filename).read_bytes()
    rate = len(compressed)/len(x)

    conrates.append(rate)
    
for file in data:
    da = file['all_fr']
    
    # sort according to spike depth
    depth = file['spike_depth']
    ind = np.argsort(depth.flatten())
    d = np.take(da, ind, axis=0)
    
    cells = d.shape[0]
    time = d.shape[2]
    
    filename = "outputket" + str(count) + ".mp4"
    count = count + 1
    
    writer = skvideo.io.FFmpegWriter(filename, outputdict={'-vcodec': 'libx264','-crf': str(crf),})
    for t in range(100):
        dat = d[:,t+100,:].reshape((cells, time))
        img = dat.astype(np.uint8)
        writer.writeFrame(img)
    writer.close() 
    
    x=d[:,100:-1,:].tobytes()
    compressed=Path(filename).read_bytes()
    rate = len(compressed)/len(x)
    
    ketrates.append(rate)


# In[11]:


## FIGURES
# lossy compression
subjects = ("Subject 1", "Subject 2", "Subject 3","Subject 4","Subject 5")
to_plot = {
    'Ketamine': ketrates,
    'Control': conrates,
}

x = np.arange(len(subjects))  
width = 0.25
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in to_plot.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    multiplier += 1

ax.set_ylabel('H264 ICR')
ax.set_title('Lossy Compression')
ax.set_xticks(x + width, subjects)
ax.legend(loc='upper left', ncols=2)

plt.show()


# In[12]:


## STATISTICAL TESTING
# lossless, gzip:
k_gzip = np.mean(gzip_icr[:,100:-1], axis = 1)
c_gzip = np.mean(gzip_icr[:,0:100], axis = 1)
s_gzip,p_gzip = stats.ttest_ind(a=k_gzip, b=c_gzip, equal_var=False)
print("GZIP P-value: ", p_gzip)

# lossless, zstd:
k_zstd = np.mean(zstd_icr[:,100:-1], axis = 1)
c_zstd = np.mean(zstd_icr[:,0:100], axis = 1)
s_zstd,p_zstd = stats.ttest_ind(a=k_zstd, b=c_zstd, equal_var=False)
print("ZSTD P-value: ", p_zstd)

# lossy, h264
s_h264,p_h264 = stats.ttest_ind(a=ketrates, b=conrates, equal_var=False)
print("H264 P-value: ", p_h264)


# In[16]:


## SWEEP OVER DIFFERENT CRF VALUES
for crf in tqdm(range(51)):
    count = 1
    conrates =[]
    ketrates= []

    #control
    for file in data:
        da = file['all_fr']

        # sort according to spike depth
        depth = file['spike_depth']
        ind = np.argsort(depth.flatten())
        d = np.take(da, ind, axis=0)

        cells = d.shape[0]
        time = d.shape[2]

        filename = "outputcont" + str(count) + ".mp4"
        count = count + 1

        writer = skvideo.io.FFmpegWriter(filename, outputdict={'-vcodec': 'libx264','-crf': str(crf),})
        for t in range(100):
            dat = d[:,t,:].reshape((cells, time))
            img = dat.astype(np.uint8)
            writer.writeFrame(img)
        writer.close()

        x=d[:,0:100,:].tobytes()
        compressed=Path(filename).read_bytes()
        rate = len(compressed)/len(x)

        conrates.append(rate)

    for file in data:
        da = file['all_fr']

        # sort according to spike depth
        depth = file['spike_depth']
        ind = np.argsort(depth.flatten())
        d = np.take(da, ind, axis=0)

        cells = d.shape[0]
        time = d.shape[2]

        filename = "outputket" + str(count) + ".mp4"
        count = count + 1

        writer = skvideo.io.FFmpegWriter(filename, outputdict={'-vcodec': 'libx264','-crf': str(crf),})
        for t in range(100):
            dat = d[:,t+100,:].reshape((cells, time))
            img = dat.astype(np.uint8)
            writer.writeFrame(img)
        writer.close() 

        x=d[:,100:-1,:].tobytes()
        compressed=Path(filename).read_bytes()
        rate = len(compressed)/len(x)

        ketrates.append(rate)
        
    s,p = stats.ttest_ind(a=ketrates, b=conrates, equal_var=False)
    print("At CRF value ",crf," p-value is: ", p)

