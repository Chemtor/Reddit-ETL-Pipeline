# import emoji
import re

def clean_text(text):
    """Clean the text by removing unwanted characters and formatting."""
    text = re.sub(r"<.*?>", "", text)
    text = text.replace("\n", " ").replace("\r", " ")
    return text.strip()

def transformer(post_data, cmt_data):
    """Transform the data into a more structured format."""
    # Clean post data
    for post in post_data:
        post["title"] = clean_text(post["title"])
        post["content"] = clean_text(post["content"])
    
    # Clean comment data
    for cmt in cmt_data:
        for comment in cmt["comments"]:
            comment["body"] = clean_text(comment["body"])
    
    return post_data, cmt_data