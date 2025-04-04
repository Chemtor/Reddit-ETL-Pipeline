import utils.setup_api as setup_api
from datetime import datetime
# import os
from dotenv import load_dotenv
import yaml

load_dotenv()

# Load environment variables
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

SUBREDDIT = config['subreddits']
POST_LIMIT = config['extraction']['limit']
KEY = config['extraction']['key']
COMMENT_LIMIT = config['extraction']['comment_limit']
FILTER = config['extraction']['time_filter']

def extract_data():
    reddit = setup_api.connect_reddit()
    posts = []
    for subreddit_name in SUBREDDIT:
        subreddit = reddit.subreddit(subreddit_name)
        if KEY == "hot":
            subreddit = subreddit.hot(limit=POST_LIMIT)
        elif KEY == "new":
            subreddit = subreddit.new(limit=POST_LIMIT)
        elif KEY == "rising":
            subreddit = subreddit.rising(limit=POST_LIMIT)
        elif KEY == "controversial":
            subreddit = subreddit.controversial(limit=POST_LIMIT, time_filter=FILTER)
        elif KEY == "top":
            subreddit = subreddit.top(limit=POST_LIMIT, time_filter=FILTER)
        for post in subreddit:
            posts.append({
                "id": post.id,
                "title": post.title,
                "author": str(post.author),
                "subreddit": post.subreddit.display_name,
                "content": post.selftext,
                "score": post.score,
                "upvote_ratio": post.upvote_ratio,
                "num_comments": post.num_comments,
                "url": post.url,
                "created_date": datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'extracted_at': datetime.now().isoformat().split(".")[0].replace("T", " ")
            })

    cmt_data = []
    for post in posts:
        submission = reddit.submission(id=post["id"])
        submission.comments.replace_more(limit=0)
        cmt_data.append({
            "id": post["id"],
            "title": post["title"],
            "subreddit": post["subreddit"],
            "comments": [],
            "extracted_at": datetime.now().isoformat().split(".")[0].replace("T", " ")
        })
        for comment in submission.comments.list()[:COMMENT_LIMIT]:
            cmt_data[-1]["comments"].append({
                "id": comment.id,
                "parent_id": comment.parent_id,
                "author": str(comment.author),
                "score": comment.score,
                "body": comment.body,
                "created_date": datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            })
    return posts, cmt_data