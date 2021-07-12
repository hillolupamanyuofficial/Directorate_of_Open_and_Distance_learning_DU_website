from flask import jsonify
from .DataFormatter import Formatter
class Datadaos:
    def __init__(self,cluster):
        self.cluster = cluster


    def check_ntf(self,title,col):
        cluster = self.cluster.db
        collection = cluster[col]
        response = collection.find_one({"title": 
            {'$regex' : '^{}'.format(title),'$options' : 'i'}
            })
        if response:
            return collection
        return False


    def get_notifications_by_category(self,col):
        cluster = self.cluster.db
        collections = cluster[col]
        response = collections.find()
        if response:
            result = Formatter.NotificationFormatter(response)
            return result
        return False

    def get_notifications_by_title(self,title):
        cluster = self.cluster.db
        collections = cluster.collection_names()
        for i in collections:
            collection = cluster[i]
            response = collection.find_one({"title": 
            {'$regex' : '^{}'.format(title),'$options' : 'i'}
            })
            if response:
                return response["doc_link"]
        return False

    def post_new_notification(self,data,col):
        title = data["title"]
        collection = self.check_ntf(title,col)
        if collection:
            return collection.update_one({"title" : title},{"$set" : data})
        else:
            cluster = self.cluster.db
            col = cluster[col]
            return col.insert_one(data)

    def delete_notification(self,title):
        try: 
            cluster = self.cluster.db
            collections = cluster.collection_names()
            for i in collections:
                collection = cluster[i]
                response = collection.find_one({"title": 
                {'$regex' : '^{}'.format(title),'$options' : 'i'}
                })
                if response:
                    result = collection.delete_one({"title" : title})
                    if result:
                        return True
            return False
        except Exception as e:
            with open('error.log','a') as fptr:
                fptr.write(f"Error: {e}\n")
            return False