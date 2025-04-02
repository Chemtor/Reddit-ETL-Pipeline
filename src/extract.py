import utils.setup as setup
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
SUBREDDIT = os.environ["SUBREDDIT"]
POST_LIMIT = int(os.environ["POST_LIMIT"])
COMMENT_LIMIT = int(os.environ["COMMENT_LIMIT"])
FILTER = os.environ["FILTER"]

def extract_data():
    reddit = setup.connect_reddit()
    posts = []
    for subreddit_name in SUBREDDIT.split(","):
        subreddit = reddit.subreddit(subreddit_name.strip())
        for post in subreddit.top(limit=POST_LIMIT, time_filter=FILTER):
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
                "author": str(comment.author),
                "score": comment.score,
                "body": comment.body,
                "created_date": datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                "parent_id": comment.parent_id
            })
    return posts, cmt_data