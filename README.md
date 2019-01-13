# Predicting Ball Location From Optical Tracking Data

Model which is designed to predict ball location on the pitch during a soccer match using spatiotemporal data by utilizing machine learning algorithms.

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
    conda create --name aind-vui python=3.5 numpy
    source activate aind-vui
    ```
    
    * **Windows**:
    
    ```
    conda create --name aind-vui python=3.6 numpy scipy
    activate aind-vui
    ```

3. Check requiremenets.
    ```
    requirements.py
    ```
