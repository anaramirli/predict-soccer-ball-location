# Predicting Ball Location From Optical Tracking Data

In this study, an automated method for predicting the ball’s location during a soccer match has been developed using
optical tracking data. The rolespecific analysis using the individual player attributes has been
conducted on a dataset of 298 matches from the Turkish Football Federation Super League 2017-2018 season (≈34,000,000 data
points).


The data is provided by an optical  tracking  system  developed  by start-up  company [Sentio  Sports  Analytics](https://sentiosports.com/).


The project contains data analysis, features construction, model development and testing files written using python.

Project consists of 2 models:
* X REG: nn regression model predicts ball's location on x-axis
* Y REG: nn regression model predicts ball's location on y-axis

Performance overview:

| Model | Train RMSE / MAE Loss | Validation RMSE / MAE Loss | Test RMSE / MAE Loss
| :--- | :---: | :---: | :---: 
| X REG | 9.90/6.47 m | 11.23/7.39 m | 11.46/7.56 m
| Y REG | 2.01/1.62 m | 2.00/1.61 m | 2.00/1.61 m

</br>
</br>

![](https://github.com/anaramirli/predict-soccer-ball-location/blob/master/assets/sample.gif)
Orange and blue point -> home and away team players</br>
Green dot -> actual ball location</br>
Red dot -> predicted ball location</br>


## License
This library (all the notebooks) is distributed under Apache License 2.0 . Please see Apache License 2.0 terms to learn about how to use this library.


# Project Instructions

## Getting Started

1. Clone the repository, and navigate to the downloaded folder.

    ```
    git clone https://github.com/anaramirli/predict-soccer-ball-location.git
    cd predict-soccer-ball-location
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
