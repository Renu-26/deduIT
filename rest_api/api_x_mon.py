import requests
from pymongo import MongoClient

API_URL = "https://jsonplaceholder.typicode.com/posts"
MONGO_URI = "mongodb://localhost:27017"


def fetch_posts():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()      # stops with an error if the status is 4xx/5xx
    return response.json()           # a list of dictionaries


def main():
    posts = fetch_posts()
    print(f"Fetched {len(posts)} posts from the API")

    client = MongoClient(MONGO_URI)
    collection = client["api_data"]["posts"]   # database: api_data, collection: posts

    result = collection.insert_many(posts)
    print(f"Inserted {len(result.inserted_ids)} documents into MongoDB")


if __name__ == "__main__":
    main()