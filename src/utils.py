# Copyright 2018 Anar Amirli
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


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
import functools
import itertools


from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler




def caluclate_avrg_pos(c_ap_minutes_step, pos_mean, player, pos_count, activity_count):
    '''
    Function for calculating mean of players x,y positions on the pitch
    
    Parameters
    ----------
    c_ap_minutes_step: timeline step for caclulation pas average poisition for speficif minutes 
          
    pos_mean: player's mean position vector for x,y coordinates
    
    player: player position in our player_dict
    
    pos_count: sum of player's x, y coordinates for psat 1 minute
    
    activity_count: play time of player during data frame of pas 1 minute
    '''
    
    avrg_pos_count = 0 
    for c_ap_minutes in range(c_ap_minutes_step):
        pos_mean[player][0] += pos_count[player][0][c_ap_minutes]
        pos_mean[player][1] += pos_count[player][1][c_ap_minutes]
        avrg_pos_count += activity_count[player][c_ap_minutes] 
    if avrg_pos_count!=0:
        pos_mean[player][0] /= avrg_pos_count
        pos_mean[player][1] /= avrg_pos_count
    else:
        pos_mean[player][0] = 0 
        pos_mean[player][1] = 0
        
def caluclate_activity_count(c_ac_minutes_step, player, activity_count):
    '''
    Function for checking activity over the specific period of time
    
    Parameters
    ----------
    c_ap_minutes_step: timeline step for caclulation pas average poisition for speficif minutes 
    
    player: player position in our player_dict
          
    pos_mean: player's mean position vector for x,y coordinates 
    
    activity_count: seconds that player was in game during data frame of pas 1 minute
    '''

    activity_count_each = 0 
    for c_ac_minutes in range(0, c_ac_minutes_step):
        activity_count_each += activity_count[player][c_ac_minutes] 
    
    if activity_count_each != 0:
        return 1
    else:
        return 0
    
def caluclate_last_nzero_ac_count(player_gorup_len, activity_count):
    '''
    Function return the number players those were in game for last minute
    
    Parameters
    ----------
    player_gorup_len: number of players in the team
    
    activity_count: play time of player during data frame of pas 1 minute
    '''
    
    last_activity_count = 0
    for player_lac_i in range(player_gorup_len):
        if activity_count[player_lac_i][1] !=0:
            last_activity_count += 1
            
    return last_activity_count


def caluclate_nzero_activity_count(start, end, player, activity_count):
    '''
    Function to find the minute that the last non-zero activty occured in
    
    Parameters
    ----------
    start, end: time span for calucaltion
    
    player: player position in our player_dict
    
    activity_count: play time of player during data frame of pas 1 minute
    '''
    activity_count_each = 0 
    for c_nz_minutes in range(start, end, -1):
        if activity_count[player][c_nz_minutes-1]!=0:
            return c_nz_minutes-1
        
    return -1


