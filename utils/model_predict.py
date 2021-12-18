import os
import pickle
import numpy as np
import pandas as pd
import xgboost as xgb
import utils.constants as Constants
from utils.repository import Repository
from sklearn.preprocessing import LabelEncoder

import io
import base64

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class ModelPredict:
    def __init__(self): 
        self.repository = Repository()
        self.model = self.load(os.environ['PATH_MODEL'])    


    def load(self, file_name):
        return pickle.load(open(file_name, "rb"))

    def predict(self, data):
        dict = data.to_dict()
        payload = [int(data[col]) for col in Constants.cols]
        payload = xgb.DMatrix([payload], feature_names=Constants.cols)
        predict = np.float64(self.model.predict(payload)[0])
        dict['result'] = predict
        self.repository.save_predict(dict)
        return predict

    def transform_fields(self, df, fields):
        label_encoder = LabelEncoder()
        for field in fields:
            df[field] = label_encoder.fit_transform(list(df[field].values))
        return df
    
    def validate(self):
        dataset = pd.read_csv('data/train.csv')
        dataset = dataset.sample(n=2000)
        dataset = dataset[Constants.cols]
        dataset_predict = self.transform_fields(dataset, Constants.cols)
        for i, row in enumerate(dataset_predict.to_dict('records')):
            predict = self._predict_validate(row)
            dataset_predict.loc[i,'result'] = predict
        return self.plot_graph(dataset_predict)


    def plot_graph(self, dt): 
        # Generate plot
        data = dt['result'].value_counts()
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        axis.set_title("Cotações de seguro de Casa")
        axis.set_xlabel("Cotações")
        axis.set_ylabel("Qtd. de cotações")
        axis.grid()
        axis.bar(["Não", "Sim"], [data[0], data[1]])
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return pngImageB64String
        

    def _predict_validate(self, data):
        payload = [int(data[col]) for col in Constants.cols]
        payload = xgb.DMatrix([payload], feature_names=Constants.cols)
        predict = np.float64(self.model.predict(payload)[0])
        data['result'] = predict
        self.repository.save_predict_validate(data)
        return predict
        
