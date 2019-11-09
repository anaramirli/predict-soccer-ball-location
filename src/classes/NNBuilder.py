from classes.NNParameterValidate import *
from classes.Utils import *
from keras.models import Sequential
from keras.layers import Dropout
from keras.layers import Dense
from keras.regularizers import l1_l2

class NNBuilder(object):  
   
    parameterValidate = ParameterValidate()
    
    
    def __init__(self, input_shape = None):
        

    # validate and set values  
        if type(input_shape)==int:
            self.input_shape = input_shape
        else:
            raise ValueError
            
    def activate_regularization(self, key_value):
        '''
        Parameters
        ----------
        key_value= inner key of nn structure stores the regularization information
        
  
        Output
        ------
        if kernel and activity regularizers are not defined then set them to None
        '''
       
        try:
            kernel_regularizer=l2(key_value['kernel_regularizer'])
        except:
            kernel_regularizer=None

        try:
            activity_regularizer=l1(key_value['activity_regularizer'])
        except:
            activity_regularizer=None

        return kernel_regularizer, activity_regularizer 
            
    def init_model(self, nn_structure):
        
        # convert dict keys to lover case
        nn_structure = dictKeyLower(nn_structure) 
        
        # validate dict
        if self.parameterValidate.validate_NNlayer_dict(nn_structure)==True: 
            # init model
            self.model = Sequential() 
            
            
            kernel_regularizer_p, activity_regularizer_p = self.activate_regularization(nn_structure['input'])
            
            #add input layer
            self.model.add(Dense(nn_structure['input']['layer'], activation=nn_structure['input']['activation'], input_shape=(self.input_shape,), kernel_regularizer=kernel_regularizer_p, activity_regularizer=activity_regularizer_p))

            # add hidden and droupout layers
            for layer, values in nn_structure.items():
                if 'hidden' in layer:
                    
                    kernel_regularizer_p, activity_regularizer_p = self.activate_regularization(values)
                    
                    self.model.add(Dense(values['layer'], activation=values['activation'], input_shape=(self.input_shape,), kernel_regularizer=kernel_regularizer_p, activity_regularizer=activity_regularizer_p))
                elif 'dropout' in layer:
                    self.model.add(Dropout(values['ratio']))

            # add output layer
            self.model.add(Dense(nn_structure['output']['layer'], activation=nn_structure['output']['activation']))
            
    

    # return model
    def get_model(self):
        return self.model

    def del_model(self):
        del self.model
    
    def save_model(self, folder_name, model_name):
        # Creates a HDF5 file 'my_model.h5'
        self.model.save('{path}/{model}.h5'.format(path=folder_name,model=model_name))
 