def fist_time_step_mean_data(threshold_second, half,data_persec_t,home_pos_count_minutes,home_activity_count_minutes,
                             away_pos_count_minutes,away_activity_count_minutes, home_dict, away_dict, 
                             home_team_player, away_team_player, home_team_id, away_team_id, player_positionId, minutes_step):
    '''
    At the beginning of each half it took a while to have all players' data, therefore, 
    we should know whether we have all players data those supposed start (in 1st half) 
    and continute (in 2nd half) game or not.
    This function calculates the mean position data of each player as soon as we have all player
    and return the player list that are supposed to start in game.
    
    By that way we'll be able to separately calculate mean pos data for each half . 
    
    Parameters
    ----------
    half: half of match 
    
    data_persec_t: raw data of match for per secdon
    
    activity_count: play time of player during data frame of pas 1 minute
    '''
    
    tmp_time_step_t = 0
    
    for t in data_persec_t:

        first_time_step_i = int(t['minute'])*60 + int(t['second'])
        x_pos = t['xpos']
        y_pos = t['ypos']
        team_id_t = int(t['teamId'])
        jersey_number_t = int(t['jerseyNumber'])
        has_ball_teamId_t = int(t['hasballTeamId'])
        math_half = int(t['half'])


        sec = first_time_step_i-(half-1)*45*60
        time_step = math.floor(sec/60)

        if sec==threshold_second:
            break
            
        if tmp_time_step_t == time_step:
            
            tmp_time_step_t += 1
            
            for player_home in range(len(home_team_player)):
                home_pos_count_minutes[player_home][0] = (shift(home_pos_count_minutes[player_home][0], -1, cval=0))
                home_pos_count_minutes[player_home][1] = (shift(home_pos_count_minutes[player_home][1], -1, cval=0))
                home_activity_count_minutes[player_home] = (shift(home_activity_count_minutes[player_home], -1, cval=0))
                
            for player_away in range(len(away_team_player)):
                away_pos_count_minutes[player_away][0] = (shift(away_pos_count_minutes[player_away][0], -1, cval=0))
                away_pos_count_minutes[player_away][1] = (shift(away_pos_count_minutes[player_away][1], -1, cval=0))
                away_activity_count_minutes[player_away] = (shift(away_activity_count_minutes[player_away], -1, cval=0))

            

        if math_half == half:
            

            if team_id_t == home_team_id:
                
                player_home = home_dict[str(jersey_number_t)]
                if player_positionId['homeTeam'][jersey_number_t] == 1 and has_ball_teamId_t != 0:
                    if x_pos!=0 and y_pos !=0:    
                        home_pos_count_minutes[player_home][0][minutes_step-1] += x_pos
                        home_pos_count_minutes[player_home][1][minutes_step-1] += y_pos
                        home_activity_count_minutes[player_home][minutes_step-1] +=1 

                elif has_ball_teamId_t == away_team_id:
                    if x_pos!=0 and y_pos !=0:    
                        home_pos_count_minutes[player_home][0][minutes_step-1] += x_pos
                        home_pos_count_minutes[player_home][1][minutes_step-1] += y_pos
                        home_activity_count_minutes[player_home][minutes_step-1] +=1 

            elif team_id_t == away_team_id:

                player_away = away_dict[str(jersey_number_t)]
                if player_positionId['awayTeam'][jersey_number_t] == 1 and has_ball_teamId_t != 0:
                    if x_pos!=0 and y_pos!=0:
                        away_pos_count_minutes[player_away][0][minutes_step-1] += x_pos
                        away_pos_count_minutes[player_away][1][minutes_step-1] += y_pos
                        away_activity_count_minutes[player_away][minutes_step-1] +=1  

                elif has_ball_teamId_t == home_team_id:
                    if x_pos!=0 and y_pos!=0:
                        away_pos_count_minutes[player_away][0][minutes_step-1] += x_pos
                        away_pos_count_minutes[player_away][1][minutes_step-1] += y_pos
                        away_activity_count_minutes[player_away][minutes_step-1] +=1  

                        
    return home_activity_count_minutes, away_activity_count_minutes


def define_role(x, y, pitch_value, gk_state):
    '''
    Function to define players role in the game
    
    Parameters
    ----------
    x, y: coordinates
    
    pitch_value: pitch segment value
    
    Returns
    -------
    1-6: players rolse assigment indexes
      7: goalkeeper
     -1: player is not in game
    
    '''
    
    # gk_state==1 := golakeeper
    if gk_state==1:
        return 7
    else:
        for pitch_i in range(0,7):
            if x>=pitch_value[pitch_i][0] and x<pitch_value[pitch_i][1] and y>=pitch_value[pitch_i][2] and y<pitch_value[pitch_i][3]:
                return pitch_i
    return -1




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

    plt.figure(figsize=(10, 8))
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

    plt.figure(figsize=(12, 12))
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





def define_pitch_index(x,y):
    '''
    Function to define pitch index and role
    
    Parameters
    ----------
    x, y: coordinates
    
    pitch_value: pitch segment value
    
    Returns
    -------
    1-33: pitch index
        0: Null index(0) represents all the index categories, that occur when the game stops.
    '''
    i=0
    j=0
    

    if y<=22:
        i=0
    elif y<=46:
        i=1
    else:
        i=2
        
    if x<=22.5:
        j=1
    elif x<=42.5:
        j=4
    elif x<=62.5:
        j=7
    elif x<=82.5:
        j=10
    else:
        j=13
   
    index = i+j   
    
