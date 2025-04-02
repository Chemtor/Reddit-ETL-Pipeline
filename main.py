from src import extract, transform, load
from utils import save_to_file
import os
from dotenv import load_dotenv

load_dotenv()
# Load environment variables
DATA_DIR_RAW = os.getenv("DATA_DIR_RAW")
DATA_PATH = os.getenv("DATA_PATH")

post_data, cmt_data = extract.extract_data()
# save_to_file.save_to_file_json(post_data, DATA_DIR_RAW + "/posts.json")
# save_to_file.save_to_file_json(cmt_data, DATA_DIR_RAW + "/comments.json")

clean_posts, clean_comments = transform.transformer(post_data, cmt_data)
save_to_file.save_to_file_json(clean_posts, DATA_PATH + "/clean_posts.json")
save_to_file.save_to_file_json(clean_comments, DATA_PATH + "/clean_comments.json")

# load.load_to_postgresql(clean_posts, clean_comments)
load.upload_data_to_bucket(clean_posts)
load.upload_data_to_bucket(clean_comments)

