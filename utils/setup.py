import praw
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def connect_reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET):
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="DeleteThisBot"
    )
