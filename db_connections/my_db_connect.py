from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
# A module to connect to MongoDB and test the connection and try inserting 
# records into the db.
# Create the db connection string and store it securely in the .env file
# and read it initialize a connection
mongodb_uri = os.getenv("MONGODB_URI")

client = MongoClient(mongodb_uri)

def check_connection_status():
    try:
        client.admin.command("ismaster")
        print("Successfully connected to MongoDB")
    except Exception as e:
        print("Failed to connect to MongoDB", e)

    finally:
        client.close()

# sample data record to be inserted
#data = [
#        {
#            "id" : "123",
#            "name" : "Testing Product",
#            "description" : "adfsf",
#            "price" : 100,
#            "stock" : 10
#        }
#]

def add_dummy_products_to_db(data):
    try:
        db = client["store_database"]
        product_collection = db["products"]
        result = product_collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} products into the 'products' collection")
    
    except Exception as e:
        print(f"An error occured while adding data to db: {e}")

    finally:
        client.close()


check_connection_status()
