from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URL")

# Create a connection to MongoDB
client = MongoClient(mongo_url)
db = client["my_database"]
collection = db["users"]

# Function to verify password
def verify_password(email, entered_password):
    user = collection.find_one({"email": email})  # Find user by email
    if user:
        stored_hash = user["password"]  # This is now a hashed password
        # Compare the entered password with the stored hash
        try:
            return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash)
        except Exception as e:
            print(f"Error during password verification: {e}")
            return False
    return False

# Credentials to check
email_to_check = "ahmet@gmail.com"
password_to_check = "ahmet123"

# Perform check
if verify_password(email_to_check, password_to_check):
    print("✅ Login successful!")
else:
    print("❌ Invalid email or password!")