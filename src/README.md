## Core Source Files
These are the notebooks used during model development and optimization.

### requirements.ipynb
----------------------
This is the notebook you can use to check if your system meets the requirements to run all the notebooks. If all is okay, then you're good to go.

### DBSCAN_test.ipynb
---------------------
In this notebook, we compute desnity-based clustering (DBSCAN) features and see if they can potentially be used to predict segments of interest.

### feature_construction.ipynb
------------------------------
This is the notebook in which we compute features from player coordinate data. This notebook contains our initial feature construction code. We generate input (aligning player trajectories based in role and then setting new features based on spatiotemporal data) and output data in order to build model for predicting ball location over the pitch. Due to losses in data, some matches have been extracted, so the total number of matches used is 299.

This was our first notebook when we started this project. Therefore, several ideas written in this document may be replaced or not used at all. However, keeping this notebook as a reference may prove useful in further studies.

### feature_analysis.ipynb
--------------------------
In this notebook, we analyze player coordinate data by plotting various simple features such as average, maximum and minimum coordinates, group speeds, sprint player coordinates, referee position, etc. We try to find relations between outliers or patterns in these features and the events we wish to predict. Additionally, we postulate ideas about how each related feature family can be effective in predicting certain events.

### target_analysis.ipynb
-------------------------
In this document, we aim to find ball location during the game. As there are infinite numbers of the data points in the pitch surface, it's merely impossible to predict exact ball location each time. Then we analyze number of assignments to each position segments.

### dataset_construction.ipynb
------------------------------
In this notebook, we construct training and test datasets using already computed feature datasets.

### regressor_testing.ipynb
---------------------------
In this document, we test our Random Forest for classifying the ball state (wheter game is stoped or not) and the ball coordinate on the y-axis

### classifier_testing.ipynb
----------------------------
In this document, we test our Random Forest for classifying the ball state (wheter game is stoped or not) and the ball y-coordinate segment

### scale_roleassign_visualization.ipynb
----------------------------------------
In this notebook, we visualize player avrg position (before and after scaling states) by drawing their average position using matplotlip. And also show example of role assignment.

### pitch_segment_visualization.ipynb
-------------------------------------
In this notebook, we visualize our segments and pitch index assignment.

### utils.py
------------
This file contains the common utility functions that are used from different notebooks.
