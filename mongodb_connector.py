# Mongo DB Class
import os
from pymongo import MongoClient
from datetime import datetime
class MongoDBConnector:
    _instance = None
    def __new__(cls):
        if cls._instance is None :
            # 아직 없다면
            cls._instance = super().__new__(cls)
            URL = os.getenv("MONGO_URL","mongodb://localhost:27017")
            DB_NAME = os.getenv("MONGO_DB_NAME")
            try :
                cls._instance.client = MongoClient(URL)
                cls._instance.__db = cls._instance.client[DB_NAME]
                print("[Success] MongoDB is connected")
            except Exception as e :
                print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")
        return cls._instance

    def get_db(self):
        return self.__db
    
if __name__=="__main__":
    m = MongoDBConnector()
