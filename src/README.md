## Core Source Files
These are the notebooks used during model development and optimization.

### feature_construction.ipynb
------------------------------
This is the notebook in which we compute features from player coordinate data. This notebook contains our initial feature construction code. We generate input (aligning player trajectories based in role and then setting new features based on spatiotemporal data) and output data in order to build model for predicting ball location over the pitch. Due to losses in data, some matches have been extracted, so the total number of matches used is 299.

This was our first notebook when we started this project. Therefore, several ideas written in this document may be replaced or not used at all. However, keeping this notebook as a reference may prove useful in further studies.


### feature_analysis.ipynb
--------------------------
In this notebook, we analyse player coordinate data by plotting various simple features such as average, maximum and minimum coordinates, group speeds, sprint player coordinates, referee position, etc. We try to find relations between outliers or patterns in these features and the events we wish to predict. Additionally, we postulate ideas about how each related feature family can be effective in predicting certain events.

### target_analysis.ipynb
-------------------------
In this doocument, we aim to find ball location during the game. As there are infinite numbers of the data points in the pitch surface, it's merely impossible to predict exact ball location each time. Then we anlisyse number of asssigments to each position segments.

### scale_roleassign_visualization.ipynb
----------------------------------------
In this notebook, we visualize player avrg position (before and after scaling states) by drawing their average position using matplotlip. And also show example of role assignment.
