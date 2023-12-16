# EE274 Final Project: Compression and Neural Data

## Introduction

The complexity of neural data changes as the brain process information during events. 
Compression ratio may be used as a convenient estimator for the complexity of a given signal.
In particular, previous work has shown that compression algorithms may be used to detect seizure from neural array recordings in epileptic patients, historically done with tedious manual inspection [1,2]. 
Previous work has also demonstrated that lossy compression algorithms, such as those used in video compression, perform better than lossless compressors like GZIP [1, 3]. 
However, it remains unknown how these findings generalize to other events and neural data modalities.

In this project, we investigated the use of the inverse compression ratio (ICR) over three distinct datasets spanning three different species and measurement modalities in order to analyze how compression algorithms may be used to track the underlying structure of neural signals recorded with different modalities and tracked behaviors.
We also review previous work on detecting seizure in epilepsy patients.
This project calculates lossless compression ratios using the ZSTD and GZIP lossless compressors, and calculates lossy compression ratios using the H264 lossless compressor.
While our data is not video-based, lossy video compressors (like H264) have been used in the literature due to their ease in use with time-series data [1].

Through our survey of different datasets, we conclude that we are indeed able to track neural events across different measurement modalities and species.
In particular, the inverse compression ratio may be used as a reliable and convenient way to detect events that perturb the temporal structure of neural activity.

## Data

The first dataset explored is a single-unit spike dataset collected from the motor cortex of a rhesus macaque implanted with a 96-electrode Utah array. The data was collected during a radius reaching task over 13 consecutive days. On day 0 denoted in the figures, small electrolytic lesions were performed through the array in the motor cortex. Portions of the NHP stroke data are conditionally available upon request from [the Brain Interfacing Lab](https://bil.stanford.edu/) at Stanford University.

The second dataset contains intracortical probe (NeuroPixel) recordings from the medial entorhinal cortex (MEC) of five different mice performing a navigation task.
In this task, mice traversed a virtual reality linear track.
During the first 100 trials, the mice explored the track without external intervention.
Each mouse was then given a ketamine injection and recorded from for an additional 200 trials. 
This dataset was collected by Dr. Francis Masuda in the Giocomo Lab at Stanford University, and is freely available at this [link](https://giocomolab.weebly.com/data-code-methods.html).


The final dataset is a calcium imaging dataset for ablation experiments in the zebrafish spinal cord. This dataset was collected by the Keller lab at the Janelia Research Campus, and is available at this [link](https://doi.org/10.25378/janelia.7607411.v1).

## Codes

The codes for the NHP dataset analysis can be found at [NHP_M1_spikes](NHP_M1_spikes). Examples of how to run the codes can be found in [main.ipynb](NHP_M1_spikes/main.ipynb). The codes for generating the figures can be found in [plots.ipynb](NHP_M1_spikes/plots.ipynb).

The codes for the mouse dataset analysis can be found at [ketamine](ketamine). To run this code, simply execute the python file in a directory with the specified datasets, downloadable at the link above.

The codes for the zebrafish dataset analysis can be found at [Fish_spinal_cord_imaging](Fish_spinal_cord_imaging). Examples of how to run the codes can be found in [main.ipynb](Fish_spinal_cord_imaging/main.ipynb). The codes for generating the figures can be found in [plots.ipynb](Fish_spinal_cord_imaging/plots.ipynb).

## Project Report

The project report can be found at [here](https://drive.google.com/file/d/1_TsoPetPZEXa9ZDKCPXvtNDwEh22UZDl/view?usp=sharing) or [here](EE_274_Project_Final_Report.pdf).

## References:
[1] Yamada, L., Nuyujukian, P. H., Nishimura, D. G., Weissman, T. A compression-enabled approach to analyze seizures for people with refractory epilepsy. Stanford University. 2023

[2] Higgins G, et al. The effects of lossy compression on diagnostically relevant seizure information in EEG signals. IEEE J Biomed Health Inform. 2013

[3] Nguyen, B., Ma, W., Tran, D. A study of combined lossy compression and seizure detection on epileptic EEG signals. Procedia Computer Science. 2018