#     if y>22 and y<=46:
#         if x<=10.5:
#             index=2
#         elif x<=21:
#             index=4
        
#         if x>84:
#             if x<=94.5:
#                 index = 24
#             else:
#                 index = 26
    
        
#     if x<=21:
#         if y<=22:
#             index = 1
#         elif y>46:
#             index = 3
        
#     if x>84:
#         if y<=22:
#             index = 23
#         elif y>46:
#             index = 25
    
    assert index>0, 'Index can not be zero or non negative: index-value: {}, x-value: {}, y-value: {}'.format(index, x,y)
    
    return index


def construct_train_set(event_files):
    pd.options.mode.chained_assignment = None
    feature_df = pd.DataFrame()

    # get match information
    match_id = event_files.split('_')[0]
    
    try:
        feature_df = pd.read_csv(join('../data/general/feature-set/', event_files))
        print('Current data: {}'.format(match_id))
    except FileNotFoundError:
        print('No feature data for: {}'.format(match_id))
        return
    
    
    if Counter(feature_df['pitch_index']).most_common(2)[0][0]==0:
        max_occurecnce = Counter(feature_df['pitch_index']).most_common(2)[0][1]
        count=0
        thserhlod_value=0
        for key, val in sorted(Counter(feature_df['pitch_index']).items()):
                if key!=0 and key!=1 and key!=3 and key!=13 and key!=15:
                    thserhlod_value+=val
                    count+=1
        thserhlod_value= thserhlod_value//(count-1)

        feature_df = feature_df.sample(frac=1).reset_index(drop=True)
        feature_df.sort_values('pitch_index', inplace=True)
        feature_df.reset_index(inplace=True, drop=True)

        zero_seperation_value = 0 if thserhlod_value>max_occurecnce else max_occurecnce-thserhlod_value
        

        # iloc, shuffle and rest
        feature_df = feature_df.iloc[zero_seperation_value:]
        feature_df = feature_df.sample(frac=1).reset_index(drop=True)
    
    return feature_df

def construct_data_set(event_files):
    pd.options.mode.chained_assignment = None
    feature_df = pd.DataFrame()

    # get match information
    match_id = event_files.split('_')[0]

    try:
        feature_df = pd.read_csv(join('../data/general/feature-set/', event_files))
        print('Current data: {}'.format(match_id))
    except FileNotFoundError:
        print('No feature data for: {}'.format(match_id))
        return
    
    # iloc, shuffle and rest
    feature_df = feature_df.sample(frac=1).reset_index(drop=True)
    
    return feature_df


def speed_group(speed):
    if speed<=1.5: # slow Speed (V)
        return 0
    elif speed<=3: # HIR
        return 1
    else: # Sprint (S)
        return 2

def define_direction(delta):
    if delta==0:
        return 0
    elif delta>0:
        return 1
    else:
        return -1
    
