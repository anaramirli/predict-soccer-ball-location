import numpy as np
from classes.Utils import calculate_average, distance_2points, innerDBSCAN

class FeatureBuilder(object):
   
    # speed group features
    speedgroup = {
        
        'all_avrg_x':-1,
        'all_avrg_y':-1,
        'all_avrg_speed':-1,
        'all_avrg_direction_x':0,
        'all_avrg_direction_y':0,
        'all_inner_dis_to_avrg_pos':0,
        
        'slow_avrg_x':-1,
        'slow_avrg_y':-1,
        'slow_avrg_speed':-1,
        
        'hir_avrg_x':-1,
        'hir_avrg_y':-1,
        'hir_avrg_speed':-1,
        
        'sprint_avrg_x':-1,
        'sprint_avrg_y':-1,
        'sprint_avrg_speed':-1,
    }
    
    # teams features
    team = {
        
        'dbscan_avrg_x':-1,
        'dbscan_avrg_y':-1,
        'dbscan_avrg_speed':-1,
        'inner_dis_to_dbscan_pos':0,
               
        'gk_x':-1,
        'gk_y':-1,
        'gk_speed':-1,
        'gk_direction_x':0,
        'gk_direction_y':0,
        
        'min_x':-1,
        'min_x_speed':-1,
        'max_x':-1,
        'max_x_speed':-1,
        
        'min_y':-1,
        'min_y_speed':-1,
        'max_y':-1,
        'max_y_speed':-1,
        
        'min_speed':-1,
        'min_speed_x':-1,
        'min_speed_y':-1,
        
        'max_speed':-1,
        'max_speed_x':-1,
        'max_speed_y':-1
    
    }
    
    # both teams together features
    bothteams = {
        
        'avrg_x':-1,
        'avrg_y':-1,
        'avrg_speed':-1,
        'inner_dis_to_avrg_pos':0,
        'dbscan_avrg_x':-1,
        'dbscan_avrg_y':-1,
        'dbscan_avrg_speed':0,
        'inner_dis_to_dbscan_pos':0,
    
    }
   
    # referee features
    referee = {
        
        'x':-1,
        'y':-1,
        'speed':-1,
        'direction_x':0,
        'direction_y':0
    }
    
    
    def __init__(self, player_role_list):
        
        '''
            player_role_list: array storing roles (['LB', 'CB', 'RB', .etc'])
            
        '''
        
        if (type(player_role_list)!=list):
            raise TypeError
        else:
            
            self.player_role_list = player_role_list
            
            
            # dict array to store spatiotemporal data: referee data, goalkeeper data, and role data
            self.referee_data =  {'x':[], 'y':[], 'previous_x':[], 'previous_y':[], 'speed':[]}
            
            self.goalkeeper_data = {'home':{'x':[], 'y':[], 'previous_x':[], 'previous_y':[], 'speed':[]}, 
                                    'away':{'x':[], 'y':[], 'previous_x':[], 'previous_y':[], 'speed':[]}}
            
            self.role_data = {'home':{},'away':{}}
            for role in self.player_role_list + ['Team']:
                for team, _ in self.role_data.items():
                    self.role_data[team][role] = {'all_x':[],'all_y':[], 'all_speed':[],
                                                  'previous_all_x':[], 'previous_all_y':[],
                                                  'hir_x':[], 'hir_y':[], 'hir_speed':[],
                                                  'slow_x':[], 'slow_y':[], 'slow_speed':[],
                                                  'sprint_x':[], 'sprint_y':[], 'sprint_speed':[]}

                    
    def reset_role_data(self):
        
        '''
        rest lists in the dict, excluting the keys store previousious data
        '''

        for team, _ in self.role_data.items():
            for role, _ in self.role_data[team].items():
                for key, _ in self.role_data[team][role].items():
                    if 'previous' not in key: self.role_data[team][role][key] = []
                        
                        
    def reset_goalkeeper_data(self):
        
        '''
        rest lists in the dict, excluting the keys store previousious data
        '''
        
        for team, _ in self.goalkeeper_data.items():
            for key, _ in self.goalkeeper_data.items():
                if 'previous' not in key: self.goalkeeper_data[team][key] = []
                    
                    
    def reset_referee_data(self):
        
        '''
        rest lists in the dict, excluting the keys store previousious data
        '''
        
        for key, _ in self.referee_data.items():
            if 'previous' not in key: self.referee_data[key] = []
                

    def empty_speedgroup(self):
        
        '''
        Empty rolegroup feature dict
        '''
        
        self.speedgroup = {key: 0 if 'direction' in key else -1 for key, values in self.speedgroup.items()}
       
            
    def empty_team(self):
        
        '''
        Empty team feature dict
        '''
        
        self.team = {key: 0 if 'direction' in key else -1 for key, values in self.team.items()}
       
                
                
    def empty_bothteams(self):
        
        '''
        Empty booth-teams featrure dict
        '''
        
        self.bothteams = {key: 0 if 'direction' in key else -1 for key, values in self.bothteams.items()}
            
            
    def empty_referee(self):
        
        '''
        Empty refree feature dict
        '''
        
        self.referee = {key: 0 if 'direction' in key else -1 for key, values in self.referee.items()}
            
                
    def speedgroup_to_list(self):
        
        '''
        Convert reolegroup dict values to list
        
        Output
        ------
        feature_list: 1-D list
    
        '''
        features_list = []

        for key, value in self.speedgroup.items():
            features_list.append(value)
                
        return features_list
    
                
    def team_to_list(self):
        
        '''
        Convert team dict values to list
        
        Output
        ------
        feature_list: 1-D list
        '''
        
        features_list = []

        for key, value in self.team.items():
            features_list.append(value)
                
        return features_list
    
    
    def bothteams_to_list(self):
        
        '''
        Convert both-team dict values to list
        
        Output
        ------
        feature_list: 1-D list
        '''
        
        features_list = []

        for key, value in self.bothteams.items():
            features_list.append(value)
                
        return features_list
    
    
    def referee_to_list(self):
        
        '''
        Convert refree dict values to list
        
        Output
        ------
        feature_list: 1-D list
        '''
        
        features_list = []

        for key, value in self.referee.items():
            features_list.append(value)
                
        return features_list
    
    
    def get_feature_labels(self):
        
        '''
        Return labels of features set
        
        Output
        ------
        
        labels: string list 
        '''
        
        labels = []
        
        for tmp_team in ['home','away']:
            # for speedgoup
            for tmp_role in self.player_role_list+['Team']: 
                labels += [tmp_team + '_' + tmp_role + '_' + item for item in self.speedgroup.keys()]
            # for team
            labels += [tmp_team + '_' + tmp_role + '_' + item for item in self.team.keys()]
                
                
        # for bothteams
        labels += ['bothteams_' + item for item in self.bothteams.keys()]
                
        # for referee
        labels += ['referee_' + item for item in self.referee.keys()]
        
        return labels

    
    def calculate_features(self):
    
        '''
        Here we calculate all features for each group: speed_group, teams, bothteams, referee

    
        NOTE: Structure of data dict are given above and group key are indicated in the class itself

        Outpu:
        features: list stores all the claculated fatures
        '''

        features = [] # list to store all feature set

        # empty feature dict
        self.empty_speedgroup()
        self.empty_team()
        self.empty_bothteams()
        self.empty_referee()

        for tmp_team in ['home','away']:

            # SET SPEED GROUP FEATURES (for roles and teams)

            # iterate for every role
            for tmp_role in self.player_role_list+['Team']:

                dict_values = self.role_data[tmp_team][tmp_role] # get dict value

                self.empty_speedgroup() # empy feature dict 

                for tmp_prefix in ['all', 'slow', 'hir', 'sprint']:

                    # -------------- role speed group -----------------
                    self.speedgroup[tmp_prefix+'_avrg_x']  = calculate_average(dict_values[tmp_prefix+'_x'])
                    self.speedgroup[tmp_prefix+'_avrg_y'] =  calculate_average(dict_values[tmp_prefix+'_y'])
                    self.speedgroup[tmp_prefix+'_avrg_speed'] = calculate_average(dict_values[tmp_prefix+'_speed'])


                    # -------------- team speed group -----------------
                    if tmp_prefix == 'all':

                        previous_avrg_x = calculate_average(dict_values['previous_'+tmp_prefix+'_x'])
                        avrg_x = calculate_average(dict_values[tmp_prefix+'_x'])

                        previous_avrg_y = calculate_average(dict_values['previous_'+tmp_prefix+'_y'])
                        avrg_y = calculate_average(dict_values[tmp_prefix+'_y'])

                        self.role_data[tmp_team][tmp_role]['previous_'+tmp_prefix+'_x'] = dict_values[tmp_prefix+'_x']
                        self.role_data[tmp_team][tmp_role]['previous_'+tmp_prefix+'_y'] = dict_values[tmp_prefix+'_y']

                        inner_dis_to_avrg_pos = 0
                        for pos_i in range(len(dict_values[tmp_prefix+'_x'])):
                            inner_dis_to_avrg_pos += distance_2points(avrg_x, avrg_y, dict_values[tmp_prefix+'_x'][pos_i], dict_values[tmp_prefix+'_y'][pos_i])


                        self.speedgroup[tmp_prefix+'_avrg_direction_x'] = -1 if previous_avrg_x>avrg_x else 1 if previous_avrg_x<avrg_x else 0
                        self.speedgroup[tmp_prefix+'_avrg_direction_y'] = -1 if previous_avrg_y>avrg_y else 1 if previous_avrg_y<avrg_y else 0
                        self.speedgroup[tmp_prefix+'_inner_dis_to_avrg_pos'] = round(inner_dis_to_avrg_pos, 2)

                        del previous_avrg_x, avrg_x, previous_avrg_y, avrg_y, inner_dis_to_avrg_pos

                features += self.speedgroup_to_list() # add to feature list





            # SET SPECIAL TEAM FEATURES

            tmp_role = 'Team'
            tmp_prefix = 'all'
            dict_values = self.role_data[tmp_team][tmp_role] # get dict value
            self.empty_team() # empy feature dict 


            # -------------- player dbscan -----------------
            pos_array_2d = np.array([[dict_values[tmp_prefix+'_x'][dict_values_i], dict_values[tmp_prefix+'_y'][dict_values_i]] for dict_values_i in range(len(dict_values[tmp_prefix+'_y']))])

            # get dbscan indices
            dbscan_indices = innerDBSCAN(pos_array_2d, 20, 4) # min meter = 20, min cluster size = 4

            # get the selected indices
            dbscan_x = np.array(dict_values[tmp_prefix+'_x'])[dbscan_indices]
            dbscan_y = np.array(dict_values[tmp_prefix+'_y'])[dbscan_indices]
            dbscan_speed = np.array(dict_values[tmp_prefix+'_speed'])[dbscan_indices]

            dbscan_avrg_x = calculate_average(dbscan_x)
            dbscan_avrg_y = calculate_average(dbscan_y)
            dbscan_avrg_speed = calculate_average(dbscan_speed)

            inner_dis_to_dbscan_pos = 0
            for pos_i in range(len(dbscan_x)):
                inner_dis_to_dbscan_pos += distance_2points(dbscan_avrg_x, dbscan_avrg_y, dbscan_x[pos_i], dbscan_y[pos_i])

            self.team['dbscan_avrg_x'] = dbscan_avrg_x
            self.team['dbscan_avrg_y'] = dbscan_avrg_y
            self.team['dbscan_avrg_speed'] = dbscan_avrg_speed
            self.team['inner_dis_to_dbscan_pos'] = round(inner_dis_to_dbscan_pos, 2)

            del pos_array_2d, dbscan_indices, dbscan_x, dbscan_y, dbscan_speed, dbscan_avrg_x, dbscan_avrg_y, dbscan_avrg_speed, inner_dis_to_dbscan_pos


            # -------------- player normal -----------------
            self.team['min_x'] = min(dict_values[tmp_prefix+'_x'])
            self.team['min_x_speed'] = dict_values[tmp_prefix+'_speed'][np.argmin(dict_values[tmp_prefix+'_x'])]

            self.team['max_x'] = max(dict_values[tmp_prefix+'_x'])
            self.team['max_x_speed'] = dict_values[tmp_prefix+'_speed'][np.argmax(dict_values[tmp_prefix+'_x'])]

            self.team['min_y'] = min(dict_values[tmp_prefix+'_y'])
            self.team['min_y_speed'] = dict_values[tmp_prefix+'_speed'][np.argmin(dict_values[tmp_prefix+'_y'])]

            self.team['max_y'] = max(dict_values[tmp_prefix+'_y'])
            self.team['max_y_speed'] = dict_values[tmp_prefix+'_speed'][np.argmax(dict_values[tmp_prefix+'_y'])]

            self.team['min_speed'] = min(dict_values[tmp_prefix+'_speed'])
            self.team['min_speed_x'] = dict_values[tmp_prefix+'_x'][np.argmin(dict_values[tmp_prefix+'_speed'])]
            self.team['min_speed_y'] = dict_values[tmp_prefix+'_y'][np.argmin(dict_values[tmp_prefix+'_speed'])]

            self.team['max_speed'] = max(dict_values[tmp_prefix+'_speed'])
            self.team['max_speed_x'] = dict_values[tmp_prefix+'_x'][np.argmax(dict_values[tmp_prefix+'_speed'])]
            self.team['max_speed_y'] = dict_values[tmp_prefix+'_y'][np.argmax(dict_values[tmp_prefix+'_speed'])]


            # -------------- goalkeeper -----------------
            previous_avrg_x = calculate_average(self.goalkeeper_data[tmp_team]['previous_x'])
            avrg_x = calculate_average(self.goalkeeper_data[tmp_team]['x'])

            previous_avrg_y = calculate_average(self.goalkeeper_data[tmp_team]['previous_y'])
            avrg_y = calculate_average(self.goalkeeper_data[tmp_team]['y'])

            self.goalkeeper_data[tmp_team]['previous_x'] = self.goalkeeper_data[tmp_team]['x']
            self.goalkeeper_data[tmp_team]['previous_x'] = self.goalkeeper_data[tmp_team]['x']

            self.team['gk_x'] = avrg_x
            self.team['gk_y'] = avrg_y
            self.team['gk_speed'] = calculate_average(self.goalkeeper_data[tmp_team]['speed'])
            self.team['gk_direction_x'] = -1 if previous_avrg_x>avrg_x else 1 if previous_avrg_x<avrg_x else 0
            self.team['gk_direction_y'] = -1 if previous_avrg_y>avrg_y else 1 if previous_avrg_y<avrg_y else 0

            del previous_avrg_x, avrg_x, previous_avrg_y, avrg_y

            features += self.team_to_list() # add to feature list





        # SET SPECIAL BOTHTEAMS FEATURES

        self.empty_bothteams() # empy feature dict 
        
        tmp_role = 'Team'
        # get values of both teams
        bothteams_x = self.role_data['home'][tmp_role]['all_x'] + self.role_data['away'][tmp_role]['all_x']
        bothteams_y = self.role_data['home'][tmp_role]['all_y'] + self.role_data['away'][tmp_role]['all_y']
        bothteams_speed = self.role_data['home'][tmp_role]['all_speed'] + self.role_data['away'][tmp_role]['all_speed']


        # -------------- player normal -----------------
        bothteams_avrg_x = calculate_average(bothteams_x)
        bothteams_avrg_y = calculate_average(bothteams_y)
        bothteams_avrg_speed = calculate_average(bothteams_speed)

        inner_dis_to_avrg_pos = 0
        for pos_i in range(len(bothteams_x)):
            inner_dis_to_avrg_pos += distance_2points(bothteams_avrg_x, bothteams_avrg_y, bothteams_x[pos_i], bothteams_y[pos_i])

        self.bothteams['avrg_x'] = bothteams_avrg_x
        self.bothteams['avrg_y'] = bothteams_avrg_y
        self.bothteams['avrg_speed'] = bothteams_avrg_speed
        self.bothteams['inner_dis_to_avrg_pos'] = round(inner_dis_to_avrg_pos, 2)

        del bothteams_avrg_x, bothteams_avrg_y, bothteams_avrg_speed, inner_dis_to_avrg_pos    


        # -------------- player dbscan -----------------
        pos_array_2d = np.array([[bothteams_x[teams_val_i], bothteams_y[teams_val_i]] for teams_val_i in range(len(bothteams_x))])

        # get dbscan indices
        dbscan_indices = innerDBSCAN(pos_array_2d, 20, 7) # min meter = 20, min cluster size = 7

        # get the selected indices
        dbscan_x = np.array(bothteams_x)[dbscan_indices]
        dbscan_y = np.array(bothteams_y)[dbscan_indices]
        dbscan_speed = np.array(bothteams_speed)[dbscan_indices]

        dbscan_avrg_x = calculate_average(dbscan_x)
        dbscan_avrg_y = calculate_average(dbscan_y)
        dbscan_avrg_speed = calculate_average(dbscan_speed)

        inner_dis_to_dbscan_pos = 0
        for pos_i in range(len(dbscan_x)):
            inner_dis_to_dbscan_pos += distance_2points(dbscan_avrg_x, dbscan_avrg_y, dbscan_x[pos_i], dbscan_y[pos_i])


        self.bothteams['dbscan_avrg_x'] = dbscan_avrg_x
        self.bothteams['dbscan_avrg_y'] = dbscan_avrg_y
        self.bothteams['dbscan_avrg_speed'] = dbscan_avrg_speed
        self.bothteams['inner_dis_to_dbscan_pos'] = round(inner_dis_to_dbscan_pos, 2)

        del pos_array_2d, dbscan_indices, dbscan_x, dbscan_y, dbscan_speed, dbscan_avrg_x, dbscan_avrg_y, dbscan_avrg_speed, inner_dis_to_dbscan_pos
        del bothteams_x, bothteams_y, bothteams_speed

        features += self.bothteams_to_list() # add to feature list





        # SET REFEREE FEATURES
        self.empty_referee() # empty list

        previous_avrg_x = calculate_average(self.referee_data['previous_x'])
        avrg_x = calculate_average(self.referee_data['x'])

        previous_avrg_y = calculate_average(self.referee_data['previous_y'])
        avrg_y = calculate_average(self.referee_data['y'])

        self.referee_data['previous_x'] = self.referee_data['x']
        self.referee_data['previous_y'] = self.referee_data['y']

        self.referee['x'] = avrg_x
        self.referee['y'] = avrg_y
        self.referee['speed'] = calculate_average(self.referee_data['speed'])
        self.referee['direction_x'] = -1 if previous_avrg_x>avrg_x else 1 if previous_avrg_x<avrg_x else 0
        self.referee['direction_y'] = -1 if previous_avrg_y>avrg_y else 1 if previous_avrg_y<avrg_y else 0

        del previous_avrg_x, avrg_x, previous_avrg_y, avrg_y

        features += self.referee_to_list() # add to feature list

        return features