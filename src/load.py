import pandas as pd
import os
from dotenv import load_dotenv
from b2sdk.v2 import InMemoryAccountInfo, B2Api
import json

load_dotenv()

# KEY_ID = os.getenv("KEY_ID")
# APPLICATION_KEY = os.getenv("APPLICATION_KEY")
# BUCKET_NAME = os.getenv("BUCKET_NAME")
# REMOTE_PATH = os.getenv("REMOTE_PATH")
KEY_ID = os.environ["KEY_ID"]
APPLICATION_KEY = os.environ["APPLICATION_KEY"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
REMOTE_PATH = os.environ["REMOTE_PATH"]

info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", KEY_ID, APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

def load_to_postgresql(data, cmt_data):
    """Load the data into PostgreSQL database."""
    from sqlalchemy import create_engine

    # Load environment variables
    DB_URL = os.getenv("DB_URL")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Create a connection to the PostgreSQL database
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}')

    # Convert data to DataFrame
    posts_df = pd.DataFrame(data)
    comments_df = pd.DataFrame([{
        **cmt,
        "comments": cmt["comments"]
    } for cmt in cmt_data])

    # Load data into PostgreSQL tables
    posts_df.to_sql('posts', engine, if_exists='replace', index=False)
    comments_df.to_sql('comments', engine, if_exists='replace', index=False)

def delete_data():
    for file_info in bucket.ls(REMOTE_PATH):
        file_version = bucket.get_file_info_by_name(file_info.file_name)
        file_version.delete()

def upload_data_to_bucket(posts, cmts):
    """Upload the data to B2 bucket."""
    with open("data.json", "w") as f:
        json.dump(posts, f)
    
    with open("data_2.json", "w") as f:     
        json.dump(cmts, f)
    # Upload the file to B2 bucket
    # delete_data()
    # Upload the file to B2 bucket
    bucket.upload_local_file(
        local_file="data.json",
        file_name=REMOTE_PATH + "/post.json"
    )

    bucket.upload_local_file(
        local_file="data_2.json",
        file_name=REMOTE_PATH + "/comments.json"
    )

    # Delete the local file after uploading
    os.remove("data.json")
    os.remove("data_2.json")
        
    