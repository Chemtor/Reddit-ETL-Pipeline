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
    for post in post_data:
        post["title"] = clean_text(post["title"])
        if post["title"] == "":
            post["title"] = "Untitled"

        post["content"] = clean_text(post["content"])
        if post["content"] == "":
            post["content"] = "No content"
    
    # Clean comment data
    for cmt in cmt_data:
        for comment in cmt["comments"]:
            comment["body"] = clean_text(comment["body"])
        if cmt["comments"] == []:
            cmt["comments"] = "No comments"

    return post_data, cmt_data