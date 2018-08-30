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
import operator
from os.path import join
import scipy as sc



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
    
    if x<=31.5:
        j=5
    elif x<=42:
        j=8
    elif x<=52.5:
        j=11
    elif x<=63:
        j=14
    elif x<=73.5:
        j=17
    elif x<=84:
        j=20
   
    index = i+j
    
    
    if y>22 and y<=46:
        if x<=10.5:
            index=2
        elif x<=21:
            index=4
        
        if x>84:
            if x<=94.5:
                index = 24
            else:
                index = 26
    
        
    if x<=21:
        if y<=22:
            index = 1
        elif y>46:
            index = 3
        
    if x>84:
        if y<=22:
            index = 23
        elif y>46:
            index = 25
    
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
    
    occurence = []
    for i in range(27):
        occurence.append(Counter(feature_df['pitch_index'])[i])
    occurence = np.sort(occurence)
    max_occurecnce = max(occurence)
    thserhlod_value = occurence[25]

    feature_df = feature_df.sample(frac=1).reset_index(drop=True)
    feature_df.sort_values('pitch_index', inplace=True)
    feature_df.reset_index(inplace=True, drop=True)

    zero_seperation_value = 140 if max_occurecnce-thserhlod_value >= 140 else max_occurecnce-thserhlod_value

    # iloc, shuffle and rest
    feature_df = feature_df.iloc[max_occurecnce-zero_seperation_value:]
    feature_df = feature_df.sample(frac=1).reset_index(drop=True)
    
    return feature_df

def construct_test_set(event_files):
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
        
        slow_group_id=[]
        hir_group_id=[]
    
        if len(team_f_speed_dict[f_a_i])!=0:

            player_x = []
            player_y = []
            
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
                    slow_group_id.append(player)
                elif s_group==1:
                    f_group_v[f_a_i][10] += x_data[player][1]
                    f_group_v[f_a_i][11] += y_data[player][1]
                    hir_group_id.append(player)
                    
            
            f_group_v[f_a_i][4:7] = f_group_v[f_a_i][4:7]/len(team_f_speed_dict[f_a_i])

            f_group_v[f_a_i][0] = max(player_x)
            f_group_v[f_a_i][1] = min(player_x)
            f_group_v[f_a_i][2] = max(player_y)
            f_group_v[f_a_i][3] = min(player_y)

            # calculate avrg for slow group
            if len(slow_group_id)==1:
                f_group_v[f_a_i][9] = 1
        
            elif len(slow_group_id)>1:
                f_group_v[f_a_i][7:9] = f_group_v[f_a_i][7:9] / len(slow_group_id)
                max_distance_slow = []
                for player_s in slow_group_id:
                    max_distance_slow.append(math.fabs(f_group_v[f_a_i][7]-x_data[player_s][1]))

                max_distance_slow = max(max_distance_slow)
                if max_distance_slow<1:
                    max_distance_slow=1
                f_group_v[f_a_i][9] = 1/max_distance_slow

                
            # calculate avrg for hir group
            if len(hir_group_id)==1:
                f_group_v[f_a_i][12] = 1
        
            elif len(hir_group_id)>1:
                f_group_v[f_a_i][10:12] = f_group_v[f_a_i][10:12] / len(hir_group_id)
                max_distance_hir = []
                for player_s in hir_group_id:
                    max_distance_hir.append(math.fabs(f_group_v[f_a_i][10]-x_data[player_s][1]))

                max_distance_hir = max(max_distance_hir)
                if max_distance_hir<1:
                    max_distance_hir=1
                f_group_v[f_a_i][12] = 1/max_distance_hir

                
            # calcualte max-Sprint player
            if max(team_f_speed_dict[f_a_i].items(), key=operator.itemgetter(1))[1] > 3:
                max_speed_id = max(team_f_speed_dict[f_a_i].items(), key=operator.itemgetter(1))[0]
                f_group_v[f_a_i][13]  = x_data[max_speed_id][1]
                f_group_v[f_a_i][14] = y_data[max_speed_id][1]
                f_group_v[f_a_i][15] = team_f_speed_dict[f_a_i][max_speed_id]

           

    # calculate avrg for team
    if len(team_x)!=0:
        team_v[0] = max(team_x)
        team_v[1] = min(team_x)
        team_v[2] = max(team_y)
        team_v[3] = min(team_y)
        team_v[4:7] = team_v[0:3] / len(team_x)
    else:
        team_v[0:7] = 0
        f_group_v[f_a_i][0:len(f_group_v[0])] = 0
        
    
    
    
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