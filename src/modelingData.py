from __future__ import division

import json
import pickle
import pandas as pd
import numpy as np
import math
from scipy.ndimage.interpolation import shift
from matplotlib import style
import matplotlib.pyplot as plt


style.use('ggplot')


#Function for calculating mean of players x,y positions on the pitch
def caluclate_avrg_pos(c_ap_minutes_step, pos_mean, player, pos_count, activity_count):
    avrg_pos_count = 0 
    for c_ap_minutes in range(0,c_ap_minutes_step):
        pos_mean[player][0] += pos_count[player][0][c_ap_minutes]
        pos_mean[player][1] += pos_count[player][1][c_ap_minutes]
        avrg_pos_count += activity_count[player][c_ap_minutes] 
    if avrg_pos_count!=0:
        pos_mean[player][0] /= avrg_pos_count
        pos_mean[player][1] /= avrg_pos_count
    else:
        pos_mean[player][0] = 0 
        pos_mean[player][1] = 0
		

#Function for checking activity over the specific period of time		
def caluclate_activity_count(c_ac_minutes_step, player, activity_count):
    
    activity_count_each = 0 
    for c_ac_minutes in range(0, c_ac_minutes_step):
        activity_count_each += activity_count[player][c_ac_minutes] 
    
    if activity_count_each != 0:
        return 1
    else:
        return 0
		
		
# Function for calculating last number of non-zero activities occurred in last minute		
def caluclate_last_nzero_ac_count(player_gorup_len, activity_count):
    
    last_activity_count = 0
    for player_lac_i in range(0, player_gorup_len):
        if activity_count[player_lac_i][1] !=0:
            last_activity_count += 1
            
    return last_activity_count
	
	
# Function to find the minute that the last non-zero activity occurred in	
def caluclate_nzero_activity_count(start, end, player, activity_count):
    
    activity_count_each = 0 
    for c_nz_minutes in range(start, end, -1):
        if activity_count[player][c_nz_minutes-1]!=0:
            return c_nz_minutes-1
        
    return -1
	
	
# Functions for calculating first 15 min of mean of position data of each player. By that way we'll be able to separately calculate each half mean pos data.	
def fist_time_step_mean_data(half, data_persec_t):
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
            
            for player_home in range(0, len(home_team_player)):
                home_pos_count_minutes[player_home][0] = (shift(home_pos_count_minutes[player_home][0], -1, cval=0))
                home_pos_count_minutes[player_home][1] = (shift(home_pos_count_minutes[player_home][1], -1, cval=0))
                home_activity_count_minutes[player_home] = (shift(home_activity_count_minutes[player_home], -1, cval=0))
                
            for player_away in range(0, len(away_team_player)):
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
	
	
with open('../data/general/matches_2017_2018_v1.json') as matches_json:
    matches = json.load(matches_json)
    

    
minutes_step = 15
threshold_second = 60
data_height = 6000 # number of seconds in per match
data_width = 128 # number of features for fector

matches_d = [60834]

