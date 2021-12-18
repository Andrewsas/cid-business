import os
import pickle
import numpy as np
import xgboost as xgb
import utils.constants as Constants
from utils.repository import Repository

class ModelPredict:
    def __init__(self): 
        self.repository = Repository()
        self.model = self.load(os.environ['PATH_MODEL'])    


    def load(self, file_name):
        return pickle.load(open(file_name, "rb"))

    def predict(self, data):
        payload = [int(data[col]) for col in Constants.cols]
        payload = xgb.DMatrix([payload], feature_names=Constants.cols)
        predict = np.float64(self.model.predict(payload)[0])
        dict = data.to_dict()
        dict['result'] = predict
        self.repository.save_predict(dict)
        return predict
