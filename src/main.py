from etl import extract, transform, load
from utils import save_to_file
# import os
from dotenv import load_dotenv
from utils.logger import get_logger
import yaml

logger = get_logger(__name__)

load_dotenv()
# Load environment variables
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

DATA_RAW = config['data_path']['raw']
DATA_PROCESSED = config['data_path']['processed']

logger.info("Starting ETL process")
logger.info("Extracting data from Reddit API")
post_data, cmt_data = extract.extract_data()
logger.info("Extracted data from API successfully")
logger.info(f"Post data: {len(post_data)} records")
logger.info(f"Comment data: {len(cmt_data)} records")
logger.info("Saving data to files")
save_to_file.save_to_file_json(post_data, DATA_RAW + "/posts.json")
save_to_file.save_to_file_json(cmt_data, DATA_RAW + "/comments.json")


logger.info("Transforming data")
clean_posts, clean_comments = transform.transformer(post_data, cmt_data)
logger.info("Transformed data successfully")
logger.info(f"Clean post data: {len(clean_posts)} records")
logger.info(f"Clean comment data: {len(clean_comments)} records")
logger.info("Saving transformed data to files")
save_to_file.save_to_file_json(clean_posts, DATA_PROCESSED + "/clean_posts.json")
save_to_file.save_to_file_json(clean_comments, DATA_PROCESSED + "/clean_comments.json")
save_to_file.save_to_file_csv(clean_posts, DATA_PROCESSED + "/posts.csv")
save_to_file.save_to_file_csv(clean_comments, DATA_PROCESSED + "/comments.csv")

# load.load_to_postgresql(clean_posts, clean_comments)
# logger.info("Loaded data to PostgreSQL")
load.upload_data_to_bucket(clean_posts, clean_comments)
logger.info("Data uploaded to B2 bucket successfully")

