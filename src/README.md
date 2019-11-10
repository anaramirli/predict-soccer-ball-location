This markdown gives a brief intro into the "scr" structure.

Directories:
* **classes**: contains main classes and models
    * **DataModel.py**: data model and main modules for data-handling. 
    * **FeatureBuilder.py**: calculates features from given data
    * **NNBuilder.py**: for easily generating the desired nn models in traning 
    * **NNParameterValdate.py**: validate values of given nn structure
    * **Utils.py**: general utility functions
* **feature analysis**: contains ipynb files for feature and target data analyzing. those analyses were conducted with old datasets, therefore labels can be different.
* **rf old**: contains previous files for training and testing models with old datasets using random forest methods.
* **rest api**: fetching json data from rest apis
* **logs**: contains logs of nn model training

main ipynb files:
* **dataset_construction.ipynb**: generating dataset
* **feature_generation.ipynb**: generate features from json files
* **nn_clf_gamestate.ipynb**: building, analyzing, testing of nn classification model for game state
* **nn_reg_ball_location.ipynb**: building, analyzing, testing of nn regression model for ball's location on x and y axes.
