# EE274 Final Project: Compression and Neural Data

## Midterm Report
### Introduction:
The complexity of neural data changes as the brain process information during events.
Compression ratio may be used as an estimator for the complexity of a given signal.
Compression ratio and the inverse compression ratio (ICR) have been used to detect seizure from neural array recordings in epileptic patients, a task typically done with tedious manual inspection.
However, it remains unknown how these findings generalize to other events and neural data modalities.
Characterizing the use of ICR in neural data across species and collection modalities may help establish efficient, information-theoretic tools for medical diagnosis.
Another goal of the project is to see if there are internal relations between compression ratios of neural data across different species; similarities may reveal potential commanalities between cortical structures.

### Literature/Code review:
As mentioned above, previous work has shown that compression algorithms may be used to detect seizure from neural array recordings in epileptic patients with comparable accuracy to current methods like manual inspection [1,2].
Previous work has also demonstrated that lossy compression algorithms, such as those used in video compression, perform better than gzip, a lossless compressor [1, 3].

### Methods:
By first binning data, we will compute time-series compression ratios using both lossless (zstd, gzip) and lossy (neural network-based compressors, h264) algorithms.
While our data is not video-based, lossy video compressors (like h264) have been used in the literature due to their ease in use with time-series data [1].
To measure success of our project, we will correlate behavioral/stimulus data to time-series inverse compression ratios.
If compression ratio may be used to indicate event onset with the given dataset and compressor, we expect to see a statistically significant result emerge from our correlation.
We will also train classifiers based on the compression ratio to measure if the compression ratio of neural data is a good indicator of event onsets. The results can be evaluated by metrics including the area under receiver operating characteristic curve (AUROC) and the area under precision-recall curve (AUPR).
Furthermore, we will compare results between different lossless and lossy compressors to understand how compression may be used to characterize neural data.
In line with previous work, we expect to be able to detect statistically significant state/event changes with ICR metrics.
Additionally, if the values of compression ratios lie in the same range cross-species, this may indicate potential computational structures in cortices that are preserved during evolution.

### Progress report:
So far, we have decided to use four distinct datasets in order to analyze how compression algorithms may be used to track the complexity of neural signals recorded with different modalities and tracked behaviors.
These four datasets include intracortrical array data from human epilepsy patients (seizure/no seizure), noninvasive electroencephalography (EEG) data from healthy human subjects performing a task (left/right), intracortical array data from non-human primates (pre-lesion/post-lesion), and intacortical probe data from mice (reward/no reward).
We are additionally considering changing our EEG dataset to a calcium imaging dataset on Drosophila (fruit flies) to better support claims on the multi-species and multi-modality utility of ICR as a neural event detection technique.
Access to all datasets have been secured.
Each dataset may be labeled with two binary states, such as reward/no reward or stroke/no stroke, to allow us to easily classify neural events that may be detectable with ICR.
We have began to implement lossless compressors to calculate compression ratios.
We have settled on using ZSTD and GZIP to calculate lossless ICR values.
We are also using statistical tests to evaluate the similarity between the binary states in the data.
Please see the gitlab repo associated with this readme file for our current code progress; we currently have prelimary results for NHP and human epileptic datasets.
Please see the .md files associated with the _report folders to see detailed reports of specific progress for each dataset.
In the remaining weeks, we plan to complete analysis, namely by implementing lossy compressors and extending analysis to the rest of the datasets.
The lossy compressor we have decided to use is h264.
We will convert data into frames before using h264 to understand compression rate for subsections of binned frames.

The progress report on intracortical array data from non-human primates can be found at [NHP_M1_spikes_report](NHP_M1_spikes_report/milestone_report_yuxin.md).

The progress report on epilepsy data from human patients can be found at [Human_Epi_report](Human_Epi_report/milestone_report_alice.md).


### References:
[1] Yamada, L., Nuyujukian, P. H., Nishimura, D. G., Weissman, T. A compression-enabled approach to analyze seizures for people with refractory epilepsy. Stanford University. 2023

[2] Higgins G, et al. The effects of lossy compression on diagnostically relevant seizure information in EEG signals. IEEE J Biomed Health Inform. 2013

[3] Nguyen, B., Ma, W., Tran, D. A study of combined lossy compression and seizure detection on epileptic EEG signals. Procedia Computer Science. 2018





## Nov 10 Meeting Notes:
* four datasets:
  * Monkey reaching data, before/after stroke (Yuxin): from Paul
  * Neuropixel mouse data, receiving reward (Alice): https://dandiarchive.org/dandiset/000053?search=giocomo&pos=3
  * EEG human data, left/right task (Yuxin): https://crcns.org/data-sets/methods/eeg-1/about-eeg-1
  * intractorical array data, epilepsy (Alice): from Lisa
* Algorithms:
  * Lossless compressors: ZSTD and GZIP
  * Lossy compressors: h264
* Work on establishing access to datasets by next meeting: 11/16 (Thursday)
