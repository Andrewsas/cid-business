import os
from pymongo import MongoClient

class Repository: 
    def  __init__(self):
        self.client = MongoClient(os.environ['MONGO_URL'])
        self.db = self.client['business']
    
    def save_predict(seld, data):
        collection = seld.db['predicts']
        predict = collection.insert_one(data).inserted_id
        return predict

    def save_predict_validate(seld, data):
        collection = seld.db['validates']
        predict = collection.insert_one(data).inserted_id
        return predict

    def get_predicts(seld):
        collection = seld.db['predicts']
        predicts = collection.find()
        return predicts

    