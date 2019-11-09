import math
import numpy as np
from scipy.ndimage.interpolation import shift

class DataModel(object):
    
    # CONSTANTS
    referee_id = 0
    role_segment_coord = {'LB':[-1,  40, -1, 19],    # Left Back 
                          'CB':[-1,  35,  19, 49],   # Center Back
                          'RB':[-1,  40,  49, 69],   # Right Back
                          'LW':[ 40, 106, -1, 19],  # Left Winger
                          'CM':[ 35,  75,  19, 49],  # Center Midfielder  
                          'RW':[ 40, 106,  49, 69], # Right Winger
                          'CF':[ 75, 106,  19, 49]}  # Center Forward/Attacking Middle
   
    
    segment_values = {'x':{'start':7, 'end':98}, 'y':{'start':0, 'end':68}} # segment start and end used in scaling

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
                
      
    def get_role_list(self):
        
        '''
        Get players role list
        
        '''

        return list(self.role_segment_coord.keys())
    
                
    def scale_linear_data(self, value, max_v, min_v, std_v, segment_start, segment_end):
        
        '''
        Function for sclaing player avrg position to the to the range of (for x-axis: [105-std,0+std])

        Parameters
        ----------

        Output
        ------
        scaled value

        '''
        segment_end -= std_v
        segment_start += std_v
        
        return segment_end - (segment_end - segment_start) * (max_v - value) / (max_v - min_v)
    
    
    
    def assign_role(self, x, y):
        
        '''
        Function to define players role in the game
        Parameters
        ----------
        x, y: coordinates

        pitch_value: pitch segment value

        Returns
        -------
        role
        '''

        for role, segment in self.role_segment_coord.items():
            if (x>=segment[0] and x<=segment[1] and y>=segment[2] and y<=segment[3]):
                return role
            
        return None
    
    def get_scale_values(self, dataModel, posCounIndex):
        
        '''
        return scale values
        Paremeters
        ----------
        dataModel: pass model data
        posCounIndex: index start to check posCount array to find non zero activity 
        
        Output:
        scale_values: dict[home/away][x/y][0-max, 1-min, 2-mean]
        
        '''
        
        
        scale_array = {'away':{'x':[], 'y':[]}, 'home':{'x':[], 'y':[]}}
        
        # calculate 
        for team, _ in dataModel.player_data.items():
            for ID, playerData in dataModel.player_data[team].items():
                if playerData['posCount'][posCounIndex]!=0 and np.sum(playerData['rolePosCount'])!=0:
                    player_tmp_x = np.sum(playerData['rolePosCountTmsX'])/np.sum(playerData['rolePosCount'])
                    player_tmp_y = np.sum(playerData['rolePosCountTmsY'])/np.sum(playerData['rolePosCount'])
                    
                    # swap direction of away team x-axis / we calculate roles in one direction
                    if team == 'away': player_tmp_x=105-player_tmp_x

                    if playerData['position']!=1:
                        scale_array[team]['x'].append(player_tmp_x)
                        scale_array[team]['y'].append(player_tmp_y)

        # output 
        # order: max, mena, std          
        scale_values = {'home':{'x':[], 'y':[]}, 'away':{'x':[], 'y':[]}}

        for team_label in ['home', 'away']:
            
            try:
                for axis_label in ['x', 'y']:
                    scale_values[team_label][axis_label].append(np.max(scale_array[team_label][axis_label]))
                    scale_values[team_label][axis_label].append(np.min(scale_array[team_label][axis_label]))
                    scale_values[team_label][axis_label].append(np.std(scale_array[team_label][axis_label]))
                    
            except (ValueError):
                raise ValueError

        return scale_values
    
    
    
    def set_role(self, playerdata, scale_values, posCounIndex, team):
        
        '''
        Seting role to each player based on given role segment
        
        Paremeters
        ----------
       
        playerdata: dataModel['team']['id'] / stores players positional informations
        posCounIndex: index start to check posCount array to find non zero activity
        scale_values: dict[home/away][x/y][0-max, 1-min, 2-std] / dict array stores min, max, std of average position
        team: team label / home or away
        
        Outputs
        -------
        return role 1-to rolesize or None 
        
        '''
        
        # set role to player if sum of rolePosCount and last min count of posCount is equal is nonzero
        if playerdata['posCount'][posCounIndex]!=0 and np.sum(playerdata['rolePosCount'])!=0:
            
            player_tmp_x = np.sum(playerdata['rolePosCountTmsX'])/np.sum(playerdata['rolePosCount'])
            player_tmp_y = np.sum(playerdata['rolePosCountTmsY'])/np.sum(playerdata['rolePosCount'])

            # swap direction of away team x-axis (we calculate roles in one direction)
            if team == 'away': player_tmp_x=105-player_tmp_x

            # if goalkeepr the set role role directly/ goalkeepr is not included in role assignment
            if playerdata['position']==1:
                return 'GK'
            else:
                # scale average positions
                player_tmp_x = self.scale_linear_data(value=player_tmp_x, 
                                                 max_v=scale_values[team]['x'][0], # max
                                                 min_v=scale_values[team]['x'][1], # min
                                                 std_v=scale_values[team]['x'][2], # std
                                                 segment_start=self.segment_values['x']['start'], # start of segment of x-axis
                                                 segment_end=self.segment_values['x']['end']) # end of segment of x-axis

                player_tmp_y = self.scale_linear_data(value=player_tmp_y, 
                                                 max_v=scale_values[team]['y'][0], 
                                                 min_v=scale_values[team]['y'][1], 
                                                 std_v=scale_values[team]['y'][2], 
                                                 segment_start=self.segment_values['y']['start'],
                                                 segment_end=self.segment_values['y']['end'])
                # assign role to scaled positions
                return self.assign_role(player_tmp_x, player_tmp_y)

        else:
            return None