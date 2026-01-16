from mongodb_connector import MongoDBConnector
from datetime import datetime
class UserRepository:
    def __init__(self):
        self.db = MongoDBConnector().get_db()
        self.collection = self.db['users']
    def find_user(self,member_id:str):
        try :
            return self.collection.find_one({"member_id":member_id})
        except Exception as e :
            print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")
    def insert_user(self,name:str,member_id:str,**kwargs):
        try :
            return self.collection.insert_one({
                "name":name,
                "member_id":member_id,
            })
        except Exception as e :
            print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")
