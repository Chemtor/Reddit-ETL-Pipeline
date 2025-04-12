import emoji
import re
from datetime import datetime

def clean_text(text):
    """Clean the text by removing unwanted characters and formatting."""
    text = re.sub(r"<.*?>", "", text)
    text = text.replace("\n", "").replace("\r", "").replace("\t", "").strip()
    text = re.sub(r" +", " ", text)
    text = emoji.demojize(text, delimiters=(":", ":"))
    return text

def transformer(post_data, cmt_data):
    """Transform the data into a more structured format."""
    # Clean post data
    clean_posts = []
    for post in post_data:
        if post["title"] == "[deleted]" or post["title"] == "[removed]":
            continue
        clean_posts.append(post)
    for post in clean_posts:
        post["title"] = clean_text(post["title"])
        if post["title"] == "":
            post["title"] = "Untitled"

        post["content"] = clean_text(post["content"])
        if post["content"] == "":
            post["content"] = "No content"
        
        post["created_utc"] = datetime.fromtimestamp(post["created_utc"]).strftime("%Y-%m-%d %H:%M:%S")
    
    # Clean comment data
    clean_comments = []
    for comment in cmt_data:
        if comment["body"] == "[deleted]" or len(comment["body"]) < 3 or comment["body"] == "[removed]" or comment["author"] == "u/AutoModerator":
            continue
        comment["body"] = clean_text(comment["body"])
        comment["created_utc"] = datetime.fromtimestamp(comment["created_utc"]).strftime("%Y-%m-%d %H:%M:%S")
        clean_comments.append(comment)
        

    return clean_posts, clean_comments