def features_adjust(f_group_v, team_v, team_f_speed_dict, x_data, y_data):
    '''
    Function to calculates final features based on pitch index and role
    
    Parameters
    ----------
    f_group_v: players groups
    
    team_v: team info
    
    team_f_speed_dict: team speed dict
    
    x_data: players' x coordinate for 2 seperate data frame
    
    y_data: players' y coordinate for 2 seperate data frame
    
    '''
    
    team_x = []
    team_y = []
    
    for f_a_i in range(7):
        
        
    
        if len(team_f_speed_dict[f_a_i])!=0:

            player_x = []
            player_y = []
            
            slow_group_count=0
            hir_group_count=0
            
            for player, speed in team_f_speed_dict[f_a_i].items():
                s_group = speed_group(speed)
                
                player_x.append(x_data[player][1])
                player_y.append(y_data[player][1])
                team_x.append(x_data[player][1])
                team_y.append(y_data[player][1])

                team_v[4] += x_data[player][1]
                team_v[5] += y_data[player][1]
                team_v[6] += speed


                f_group_v[f_a_i][4] += x_data[player][1]
                f_group_v[f_a_i][5] += y_data[player][1]
                f_group_v[f_a_i][6] += speed

                if s_group==0:
                    f_group_v[f_a_i][7] += x_data[player][1]
                    f_group_v[f_a_i][8] += y_data[player][1]
                    slow_group_count+=1
                elif s_group==1:
                    f_group_v[f_a_i][9] += x_data[player][1]
                    f_group_v[f_a_i][10] += y_data[player][1]
                    hir_group_count+=1
            
            f_group_v[f_a_i][4:7] = f_group_v[f_a_i][4:7]/len(team_f_speed_dict[f_a_i])

            f_group_v[f_a_i][0] = max(player_x)
            f_group_v[f_a_i][1] = min(player_x)
            f_group_v[f_a_i][2] = max(player_y)
            f_group_v[f_a_i][3] = min(player_y)

            # calculate avrg for slow group
            if slow_group_count>1:
                f_group_v[f_a_i][7:9] = f_group_v[f_a_i][7:9] / slow_group_count
                
            # calculate avrg for hir group
            if hir_group_count>1:
                f_group_v[f_a_i][9:11] = f_group_v[f_a_i][9:11] / hir_group_count
        
           
                
            # calcualte max-Sprint player
            if max(team_f_speed_dict[f_a_i].items(), key=operator.itemgetter(1))[1] > 3:
                max_speed_id = max(team_f_speed_dict[f_a_i].items(), key=operator.itemgetter(1))[0]
                f_group_v[f_a_i][11]  = x_data[max_speed_id][1]
                f_group_v[f_a_i][12] = y_data[max_speed_id][1]
                f_group_v[f_a_i][13] = team_f_speed_dict[f_a_i][max_speed_id]

           

    # calculate avrg for team
    if len(team_x)!=0:
        team_v[0] = max(team_x)
        team_v[1] = min(team_x)
        team_v[2] = max(team_y)
        team_v[3] = min(team_y)
        team_v[4:7] = team_v[4:7] / len(team_x)
    else:
        team_v[0:7] = 0
        f_group_v[f_a_i][0:len(f_group_v[0])] = 0
        

        
def innerDBSCAN(X_all, x_all, eps_range, eps_min_sample):
    teamDBSCAN_x=0
    teamDBSCAN_y=0

    value_ids = np.zeros(shape=(len(X_all)), dtype=np.int8)

    for V_i in range(len(X_all)):
        value_ids[V_i]=V_i

    val_id=[]

    db = DBSCAN(eps=eps_range, min_samples=eps_min_sample).fit(X_all)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    unique_labels = set(labels)

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
            val_id = value_ids[class_member_mask & core_samples_mask]


    if max_key== -1 or len(val_id)==0:
        teamDBSCAN_x += np.sum(x_all[:,0], axis=0) / len(x_all)
        teamDBSCAN_y += np.sum(x_all[:,1], axis=0) / len(x_all)
    else:
        for value_i in val_id:
            teamDBSCAN_x += x_all[value_i][0]
            teamDBSCAN_y += x_all[value_i][1]

        teamDBSCAN_x/=len(val_id)
        teamDBSCAN_y/=len(val_id)
        
    return teamDBSCAN_x, teamDBSCAN_y
    
def feature_generation(r,speed,jersey_no,features_count, team_f_speed_dict):
    if r<=6:
        features_count[r][0] += 1
        team_f_speed_dict[r][jersey_no]=speed
            
            
def scale_linear_data(rawpoints, high, low):
    '''
    Function for sclaing player avrg position to the to the range of (105+std)(68-std)
    
    Parameters
    ----------
    rawpoints: player average pos data
    
    high: furthest point of scaling range
    
    low: lowest point of scaling range
    
    std: standard deviation of player positions 
    
    '''
    mins = np.min(rawpoints, axis=0)
    maxs = np.max(rawpoints, axis=0)
    rng = maxs - mins
    return high - (((high - low) * (maxs - rawpoints)) / rng)