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
POST_LIMIT = int(config['extraction']['limit'])
KEY = config['extraction']['key']
COMMENT_LIMIT = int(config['extraction']['comment_limit'])
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
                "created_utc": post.created_utc,
                'extracted_at': datetime.now().isoformat().split(".")[0].replace("T", " ")
            })

    cmt_data = []
    for post in posts:
        submission = reddit.submission(id=post["id"])
        submission.comments.replace_more(limit=0)
        # cmt_data.append({
        #     "id": post["id"],
        #     "title": post["title"],
        #     "subreddit": post["subreddit"],
        #     "comments": [],
        # })
        for comment in submission.comments.list()[:COMMENT_LIMIT]:
            cmt_data.append({
                "id": comment.id,
                "body": comment.body,
                "author": str(comment.author),
                "created_utc": comment.created_utc,
                "score": comment.score,
                "subreddit": post["subreddit"],
                "parent_id": comment.parent_id,
                "is_submitter": bool(comment.is_submitter),
                "distinguished": comment.distinguished
            })
    return posts, cmt_data