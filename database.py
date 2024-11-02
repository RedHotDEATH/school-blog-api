# database.py

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env file

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client.school_blog

#MONGO_URI=mongodb://localhost:27017  # Or your MongoDB URI
