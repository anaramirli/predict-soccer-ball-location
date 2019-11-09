# Predicting Ball Location From Optical Tracking Data

In this study, an automated method for predicting the ball’s location during a soccer match has been developed using
optical tracking data with a random forest classifier. The rolespecific analysis using the individual player attributes has been
conducted on a dataset of 298 matches from the Turkish Football Federation Super League 2017-2018 season (≈34,000,000 data
points).

The data is provided by an optical  tracking  system  developed  by start-up  company [Sentio  Sports  Analytics](https://sentiosports.com/).

This study is partially supported by TUBITAK under the grant number 118C019 and by ODTÜ BAP under project code YÖP-312- 2018-2816. 

The project contains data analysis, features construction, model development and testing files written using python.

Project consists of 3 models:
* Game-state CLF: nn classification model determines whether game is stopped or not
* X REG: nn regression model predicts ball's location on x-Axis
* Y REG: nn regression model predicts ball's location on y-Axis

Performance overview:

| Model | Train Acc/Loss | Validation Acc/Loss | Test Acc/Loss
| :--- | :---: | :---: | :---: 
| Game-state CLF | 87.78/30.45% | 87.44/31.76% | 85.00/37.29%


| Model | Train MSE / MAE Loss | Validation MSE / MAE Loss | Test MSE / MAE Loss
| :--- | :---: | :---: | :---: 
| X REG | 11.33/8.25 m | 11.67/8.43 m | 12.63/9.06 m
| Y REG | 9.48/7.15 m | 9.75/7.26 m | 10.29/7.65 m


`src` directory to view `README.md` file describing the notebooks and their structure.

![](https://github.com/anaramirli/soccerBallTracker/blob/master/src/assets/sample.gif)

- **Orange and blue points**: Home and away team players</br>
- **Green point**: Actual ball location</br>
- **Red point**: Predicted ball location</br>

## License
This library (all the notebooks) is distributed under Apache License 2.0 . Please see Apache License 2.0 terms to learn about how to use this library.


# Project Instructions

## Getting Started

1. Clone the repository, and navigate to the downloaded folder.

    ```
    git clone https://github.com/anaramirli/soccer-ball-tracker.git
    cd soccer-ball-tracker
    ```
    
2. Create (and activate) a new environment with Python 3.6 and the numpy package.

    * **Linux** or **Mac**:
    ```
    conda create --name my_env python=3.6
    source activate my_env
    ```
    
    * **Windows**:
    
    ```
    conda create --name my_env python=3.6
    activate my_env
    ```

3. Check requiremenets.
    ```
    requirements.py
    ```