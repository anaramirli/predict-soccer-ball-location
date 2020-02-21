import math
import numpy as np

class PlayersRoleSet(object):
    
    # constants
    segment_values = {'x':{'start':3, 'end':102}, 'y':{'start':0, 'end':68}} # segment start and end: used in scaling
    
    # default vars
    role_segment_coords = {'LB':[-1,  40, -1, 19],    # Left Back 
                          'CB':[-1,  35,  19, 49],   # Center Back
                          'RB':[-1,  40,  49, 69],   # Right Back
                          'LW':[ 40, 106, -1, 19],  # Left Winger
                          'CM':[ 35,  75,  19, 49],  # Center Midfielder  
                          'RW':[ 40, 106,  49, 69], # Right Winger
                          'CF':[ 75, 106,  19, 49]}  # Center Forward/Attacking Middle

    def get_role_segment_coords(self):
        
        '''
        Get players role list
        
        '''

        return self.role_segment_coords
    
    def set_role_segment_coords(self, role_segment_coords):
        
        '''
        Set players role list
        
        '''
        
        if(type(role_segment_coords)!=dict):
            assert False, "variable must be dictionary, instead it found to be type of {}".format(type(role_segment_coords))
        else:
            self.role_segment_coords = role_segment_coords
    
                
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
    
    
    
    def find_segments(self, x, y):
        
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

        for role, segment in self.role_segment_coords.items():
            if (x>=segment[0] and x<=segment[1] and y>=segment[2] and y<=segment[3]):
                return role
            
        return None
    
    def get_scaled_values(self, dataModel, posCounIndex):
        
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
                return self.find_segments(player_tmp_x, player_tmp_y)

        else:
            return None