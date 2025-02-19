from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from the environment variable
mongo_url = os.getenv("MONGO_URL")

if mongo_url is None:
    print("Error: MongoDB URI is missing in the environment variables.")
    exit()

# Create a connection to MongoDB
client = MongoClient(mongo_url)

# Print the list of databases
print("Databases:")
databases = client.list_database_names()
for db_name in databases:
    print(f"- {db_name}")

# Select the database (or create one if it doesn't exist)
db = client["my_database"]

# Print the list of collections in the selected database
print("\nCollections in 'my_database':")
collections = db.list_collection_names()
for collection_name in collections:
    print(f"- {collection_name}")

# Select the collection (MongoDB uses collections instead of tables)
collection = db["users"]

# Function to hash password with salt
def hash_password(plain_password):
    # Generate a random salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed

# Data to insert into the collection with hashed passwords
users_data = [
    {"email": "ahmet@gmail.com", "password": hash_password("ahmet123")},
    {"email": "eduardo@gmail.com", "password": hash_password("edu123")},
    {"email": "gustavo@gmail.com", "password": hash_password("gustovo123")},
    {"email": "marina@gmail.com", "password": hash_password("marina123")}
]

# Insert the data into the "users" collection
collection.insert_many(users_data)

# Print the inserted documents
print("\nDocuments in 'users' collection:")
for user in collection.find():
    # Convert binary password hash to string for display
    user['password'] = user['password'].decode('utf-8')
    print(user)

print("\nData inserted successfully!")