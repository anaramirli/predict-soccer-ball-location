
class ParameterValidate(object):

    def validate_NNlayer_dict(self, nn_structure):

        '''
        Validation of below dict strucutre:

           {'Input':   { 'layer': 150, 'activation': 'relu', kernel_regularizer': l2(0.01), 'activity_regularizer': l1(0.01)},
            'Hidden1': { 'layer': 150, 'activation': 'sofmax', kernel_regularizer': l2(0.01), 'activity_regularizer': l1(0.01)},
            'Hidden1': { 'layer': 150, 'activation': 'sofmax'},
            'Dropout': { 'ratio': 0.2},
            'Output':  { 'layer': 150, 'activation': 'sofmax'}
            }


        '''

        try:
            keys = list(nn_structure.keys())

            if 'input' not in keys or 'output' not in keys:
                assert False, "Input and Output layer must be defined"
        except AttributeError:
            assert False, "Strucute type is not dict"


        for layer_i, layer in enumerate(nn_structure.keys()):

            if layer in ['input', 'output'] or 'hidden' in layer:
                try:
                    inner_keys = list(nn_structure[layer].keys())
                    
                    if 'layer' not in inner_keys or 'activation' not in inner_keys or len(inner_keys)>4:
                        assert False, "{}: Wrong layer structure".format(layer)
                        
                    if len(inner_keys)==3:
                        if 'kernel_regularizer' not in inner_keys and 'activity_regularizer' not in inner_keys:
                            assert False, "{}: Wrong inner keys".format(layer)
                    elif len(inner_keys)==4:
                        if 'kernel_regularizer' not in inner_keys or 'activity_regularizer' not in inner_keys:
                            assert False, "{}: Wrong inner keys".format(layer)
                            
                    if type(nn_structure[layer]['layer'])!=int:
                        assert False, "{}: 'layer' value must be int".format(layer)
                        
                    if type(nn_structure[layer]['activation'])!=str:
                        assert False, "{}: 'activation' value must be str".format(layer)
                        
                    
                    try:
                        if type(nn_structure[layer]['kernel_regularizer'])!=float and type(nn_structure[layer]['kernel_regularizer'])!=None:
                            assert False, "{}: 'kernel_regularizer' value must be the variable of keras.regularizers.L1L2 type".format(layer)
                    except:
                        pass
                    
                    try:
                        if type(nn_structure[layer]['activity_regularizer'])!=float and type(nn_structure[layer]['activity_regularizer'])!=None:
                            assert False, "{}: 'activity_regularizer' value must be the variable of keras.regularizers.L1L2 type".format(layer)
                    except:
                        pass
                        
                except AttributeError:
                    assert False, "{}: Inner type is not dict".format(layer)


            elif 'dropout' in layer:
                try:
                    inner_keys = list(nn_structure[layer].keys())

                    if 'ratio' not in inner_keys or len(inner_keys)!=1:
                        assert False, "{}: Wrong inner key".format(layer)
                    if type(nn_structure[layer]['ratio'])!=float:
                        assert False, "{}: 'ratio' value must be float".format(layer)
                except AttributeError:
                    assert False, "{}: Inner type is not dict".format(layer)

            else:
                assert False, "{} is wrong layer name".format(layer)

        return True