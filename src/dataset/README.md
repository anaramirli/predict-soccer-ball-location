### Dataset structure

.zip folder contains train and test csv files.

* Train set: nxd, n=1563656, d=306
* Test set:  m*d, m= 173600, d=306

### Headers

> First 4 columns store game info:
* match_id, half, minute, second

> Next 3 columns store target info
* game_state, x, y

> The remaining 299 columns store the features. The detailed info on data features can be found on *feature_generation.ipynb*

### Download datasets

You download dataset from github. Dataset also can directly be downloaded by running the following lines:

```
wget  https://github.com/anaramirli/predict-soccer-ball-location/raw/master/src/dataset/(train%26test-csv).zip
unzip (train&test-csv).zip
rm (train&test-csv).zip
```