for id in matches_d:
   
    
    #id = int(match_data['id'])


    print('\n')
    print("Match id:" + str(id))


    # defining 3 distinct id in game
    referee_id = 0
    home_team_id = 139#int(match_data['homeId']) 
    away_team_id = 20004#int(match_data['awayId']) 


    # home and away player list
    home_team_player = []
    home_goal_keeper = []
    away_team_player = []
    away_goal_keeper = []


    # home_nonzero
    home_player_count_pitch = []
    home_prev_count = 11

    # home_nonzero
    away_player_count_pitch = []
    away_prev_count = 11

    # player dicts
    home_dict = {} 
    away_dict = {} 

    # players position ID 
    player_positionId = {'homeTeam' : {}, 'awayTeam' : {}}


    with open('../data/match_' + str(id) + '/roster_data_' + str(id) + '.json', 'r') as file:
        match_squad = json.load(file)

    for roaster in match_squad:
        if roaster['teamId'] == home_team_id:
            home_team_player.append(str(roaster['jerseyNumber']))
            player_positionId['homeTeam'][roaster['jerseyNumber']] = roaster['positionId'] 
            if roaster['positionId'] == 1:
                home_goal_keeper.append(str(roaster['jerseyNumber']))


        elif roaster['teamId'] == away_team_id:
            away_team_player.append(str(roaster['jerseyNumber']))
            player_positionId['awayTeam'][roaster['jerseyNumber']] = roaster['positionId']
            if roaster['positionId'] == 1:
                away_goal_keeper.append(str(roaster['jerseyNumber']))


    # home players dict data
    home_team_player.sort(key=int)
    home_goal_keeper.sort(key=int)
    home_val = np.arange(0, len(home_team_player))
    home_dict = dict(zip(home_team_player, home_val))
    home_dict_reverse = dict(zip(home_val, home_team_player))

    # away players dict data
    away_team_player.sort(key=int)
    away_goal_keeper.sort(key=int)
    away_val = np.arange(0, len(away_team_player))
    away_dict = dict(zip(away_team_player, away_val))
    away_dict_reverse = dict(zip(away_val, away_team_player))



    # home and away team players' status[0: not playing, 1: playing, 2-left the game], enter status[0: enter 1st half, 1: enter second half],
    # enter time, and duration, red card
    home_dur_in_out = np.zeros(shape=(len(home_team_player), 5), dtype=np.float)
    away_dur_in_out = np.zeros(shape=(len(away_team_player), 5), dtype=np.float)


    with open('../data/match_' + str(id) + '/players_data_' + str(id) + '.json', 'r') as file:
        player_data = json.load(file)


    for player in player_data:
        jersey_number = player['jerseyNumber']
        if player['teamId'] == home_team_id:
            home_dur_in_out[home_dict[str(jersey_number)]][3] = player['duration']
            home_dur_in_out[home_dict[str(jersey_number)]][4] = player['redCard']



        elif player['teamId'] == away_team_id:
            away_dur_in_out[away_dict[str(jersey_number)]][3] = player['duration']
            away_dur_in_out[away_dict[str(jersey_number)]][4] = player['redCard']



    # home and away team player pos and activity count: 0-xpos, 1-ypos
    home_pos_count = np.zeros(shape=(len(home_team_player), 2), dtype=np.float)
    home_activity_count = np.zeros(shape=(len(home_team_player), 1), dtype=np.int)
    home_activity_count_all = np.zeros(shape=(len(home_team_player), 2), dtype=np.int)
    home_act_nozero = [0,0] # number non-zero activity_count_all


    away_pos_count = np.zeros(shape=(len(away_team_player), 2), dtype=np.float)
    away_activity_count = np.zeros(shape=(len(away_team_player), 1), dtype=np.int)
    away_activity_count_all = np.zeros(shape=(len(away_team_player), 2), dtype=np.int)
    away_act_nozero = [0,0] # number non-zero activity_count_all


    # home and away team player count data for 10 min: 0-xpos, 1-ypos / 0-1min, 1-2min... 9-10min 
    home_pos_count_minutes = np.zeros(shape=(len(home_team_player), 2, minutes_step), dtype=np.float)
    home_activity_count_minutes = np.zeros(shape=(len(home_team_player), minutes_step), dtype=np.int)

    home_pos_count_minutes2 = np.zeros(shape=(len(home_team_player), 2, minutes_step), dtype=np.float)
    home_activity_count_minutes2 = np.zeros(shape=(len(home_team_player), minutes_step), dtype=np.int)

    away_pos_count_minutes = np.zeros(shape=(len(away_team_player), 2, minutes_step), dtype=np.float)
    away_activity_count_minutes = np.zeros(shape=(len(away_team_player), minutes_step), dtype=np.int)

    away_pos_count_minutes2 = np.zeros(shape=(len(away_team_player), 2, minutes_step), dtype=np.float)
    away_activity_count_minutes = np.zeros(shape=(len(away_team_player), minutes_step), dtype=np.int)


    # home and away team Mean pos data: 0-xpos, 1-ypos
    home_pos_mean = np.zeros(shape=(len(home_team_player), 2), dtype=np.float)
    away_pos_mean = np.zeros(shape=(len(away_team_player), 2), dtype=np.float)


    # create array of x input data for every match
    x_intput = np.ndarray(shape=(data_height, data_width), dtype=np.float)



    with open('../data/match_' + str(id) + '/per_sec_data_' + str(id) + '.json', 'r') as file:
        data_persec = json.load(file)




    home_pos_count_minutes = np.zeros(shape=(len(home_team_player), 2, minutes_step), dtype=np.float)
    home_activity_count_minutes = np.zeros(shape=(len(home_team_player), minutes_step), dtype=np.int)

    away_pos_count_minutes = np.zeros(shape=(len(away_team_player), 2, minutes_step), dtype=np.float)
    away_activity_count_minutes = np.zeros(shape=(len(away_team_player), minutes_step), dtype=np.int)

    # create first average positon data for assigning player position at the 1st half
    # temporary t    

    tmp_t = 0
    shift_times_right = 0

    # 1st half duration
    first_half_duration = 0

    home_nonzero = 11
    away_nonzero = 11

    prev_home_nonzero = 11
    prev_away_nonzero = 11


    # temporary half
    tmp_half = 1

    c_activity_value = 0
    c_home_activity_each = 0
    c_away_activity_each = 0

    while c_activity_value==0:

        c_home_activity_each = 0
        c_away_activity_each = 0



        a,b = fist_time_step_mean_data(1, data_persec)


        for player_home in range(0, len(home_team_player)):
            res = caluclate_activity_count(minutes_step, player_home, a)
            c_home_activity_each += res

        for player_away in range(0, len(away_team_player)):
            res = caluclate_activity_count(minutes_step, player_away, b)
            c_away_activity_each += res

        if c_home_activity_each == 11 and c_away_activity_each == 11:
            c_activity_value = 1

        threshold_second += 60  

    threshold_second -= 1




    for d in data_persec:

        match_half_t = int(d['half'])

        # create first average positon data for assigning player at the 2nd half
        if match_half_t != tmp_half and match_half_t==2:
            tmp_half = match_half_t
            shift_times_right = 0

            tmp_t = 45*60

            activity_home_nonzero = 0
            activity_away_nonzero = 0
            home_break_subs = []
            away_break_subs = []
            home_break_subs_after = []
            away_break_subs_after = []

            for player_home in range(0, len(home_team_player)):
                if home_pos_mean[player_home][0] !=0:
                        activity_home_nonzero += 1
                        home_break_subs.append(1)
                else:
                    home_break_subs.append(0)


            for player_away in range(0, len(away_team_player)):
                if away_pos_mean[player_away][0] !=0:
                        activity_away_nonzero += 1
                        away_break_subs.append(1)
                else:
                    away_break_subs.append(0)

            home_nonzero = activity_home_nonzero
            away_nonzero = activity_away_nonzero


            # clear home team data
            home_pos_count[0: len(home_team_player)] = 0
            home_activity_count[0: len(home_team_player)] = 0 
            home_activity_count_all[0: len(home_team_player)] = 0
            home_act_nozero = [0,0]
            home_pos_count_minutes[0: len(home_team_player)] = 0
            home_activity_count_minutes[0: len(home_team_player)] = 0
            home_pos_mean[0: len(home_team_player)] = 0

            # clear away team data
            away_pos_count[0: len(away_team_player)] = 0
            away_activity_count[0: len(away_team_player)] = 0 
            away_activity_count_all[0: len(away_team_player)] = 0
            away_act_nozero = [0,0]
            away_pos_count_minutes[0: len(away_team_player)] = 0
            away_activity_count_minutes[0: len(away_team_player)] = 0
            away_pos_mean[0: len(away_team_player)] = 0


            threshold_second = 60

            c_activity_value = 0
            c_home_activity_each = 0
            c_away_activity_each = 0

            while c_activity_value==0:

                c_home_activity_each = 0
                c_away_activity_each = 0

                home_break_subs_after = []
                away_break_subs_after = []

                a,b = fist_time_step_mean_data(2, data_persec)

                for player_home in range(0, len(home_team_player)):
                    res = caluclate_activity_count(minutes_step, player_home, a)
                    c_home_activity_each += res
                    home_break_subs_after.append(res)

                for player_away in range(0, len(away_team_player)):
                    res = caluclate_activity_count(minutes_step, player_away, b)
                    c_away_activity_each += res
                    away_break_subs_after.append(res)


                if c_home_activity_each == activity_home_nonzero and c_away_activity_each == activity_away_nonzero:
                    c_activity_value = 1

                threshold_second += 60


            for player_home_2 in range(0, len(home_team_player)):
                if home_break_subs_after[player_home_2]==0 and home_break_subs[player_home_2]==1:
                    home_dur_in_out[player_home_2][0] = 2 # menas goal keepr has left the game

            for player_away_2 in range(0, len(away_team_player)):
                if away_break_subs_after[player_away_2]==0 and away_break_subs[player_away_2]==1:
                    away_dur_in_out[player_away_2][0] = 2 # menas goal keepr has left the game

            threshold_second -= 1


        i = int(d['minute'])*60 + int(d['second'])
        x_pos = d['xpos']
        y_pos = d['ypos']
        team_id_t = int(d['teamId'])
        jersey_number_t = int(d['jerseyNumber'])
        has_ball_teamId_t = int(d['hasballTeamId'])


        # find out how long did 1st half last
        if match_half_t == 1:
            first_half_duration = i


        if i%60==59:

            if team_id_t == home_team_id:
                player = home_dict[str(jersey_number_t)]
                home_activity_count_all[player][1] = 1

            elif team_id_t == away_team_id:
                player = away_dict[str(jersey_number_t)]
                away_activity_count_all[player][1] = 1



        if i%60!=0:    

            if team_id_t == home_team_id:

                if home_dur_in_out[home_dict[str(jersey_number_t)]][0] == 0:
                    home_dur_in_out[home_dict[str(jersey_number_t)]][0] = 1 # indicates that a player is in game 
                    home_dur_in_out[home_dict[str(jersey_number_t)]][1] = match_half_t # enter half
                    home_dur_in_out[home_dict[str(jersey_number_t)]][2] = i  # enter time


                    plyr_position = player_positionId['homeTeam'][jersey_number_t]
                    player = home_dict[str(jersey_number_t)]
                    home_pos_count_minutes[player][1][minutes_step-1] += 34
                    home_activity_count_minutes[player][minutes_step-1] +=1


                    if plyr_position == 1:
                        home_pos_count_minutes[player][0][minutes_step-1] += 10
                    elif plyr_position == 2:
                        home_pos_count_minutes[player][0][minutes_step-1] += 38
                    elif plyr_position == 3:
                        home_pos_count_minutes[player][0][minutes_step-1] += 58
                    else:
                        home_pos_count_minutes[player][0][minutes_step-1] += 78

                if i<((home_dur_in_out[home_dict[str(jersey_number_t)]][2])+60) and home_dur_in_out[home_dict[str(jersey_number_t)]][0] == 1:
                    if x_pos!=0 and y_pos!=0:
                        home_pos_count[home_dict[str(jersey_number_t)]][0] += x_pos
                        home_pos_count[home_dict[str(jersey_number_t)]][1] += y_pos
                        home_activity_count[home_dict[str(jersey_number_t)]] +=1 

                elif player_positionId['homeTeam'][jersey_number_t] == 1 and has_ball_teamId_t != 0:
                    if x_pos!=0 and y_pos!=0:
                        home_pos_count[home_dict[str(jersey_number_t)]][0] += x_pos
                        home_pos_count[home_dict[str(jersey_number_t)]][1] += y_pos
                        home_activity_count[home_dict[str(jersey_number_t)]] +=1

                elif has_ball_teamId_t == away_team_id:
                    if x_pos!=0 and y_pos!=0:
                        home_pos_count[home_dict[str(jersey_number_t)]][0] += x_pos
                        home_pos_count[home_dict[str(jersey_number_t)]][1] += y_pos
                        home_activity_count[home_dict[str(jersey_number_t)]] +=1 

            elif team_id_t == away_team_id:

                if away_dur_in_out[away_dict[str(jersey_number_t)]][0] == 0:
                    away_dur_in_out[away_dict[str(jersey_number_t)]][0] = 1 # indicates that a player is in game
                    away_dur_in_out[away_dict[str(jersey_number_t)]][1] = match_half_t # enter half 
                    away_dur_in_out[away_dict[str(jersey_number_t)]][2] = i #enter time

                    plyr_position = player_positionId['awayTeam'][jersey_number_t]
                    player = away_dict[str(jersey_number_t)]
                    away_pos_count_minutes[player][1][minutes_step-1] += 34
                    away_activity_count_minutes[player][minutes_step-1] +=1


                    if plyr_position == 1:
                        away_pos_count_minutes[player][0][minutes_step-1] += 10
                    elif plyr_position == 2:
                        away_pos_count_minutes[player][0][minutes_step-1] += 38
                    elif plyr_position == 3:
                        away_pos_count_minutes[player][0][minutes_step-1] += 58
                    else:
                        away_pos_count_minutes[player][0][minutes_step-1] += 78


                if i<((away_dur_in_out[away_dict[str(jersey_number_t)]][2])+60) and away_dur_in_out[away_dict[str(jersey_number_t)]][0] == 1:
                    if x_pos!=0 and y_pos!=0:
                        away_pos_count[away_dict[str(jersey_number_t)]][0] += x_pos
                        away_pos_count[away_dict[str(jersey_number_t)]][1] += y_pos
                        away_activity_count[away_dict[str(jersey_number_t)]] +=1

                elif player_positionId['awayTeam'][jersey_number_t] == 1 and has_ball_teamId_t != 0:
                    away_pos_count[away_dict[str(jersey_number_t)]][0] += x_pos
                    away_pos_count[away_dict[str(jersey_number_t)]][1] += y_pos
                    away_activity_count[away_dict[str(jersey_number_t)]] +=1

                elif has_ball_teamId_t == home_team_id:
                     if x_pos!=0 and y_pos!=0:
                        away_pos_count[away_dict[str(jersey_number_t)]][0] += x_pos
                        away_pos_count[away_dict[str(jersey_number_t)]][1] += y_pos
                        away_activity_count[away_dict[str(jersey_number_t)]] +=1 

            elif team_id_t == referee_id:
                pass
                # referee_pos_t['xpos']
                # referee_pos_t['ypos']





        # shifing last index of 15min arry (period of 15min) with last min data
        # and calculate mena position of each player each min based on previus 10 min
        if i%60 == 0 and tmp_t != i+1 and (i-(match_half_t-1)*45*60)>threshold_second:
            
            
         


            tmp_t = i+1

            prev_home_nonzero = home_nonzero
            home_nonzero = 0

            prev_away_nonzero = away_nonzero
            away_nonzero = 0


            if shift_times_right !=0:
                for player_home in range(0, len(home_team_player)):

                    home_pos_count_minutes[player_home][0] = (shift(home_pos_count_minutes[player_home][0], -1, cval=0))
                    home_pos_count_minutes[player_home][1] = (shift(home_pos_count_minutes[player_home][1], -1, cval=0))
                    home_activity_count_minutes[player_home] = (shift(home_activity_count_minutes[player_home], -1, cval=0))

                    home_pos_count_minutes[player_home][0][minutes_step-1] = home_pos_count[player_home][0]
                    home_pos_count_minutes[player_home][1][minutes_step-1] = home_pos_count[player_home][1]
                    home_activity_count_minutes[player_home][minutes_step-1] = home_activity_count[player_home]


                for player_away in range(0, len(away_team_player)):

                    away_pos_count_minutes[player_away][0] = (shift(away_pos_count_minutes[player_away][0], -1, cval=0))
                    away_pos_count_minutes[player_away][1] = (shift(away_pos_count_minutes[player_away][1], -1, cval=0))
                    away_activity_count_minutes[player_away] = (shift(away_activity_count_minutes[player_away], -1, cval=0))

                    away_pos_count_minutes[player_away][0][minutes_step-1] = away_pos_count[player_away][0]
                    away_pos_count_minutes[player_away][1][minutes_step-1] = away_pos_count[player_away][1]
                    away_activity_count_minutes[player_away][minutes_step-1] = away_activity_count[player_away]


            shift_times_right = 1


            # clear home team
            home_pos_count[0: len(home_team_player)] = 0
            home_activity_count[0: len(home_team_player)] = 0

            # clear away team
            away_pos_count[0: len(away_team_player)] = 0
            away_activity_count[0: len(away_team_player)] = 0


            home_pos_mean[0:len(home_team_player)] = 0
            home_act_nozero = [0,0]

            away_pos_mean[0:len(away_team_player)] = 0
            away_act_nozero = [0,0]



            for player_home in range(0, len(home_team_player)):
                jersey_n = int(home_dict_reverse[player_home])
                if player_positionId['homeTeam'][jersey_n] == 1 and home_dur_in_out[player_home][0]==1 and home_activity_count_all[player_home][1] == 0:
                    action_status_exit = 0
                    for gk_i in home_goal_keeper:
                        if home_activity_count_all[home_dict[str(gk_i)]][1] !=0:
                            home_dur_in_out[player_home][0] = 2 # menas goal keepr has left the game
                            home_pos_mean[player_home][0] = 0 
                            home_pos_mean[player_home][1] = 0
                            action_status_exit = 1

                    if action_status_exit == 0:
                        home_activity_count_all[player_home][1] = 1

                if (home_activity_count_all[player_home][0]==1):
                    home_act_nozero[0] += 1

                if (home_activity_count_all[player_home][1]==1):
                    home_act_nozero[1] += 1




            for player_away in range(0, len(away_team_player)):
                jersey_n = int(away_dict_reverse[player_away])
                if player_positionId['awayTeam'][jersey_n] == 1 and away_dur_in_out[player_away][0]==1 and away_activity_count_all[player_away][1] == 0:
                    action_status_exit = 0
                    for gk_i in away_goal_keeper:
                        if away_activity_count_all[away_dict[str(gk_i)]][1] !=0:
                            away_dur_in_out[player_away][0] = 2 # menas goal keepr has left the game
                            away_pos_mean[player_away][0] = 0 
                            away_pos_mean[player_away][1] = 0
                            action_status_exit = 1

                    if action_status_exit == 0:
                        away_activity_count_all[player_away][1] = 1


                if (away_activity_count_all[player_away][0]!=0):
                    away_act_nozero[0] += 1

                if (away_activity_count_all[player_away][1]!=0):
                    away_act_nozero[1] += 1
                    
                    
