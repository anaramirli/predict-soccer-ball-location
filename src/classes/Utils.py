import pandas as pd
import numpy as np
import math
from collections import Counter
from scipy.ndimage.interpolation import shift
import matplotlib.pyplot as plt
import operator
from os.path import join
import scipy as sc
import warnings
import json
import functools
import itertools


from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


def dictKeyLower(iterable):
        
        '''
        Converts keys of dict to lowercase
        
        Parameters
        ----------
        iterable: dict
        '''
        
        new_iterable = {}

        for key, value in iterable.items():
            if type(iterable[key]) is dict:
                value = dictKeyLower(value)
                
            new_iterable[key.lower()] = value.lower() if type(value) is str else value  
            
        return new_iterable
    
def construct_data_set(csv_file):
    
    '''
    dataset construction function used with pooling
    
    Parameters
    ----------
    evet_file: directory of feature csv file
    
    Output
    ------
    feature_df: shuffled panda data frame
    '''
    
    pd.options.mode.chained_assignment = None
    feature_df = pd.DataFrame()

    # get match information with split (file name regex: r'match_\d+.csv')
    match_id = csv_file.split('_')[0]

    try:
        feature_df = pd.read_csv(csv_file)
        print('Current data: {}'.format((match_id)))
    except FileNotFoundError:
        print('No feature data for: {}'.format(match_id))
        return
    
    return feature_df


def innerDBSCAN(data, eps_range, eps_min_sample):
    
    '''
    Finds density based clusters
    
    Parameters
    ----------
    data: 2d array (x, y)
    esp_range:
    esp_min_sample: 
    
    Outputs
    -------
    list of sub indices from data array which are located in the largets cluster
    '''

    sub_indices = []
    data_indices = np.zeros(shape=(len(data)), dtype=np.int8)
    for V_i in range(len(data)):
        data_indices[V_i]=V_i


    # get cluster
    db = DBSCAN(eps=eps_range, min_samples=eps_min_sample).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    unique_labels = set(labels) # get clusters

    # get most common (largest) cluster
    max_key = 0
    if len(Counter(labels))==1 and Counter(labels).most_common(1)[0][0]!=-1:
        max_key=Counter(labels).most_common(1)[0][0]
    elif len(Counter(labels))>1:
        if Counter(labels).most_common(1)[0][0]==-1:
            max_key = Counter(labels).most_common(2)[1][0]
        else:
            max_key = Counter(labels).most_common(2)[0][0]


    for k_label in unique_labels:
        class_member_mask = (labels == k_label)
        if max_key!=-1 and max_key==k_label:
            sub_indices = data_indices[class_member_mask & core_samples_mask]

    return sub_indices    


def categorize_array(y, target_size):
        """
        # prepare categorical target values (y) (e.g [0,0,0,1,0])
        Paramaters
        ----------
        y_data: target data
        
        """
        
        target = np.zeros((len(y),target_size),dtype=int)
        for i,_ in enumerate(y):
            target[i][int(_)]=1
        
        return target
    
def uncategorize_array(y, axis=1):
    '''
    untageroize data with arg max
    '''

    return np.argmax(y, axis)
              
def distance_2points(x1, y1, x2, y2):
    '''
    return distance between two point
    
    '''
    return round(math.sqrt((x1-x2)**2 + (y1-y2)**2), 2)

def calculate_average(pos_list):
    '''
    return average distance, if list empty then return -1
    '''
    return round(sum(pos_list)/len(pos_list), 2) if len(pos_list)>0 else -1


def load_json_content(file):
    '''
    load json content from url
    '''
    with open(file, 'r') as file:
            data = json.load(file)
    
    return data



def plot_hbar_nameval(names, values, xlabel, max_bars=30):
    
    """
    Plots a horizontal bar chart with names as labels and values as the length
    of the bars.
    Parameters
    ----------
    names : Iterable
        Bar labels.
    values : Iterable
        Corresponding value of each label given in names.
    xlabel : str
        Label of the horizontal axis.
    max_bars : int
        Maximum number of horizontal bars to plot.
    Returns
    -------
    fig : matplotlib.figure
        Plot figure.
    ax : matplotlib.Axes
        matplotlib.Axes object with horizontal bar chart plotted.
    """
    name_val = list(zip(names, values))
    name_val.sort(key=lambda t: t[1], reverse=True)
    if len(name_val) > max_bars:
        name_val = name_val[:max_bars]
    names, values = zip(*name_val)

#     plt.figure(figsize=(10, 8))
    plt.rcdefaults()
    
    

    y_pos = np.arange(len(names))

    plt.barh(y_pos, values, align='center')
    plt.yticks(y_pos,names)
    plt.gca().invert_yaxis()
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.show()


def plot_confusion_matrix(cm,
                          classes,
                          xlabel,
                          ylabel,
                          normalize=False,
                          cmap=plt.cm.Blues):
    """
    Plot the given confusion matrix cm as a matrix using and return the
    resulting axes object containing the plot.
    Parameters
    ----------
    cm : ndarray
        Confusion matrix as a 2D numpy.array.
    classes : list of str
        Names of classified classes.
    xlabel : str
    Label of the horizontal axis.
    ylabel : str
    Label of the vertical axis.
    normalize : bool
        If True, the confusion matrix will be normalized. Otherwise, the values
        in the given confusion matrix will be plotted as they are.
    cmap : matplotlib.colormap
        Colormap to use when plotting the confusion matrix.
    Returns
    -------
    fig : matplotlib.figure
        Plot figure.
    ax : matplotlib.Axes
        matplotlib.Axes object with horizontal bar chart plotted.
    References
    ----------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    vmin = None
    vmax = None
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        vmin = 0
        vmax = 1

    plt.figure(figsize=(9, 9))
    cax = plt.imshow(
        cm, interpolation='nearest', vmin=vmin, vmax=vmax, cmap=cmap)
    plt.colorbar(cax)

    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)


    plt.yticks(tick_marks,classes)


    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        cell_str = '{:.2f}'.format(cm[i, j]) if normalize else str(cm[i, j])
        plt.text(
            j,
            i,
            cell_str,
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
  
    plt.show()
    
    
    
    import matplotlib.pyplot as plt

def plot_model_history(values, legend, title, ylabel='Accuracy', xlabel='Epoch', figure_size=(15,7)):
    
    '''
    Plot history values
    
    Parameters
    ----------
    history: python keras traning history
    ylabel&xlabel: labels for figure
    legend: legend labels for figure
    title: title of the figure
    val_label: labels for each data unit stored in the history  
    
    '''
    
    plt.figure(figsize=figure_size)
    
    
    if (type(title)!=str or title==None):
        raise ValueError
        
    if (values==None):
        raise ValueError
        
    if (type(legend)!=list or legend==None):
        raise ValueError
    
    for val_i in values:
        plt.plot(val_i)
        
    plt.title(title)
    
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend(legend, loc='upper left')
    plt.show()