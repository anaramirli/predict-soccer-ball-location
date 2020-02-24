import math
import numpy as np
from scipy.ndimage.interpolation import shift

class DataModel(object):
    
    # CONSTANTS
    referee_id = 0  
   
    # initialization
    def __init__(self, minutes_step=15):
        
        '''
        match_data = json list contains match info
        minutes_step = time window
        '''
        
        if (type(minutes_step)!=int):
            raise ValueError
            
        self.minutes_step = minutes_step
           
                     
    def init_players_info(self, match_data, match_squad_info, match_palyer_info):
        '''
        init and get players info
        match_squad_info: json list
        
        '''


        if (type(match_data)!=dict):
            raise TypeError

        # team id dictionary
        self.team_id_dict={int(match_data['homeId']):'home', int(match_data['awayId']):'away'}

        
        # PLAYER INFORMATION
        self.player_data = {'home':{}, 'away':{}}

        
        # get each player info
        # data dictionary
        for i_player_info in match_squad_info:
            
            try:                      
                team_label = self.team_id_dict[i_player_info['teamId']] # return home or away 
               
                self.player_data[team_label][i_player_info['jerseyNumber']] = {
                    'position': i_player_info['positionId'],  # 1 goalkeepr, 0 others
                    'role':None, # from 1 to role_size: players rolse assigment indexes. role_size+1: goalkeeper
                    'posCount': np.zeros(shape=(self.minutes_step),dtype=np.int16), # 1Xm_step arr: number of times player was on the pithc
                    'rolePosCount': np.zeros(shape=(self.minutes_step),dtype=np.int16), # 1Xm_step arr: times player was on the pithc 
                    'rolePosCountTmsX': np.zeros(shape=(self.minutes_step),dtype=np.float32), # 1Xm_step arr: pos count for role in x-axis
                    'rolePosCountTmsY': np.zeros(shape=(self.minutes_step),dtype=np.float32), # 1Xm_step arr: pos count for role in y-axis
                }

            except KeyError:
                continue
      
    def reset_positional_info(self):
        '''
        reset players positional frame informations
        
        Parameters
        ----------
        pass with reference
        
        '''
        for team, _ in self.player_data.items():
            for ID, _ in self.player_data[team].items():
                self.player_data[team][ID]['rolePosCountTmsX'] = np.zeros(shape=(self.minutes_step),dtype=np.float32)
                self.player_data[team][ID]['rolePosCountTmsY'] = np.zeros(shape=(self.minutes_step),dtype=np.float32)
                self.player_data[team][ID]['rolePosCount'] = np.zeros(shape=(self.minutes_step),dtype=np.int16)
                self.player_data[team][ID]['posCount'] = np.zeros(shape=(self.minutes_step),dtype=np.int16)
                self.player_data[team][ID]['role'] = None
                
                
    
    def shift_tms_data_right(self):
        '''
        shift previous timestep values to one step rihht
        
        Parameters
        ----------
        pass with reference
        '''
        for team, _ in self.player_data.items():
            for ID, _ in self.player_data[team].items():
                self.player_data[team][ID]['rolePosCountTmsX'] = shift(self.player_data[team][ID]['rolePosCountTmsX'], -1, cval=0.0)
                self.player_data[team][ID]['rolePosCountTmsY'] = shift(self.player_data[team][ID]['rolePosCountTmsY'], -1, cval=0.0)
                self.player_data[team][ID]['rolePosCount'] = shift(self.player_data[team][ID]['rolePosCount'], -1, cval=0)
                self.player_data[team][ID]['posCount'] = shift(self.player_data[team][ID]['posCount'], -1, cval=0)
                
                
       
    def add_player_activity(self, team_id, has_ball_teamId_t, jersey_number_t, x_pos, y_pos):
        '''
        That is used to get players to define their role. Therefor, players' data is colected when rival team has the ball. 
        '''
        
        x_pos = round(x_pos, 2)
        y_pos = round(y_pos, 2)
        
        try:
            team = self.team_id_dict[team_id]
        except KeyError:
            team=None

        try:
            ball_has_team = self.team_id_dict[has_ball_teamId_t]
        except KeyError:
            ball_has_team = None

        if team!=None and (x_pos!=0 or y_pos!=0) and (x_pos>-1 and y_pos>-1) and (x_pos<106 and y_pos<69):
            try:
                # calcualte activity count for players
                self.player_data[team][jersey_number_t]['posCount'][self.minutes_step-1] += 1

                # get ativity for role assignment: get position when rival has the ball,
                # if it's not a gooalkeeper: cuz there is no need to define goalkeeper role.
                if ball_has_team != team and ball_has_team!=None and self.player_data[team][jersey_number_t]['position'] != 1:
                    self.player_data[team][jersey_number_t]['rolePosCountTmsX'][self.minutes_step-1] += x_pos 
                    self.player_data[team][jersey_number_t]['rolePosCountTmsY'][self.minutes_step-1] += y_pos
                    self.player_data[team][jersey_number_t]['rolePosCount'][self.minutes_step-1] += 1
                elif self.player_data[team][jersey_number_t]['position'] == 1:
                    self.player_data[team][jersey_number_t]['rolePosCountTmsX'][self.minutes_step-1] += x_pos 
                    self.player_data[team][jersey_number_t]['rolePosCountTmsY'][self.minutes_step-1] += y_pos
                    self.player_data[team][jersey_number_t]['rolePosCount'][self.minutes_step-1] += 1
                  

            except:
                raise ('KeyError: player id/jesey number')

            
    def calculate_fist_time_step_data(self, data_persec, match_half, threshold_min):
        '''
        This function enables us separately calculate mean pos data at the begning of each half . 

        Parameters
        ----------
        half: half of match
        data_persec_t: raw data of match for per secdon
        threshold_min: 
        others pass with reference
        '''
        
        tmp_minunte_t=(match_half-1)*45
        threshold_min = tmp_minunte_t+threshold_min
        
        for data_t in data_persec:
            
            if data_t['half'] == match_half:
                
                if tmp_minunte_t==threshold_min:
                    break
                    
                if tmp_minunte_t != data_t['minute']:

                    tmp_minunte_t = data_t['minute']
                    # shif pervious timestep values to rigth 
                    self.shift_tms_data_right()
                    
                # get players data when rival owns the ball
                self.add_player_activity(data_t['teamId'], data_t['hasballTeamId'], data_t['jerseyNumber'], data_t['xpos'], data_t['ypos'])