#             if i/60>=68 and i/60<74:
#                 print(i/60)
#                 print(away_activity_count_all)


            home_subs_count_check = 0
            home_subs_count_id = 0
            home_2subs_array_in = []
            home_2subs_array_out = []

            for player_home in range(0, len(home_team_player)):

                if home_activity_count_all[player_home][1] != 0 and home_dur_in_out[player_home][0]==1:
                    caluclate_avrg_pos(minutes_step, home_pos_mean, player_home, home_pos_count_minutes, 
                                       home_activity_count_minutes)


                elif home_activity_count_all[player_home][1] == 0 and home_dur_in_out[player_home][0]==1 and home_dur_in_out[player_home][4]==1: 
                    # player current and whole game duration durng match


                    enter_half = home_dur_in_out[player_home][1]
                    enter_time = home_dur_in_out[player_home][2]
                    p_game_play_dur = home_dur_in_out[player_home][3]

                    h = match_half_t
                    f_h_d= first_half_duration

                    if enter_half == 1:
                        current_play_dur = math.floor( ((f_h_d - enter_time) + (i-45*60)*(h-1) )/60 )
                    elif enter_half == 2:
                        current_play_dur = math.floor( (i - enter_time)/60 )



                    if current_play_dur < p_game_play_dur:
                        caluclate_avrg_pos(minutes_step, home_pos_mean, player_home, home_pos_count_minutes, 
                                       home_activity_count_minutes)
                        home_activity_count_all[player_home][1] = 1
                    else:
                        home_dur_in_out[player_home][0] = 2
                        home_pos_mean[player_home][0] = 0 
                        home_pos_mean[player_home][1] = 0




                elif home_activity_count_all[player_home][1] == 0 and home_dur_in_out[player_home][0]==1 and home_dur_in_out[player_home][4]!=1:

                    if (home_act_nozero[0] == home_act_nozero[1]):
                        home_dur_in_out[player_home][0]=2
                        home_pos_mean[player_home][0] = 0 
                        home_pos_mean[player_home][1] = 0




                    elif home_act_nozero[0] > home_act_nozero[1]:
                        caluclate_avrg_pos(minutes_step, home_pos_mean, player_home, home_pos_count_minutes, 
                                       home_activity_count_minutes)
                        home_activity_count_all[player_home][1] = 1
                        home_subs_count_check += 1
                        home_2subs_array_out.append(player_home)
                        home_subs_count_id = player_home

                else:

                    home_pos_mean[player_home][0] = 0 
                    home_pos_mean[player_home][1] = 0


            for player_home in range(0, len(home_team_player)):
                if home_subs_count_check >=1 and (home_act_nozero[0]-home_act_nozero[1]==1):

                    d = caluclate_nzero_activity_count(minutes_step, 0, home_subs_count_id, home_activity_count_minutes)
                    if home_activity_count_all[player_home][0] == 0 and home_activity_count_all[player_home][1] == 1:
                        result = caluclate_nzero_activity_count(minutes_step, d+1, player_home, home_activity_count_minutes)
                        if result != -1:
                            home_2subs_array_in.append(player_home)

                home_activity_count_all[player_home][0] = home_activity_count_all[player_home][1]
                home_activity_count_all[player_home][1] = 0



            # number of last non-zero activties
            home_last_nz_act_count = caluclate_last_nzero_ac_count(len(home_team_player), home_activity_count_all)



            if home_last_nz_act_count == prev_home_nonzero and len(home_2subs_array_out)==2:
                for home_2subs_i in range(0,2):
                    player = home_2subs_array_out[home_2subs_i]
                    if home_activity_count_minutes[player][minutes_step-1] == 0:
                        home_dur_in_out[player][0] = 2
                        home_activity_count_all[player][0] = 0
                        home_pos_mean[player][0] = 0
                        home_pos_mean[player][1] = 0


            if len(home_2subs_array_out)>=2:
                for home_2subs_i in range(0,2):
                    player = home_2subs_array_out[home_2subs_i]
                    home_activity_count_all[player][0] = 1
                    caluclate_avrg_pos(minutes_step, home_pos_mean, player_home, home_pos_count_minutes, 
                                       home_activity_count_minutes)


            if len(home_2subs_array_in) == 2 and len(home_2subs_array_out)==2:
                for home_2subs_i in range(0,2):
                    player = home_2subs_array_out[home_2subs_i]
                    home_dur_in_out[player][0] = 2
                    home_activity_count_all[player][0] = 0
                    home_pos_mean[player][0] = 0
                    home_pos_mean[player][1] = 0

            if len(home_2subs_array_in) == 1 and len(home_2subs_array_out)>=2:
                player = home_2subs_array_in[0]
                home_activity_count_all[player][0] = 0
                home_pos_mean[player][0] = 0
                home_pos_mean[player][1] = 0
                
                
            if home_act_nozero[0]-home_act_nozero[1]==1 and home_subs_count_check==1 and len(home_2subs_array_in) == 1:
                player_out = home_2subs_array_out[0]
                home_dur_in_out[player_out][0] = 2
                home_activity_count_all[player_out][0] = 0
                home_pos_mean[player_out][0] = 0
                home_pos_mean[player_out][1] = 0




            for player_home in range(0, len(home_team_player)):
                if home_pos_mean[player_home][0] !=0:
                    home_nonzero += 1


