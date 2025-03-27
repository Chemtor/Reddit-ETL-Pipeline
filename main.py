import praw
import os
import time
import json
from datetime import datetime
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SUBREDDIT = os.getenv("SUBREDDIT")
POST_LIMIT = int(os.getenv("POST_LIMIT"))
COMMENT_LIMIT = int(os.getenv("COMMENT_LIMIT"))
WAIT_TIME = int(os.getenv("WAIT_TIME"))
DATA_PATH = os.getenv("DATA_PATH")
REMOTE_PATH = os.getenv("REMOTE_PATH")

KEY_ID = os.getenv("KEY_ID")
APPLICATION_KEY = os.getenv("APPLICATION_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")


reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent="DeleteThisBot"
)

info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", KEY_ID, APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(BUCKET_NAME)


def run_etl():
    subreddit = reddit.subreddit("nosleep")
    posts = []
    for post in subreddit.top(limit=1000):
        posts.append({
            "id": post.id,
            "title": post.title,
            "author": str(post.author),
            "score": post.score,
            "upvote_ratio": post.upvote_ratio,
            "num_comments": post.num_comments,
            "url": post.url,
            "created_date": datetime.fromtimestamp(post.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
            "selftext": post.selftext,
        })

    cmt_data = []
    for post in posts:
        submission = reddit.submission(id=post["id"])
        submission.comments.replace_more(limit=0)
        cmt_data.append({
            "id": post["id"],
            "title": post["title"],
            "comments": []
        })
        for comment in submission.comments.list()[:10]:
            cmt_data[-1]["comments"].append({
                "id": comment.id,
                "author": str(comment.author),
                "score": comment.score,
                "body": comment.body,
                "created_date": datetime.fromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S")
            })

    with open(DATA_PATH, "w", encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, sort_keys=False, indent=4)

    with open(DATA_PATH.replace(".json", "_comments.json"), "w", encoding='utf-8') as f:
        json.dump(cmt_data, f, ensure_ascii=False, sort_keys=False, indent=4)

    bucket.upload_local_file(local_file=DATA_PATH, file_name=REMOTE_PATH)
    bucket.upload_local_file(local_file=DATA_PATH.replace(".json", "_comments.json"), file_name=REMOTE_PATH.replace(".json", "_comments.json"))

    os.remove(DATA_PATH)
    os.remove(DATA_PATH.replace(".json", "_comments.json"))

while True:
    try:
        run_etl()
    except Exception as e:
        print(e)
    time.sleep(WAIT_TIME)