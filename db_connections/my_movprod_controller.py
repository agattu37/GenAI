from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri)


db = client["sample_mflix"]
movie_collection = db["movies"]


def get_all_movies():
    try:
        result = list(movie_collection.find({}))
        print("All Movies are", result)
    except Exception as e:
        print(f"Error occured while fetching all movies", e)



def get_movies_by_filter(year: str = None):
    """
    Queries the mongodb for movies based on a given year
    """

    search_filter = {}

    if year:
        #search_filter["year"] = {"$regex" : year, "$options" : "i"}
        search_filter["year"] = int(year)

    results = list(movie_collection.find(search_filter))

    for result in results:
        result['_id'] = str(result['_id'])

    print(results)

#    return json.dumps(results)
    return results


#get_all_products()
#get_product_by_filter("Smartphones")
get_movies_by_filter("1946")
#get_all_movies()
