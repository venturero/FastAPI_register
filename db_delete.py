from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()
mongo_url = os.getenv("MONGO_URL")

if mongo_url is None:
    print("Error: MongoDB URI is missing in the environment variables.")
    exit()

# Add TLS/SSL settings
client = MongoClient(mongo_url, 
                    tls=True,
                    tlsAllowInvalidCertificates=False)

try:
    # Test the connection
    client.admin.command('ping')
    
    # If connection successful, proceed with your operations
    db = client["my_database"]
    
    if "users" in db.list_collection_names():
        db["users"].drop()
        print("The 'users' collection has been deleted.")
    else:
        print("The 'users' collection does not exist.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()