#                 jersey_n = home_dict_reverse[player_home]
#                 if player_positionId['homeTeam'][int(jersey_n)] == 1:
#                     pass
#                 elif home_pos_mean[player_home][0]!=0 and home_pos_mean[player_home][1]!=0:
#                     plt.scatter(home_pos_mean[player_home][0], home_pos_mean[player_home][1], marker="o", color="k", linewidths=0.5)


            away_subs_count_check = 0
            away_subs_count_id = 0
            away_2subs_array_in = []
            away_2subs_array_out = []

            for player_away in range(0, len(away_team_player)):


                if away_activity_count_all[player_away][1] != 0 and away_dur_in_out[player_away][0]==1:
                    caluclate_avrg_pos(minutes_step, away_pos_mean, player_away, away_pos_count_minutes, 
                                       away_activity_count_minutes)

                elif away_activity_count_all[player_away][1] == 0 and away_dur_in_out[player_away][0]==1 and away_dur_in_out[player_away][4]==1:


                    # player current and whole game duration durng match
                    enter_half = away_dur_in_out[player_away][1]
                    enter_time = away_dur_in_out[player_away][2]
                    p_game_play_dur = away_dur_in_out[player_away][3]

                    h = match_half_t
                    f_h_d= first_half_duration



                    if enter_half == 1:
                        current_play_dur = math.floor( ((f_h_d - enter_time) + (i-45*60)*(h-1) )/60 )
                    elif enter_half == 2:
                        current_play_dur = math.floor( (i - enter_time)/60 )



                    if current_play_dur < p_game_play_dur:
                        caluclate_avrg_pos(minutes_step, away_pos_mean, player_away, away_pos_count_minutes, 
                                       away_activity_count_minutes)
                        away_activity_count_all[player_away][1] = 1

                    else:
                        away_dur_in_out[player_away][0] = 2
                        away_pos_mean[player_away][0] = 0 
                        away_pos_mean[player_away][1] = 0


                elif away_activity_count_all[player_away][1] == 0 and away_dur_in_out[player_away][0]==1:

                    if away_act_nozero[0] == away_act_nozero[1]:
                        away_dur_in_out[player_away][0] = 2
                        away_pos_mean[player_away][0] = 0 
                        away_pos_mean[player_away][1] = 0


                    elif (away_act_nozero[0] > away_act_nozero[1]):
                        caluclate_avrg_pos(minutes_step, away_pos_mean, player_away, away_pos_count_minutes, 
                                       away_activity_count_minutes)
                        away_activity_count_all[player_away][1] = 1
                        away_subs_count_check += 1
                        away_2subs_array_out.append(player_away)
                        away_subs_count_id = player_away

                else:
                    away_pos_mean[player_away][0] = 0 
                    away_pos_mean[player_away][1] = 0



            for player_away in range(0, len(away_team_player)):
                if away_subs_count_check >= 1 and (away_act_nozero[0]-away_act_nozero[1]==1):
                        d = caluclate_nzero_activity_count(minutes_step, 0, away_subs_count_id, away_activity_count_minutes)
                        if away_activity_count_all[player_away][0] ==0 and away_activity_count_all[player_away][1] == 1:
                            result = caluclate_nzero_activity_count(minutes_step, d+1, player_away, away_activity_count_minutes)
                            if result != -1:
                                away_2subs_array_in.append(player_away)

                away_activity_count_all[player_away][0] = away_activity_count_all[player_away][1]
                away_activity_count_all[player_away][1] = 0
                
                
            # number of last non-zero activties
            away_last_nz_act_count = caluclate_last_nzero_ac_count(len(away_team_player), away_activity_count_all)


            if away_last_nz_act_count == prev_away_nonzero and len(away_2subs_array_out)==2:
                for away_2subs_i in range(0,2):
                    player = away_2subs_array_out[away_2subs_i]
                    if away_activity_count_minutes[player][minutes_step-1] == 0:
                        away_dur_in_out[player][0] = 2
                        away_activity_count_all[player][0] = 0
                        away_pos_mean[player][0] = 0
                        away_pos_mean[player][1] = 0


            if len(away_2subs_array_out)>=2:
                for away_2subs_i in range(0,2):
                    player = away_2subs_array_out[away_2subs_i]
                    away_activity_count_all[player][0] = 1

            if len(away_2subs_array_in) == 2 and away_subs_count_check==2:
                for away_2subs_i in range(0,2):
                    player = away_2subs_array_out[away_2subs_i]
                    away_dur_in_out[player][0] = 2
                    away_activity_count_all[player][0] = 0
                    away_pos_mean[player][0] = 0
                    away_pos_mean[player][1] = 0

            if len(away_2subs_array_in) == 1 and away_subs_count_check>=2:
                player = away_2subs_array_in[0]
                away_activity_count_all[player][0] = 0
                away_pos_mean[player][0] = 0
                away_pos_mean[player][1] = 0
                
            if away_act_nozero[0]-away_act_nozero[1]==1 and away_subs_count_check==1 and len(away_2subs_array_in) == 1:
                player_out = away_2subs_array_out[0]
                away_dur_in_out[player_out][0] = 2
                away_activity_count_all[player_out][0] = 0
                away_pos_mean[player_out][0] = 0
                away_pos_mean[player_out][1] = 0


            for player_away in range(0, len(away_team_player)):
                if away_pos_mean[player_away][0] !=0:
                    away_nonzero += 1


#                 jersey_n = away_dict_reverse[player_away]
#                 if player_positionId['awayTeam'][int(jersey_n)] == 1:
#                     pass
#                 elif away_pos_mean[player_away][0]!=0 and away_pos_mean[player_away][1]!=0:
#                     plt.scatter(away_pos_mean[player_away][0], away_pos_mean[player_away][1], marker="o", color="r", linewidths=0.5)




            if home_nonzero != home_prev_count:
                home_player_count_pitch.append(str("half:") + str(match_half_t) +" min:" + str((i)/60) + " number: " + str(home_nonzero))
                home_prev_count = home_nonzero

            if away_nonzero != away_prev_count:
                away_player_count_pitch.append(str("half:") + str(match_half_t) +" min:" + str((i)/60) + " number: " + str(away_nonzero))
                away_prev_count = away_nonzero

#             print("half:" + str(match_half_t) +"\tmin: " + str((i)/60))
#             plt.show()
#             print('\n')        

    print(home_player_count_pitch)
    print(away_player_count_pitch)


