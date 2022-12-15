from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    def __init__(self, username, password):
        # connect to the mongo instance and login
        self.client = MongoClient('mongodb://%s:%s@localhost:30317' % (username, password))
        # select the AAC database
        self.database = self.client['AAC']
        
    def create(self, data):
        if data is not None:
            try:
                # attempt to insert the passed data into the database
                self.database.animals.insert_one(data)
            except TypeError:
                # catch any invalid types defined by mongo
                return False
            return True
        else:
            raise Exception("Nothing to save, because data parameter is empty")
    
    def read(self, query):
        # We had to rework this function as it needed to work 
        # differently than the original implementation.
        # We found that the query could in fact be '{}'
        # which implies that the client of the API wants 
        # to get all the results in the collection.
        # '{}' evaluates to 'None' in Python. This means
        # our original None check would break the functionality
        # for this use case. ALSO, we needed to set "_id": False
        # so that the dashboard actually loads correctly.
        return self.database.animals.find(query, {"_id": False})
    
        # ============= Original Implementation =============
        # find the passed query and return the results
        #if query is not None:
        #    return self.database.animals.find(query)
        #else:
        #    raise Exception("Nothing to query, because query parameter is invalid") 
        # ============= Original Implementation =============
    
    def update(self, query, data):
        if query is not None:
            # update the data at query and return results
            return self.database.animals.update(query, data)
        else:
            raise Exception("Nothing to query, because query parameter is empty")
    
    def delete(self, query):
        if query is not None:
            # delete the document at query
            result = self.database.animals.delete_one(query)
            # check deletion status
            if result.deleted_count > 0:
                return True
            return False
        else:
            raise Exception("Nothing to query, because query parameter is empty")