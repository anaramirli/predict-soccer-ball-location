# Predicting Ball Location From Optical Tracking Data

In this study, an automated method for predicting the ball’s location during a soccer match has been developed using
optical tracking data with a random forest classifier. The rolespecific analysis using the individual player attributes has been
conducted on a dataset of 298 matches from the Turkish Football Federation Super League 2017-2018 season (≈34,000,000 data
points). The average coefficient of determination R^2 of the ball tracking model on the test set of x-axis and y-axis are, accordingly, 81% and 75.1% where the mean square error is ±10.87 meters for the x-axis and ±9.41 meters for the y-axis.

The data is provided by an optical  tracking  system  developed  by start-up  company [Sentio  Sports  Analytics](https://sentiosports.com/).

This study is partially supported by TUBITAK under the grant number 118C019 and by ODTÜ BAP under project code YÖP-312- 2018-2816. 

The project contains data analysis, features construction, model development and testing files written using python.

Project consists of 3 models:
* Game State Model (determines whether game is stopped or not) `Random Forest Classifier`
* Ball Location Prediction x-Axis `Random Forest Regressor`
* Ball Location Prediction y-Axis `Random Forest Regressor`

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
