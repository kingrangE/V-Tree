from mongodb_connector import MongoDBConnector
from datetime import datetime
from bson.objectid import ObjectId
class CoinAlertRepository:
    def __init__(self):
        self.db = MongoDBConnector().get_db()
        self.collection = self.db['coin_condition']
        
    def get_user_condition(self,member_id:str):
        try :
            return self.collection.find({"member_id":member_id})
        except Exception as e :
            print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")

    def insert_user_condition(self,ticker:str,member_id:str,price:int,**kwargs):
        try :
            return self.collection.insert_one({
                "member_id":member_id,
                "ticker":ticker,
                "price":price
            })
        except Exception as e :
            print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")

    def get_all_condition(self):
        try:
            return self.collection.find()
        except Exception as e :
            print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")

    def delete_one(self,**kwargs)->bool:
        """
        다양한 유형의 Option을 받아 해당 정보 1개 삭제(제일 처음 나온 기록 삭제)

        return
            True : Request is successed
            False : Unknown Error 
        """
        options = {}
        for k,v in kwargs.items():
            options[k]=v 
        try:
            self.collection.delete_one(options)
            return True
        except Exception as e:
            print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")

    def delete_all_bulk(self,member_id:str)->bool:
        """
        Member의 모든 기록 삭제
        
        return 
            True : All request is successed
            False : Unknown Error Raised (Log)
        """
        try:
            self.collection.delete_many({'member_id':member_id})
            return True
        
        except Exception as e :
            print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")
            return False
        
    def delete_all_with_ids(self,member_id:str,ids:list[str]) -> bool:
        """
        특정 Object id 전부 삭제
        
        return 
            True : All request is successed
            False : Unknown Error Raised (Log)
        """
        try:
            for id in ids:
                self.collection.delete_one({'_id':ObjectId(id),'member_id':member_id})
            return True
        
        except Exception as e :
            print(f"[Error]({datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) : {e}")
            return False
    

if __name__ == "__main__":
    repo = CoinConditionRepository()