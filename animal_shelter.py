from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, USER, PASS):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31911
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

    def create(self, data):
        if data is not None and isinstance(data, dict):
            try:
                self.collection.insert_one(data)  # data should be dictionary
                return True       
            except Exception as e:
                print(f"An error occurred: {e}")
                return False     
        else:
            raise Exception("Nothing to save, because data parameter is empty")


    def read(self, query=None):
        print("Query:", query)
        if query is None:
            query = {}
        try:
            result = self.collection.find(query)
            documents = [doc for doc in result]
            print("Documents found:", len(documents))
            if documents:
                for doc in documents:
                    print(doc)  # Print each document
                return documents
            else:
                print("No documents match the query.")
                return []
        except Exception as e:
            print(f"An error occurred while reading from the database: {e}")
            return []
        
    def update(self, query, update_data):
        if query is None or update_data is None:
            raise Exception("Query and update_data must not be None")
        
        if not isinstance(query, dict) or not isinstance(update_data, dict):
            raise Exception("Query and update_data must be dictionaries")
        
        try:
            result = self.collection.update_many(query, {'$set': update_data})
            if result.matched_count > 0:
                print(f"Updated {result.modified_count} documents.")
                return True
            else:
                print("No documents matched the query.")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def delete(self, query):
        if query is None:
            raise Exception("Query must not be None")
        
        if not isinstance(query, dict):
            raise Exception("Query must be a dictionary")
        
        try:
            result = self.collection.delete_many(query)
            if result.deleted_count > 0:
                print(f"Deleted {result.deleted_count} documents")
                return True
            else:
                print("No documents matched the query.")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False