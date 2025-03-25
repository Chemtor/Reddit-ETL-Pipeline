import praw
import logging

client_id = "jJIKCundTtZaI98jM8vAUw"
client_secret = "FNnxW3dQ8gvApsqfwosxdAVUeoB6qw"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent="DeleteThisBot"
)

print(reddit.read_only) # Output: True
print(reddit.user.me()) # Output: TestBotDMM

for submission in reddit.subreddit("askreddit").hot(limit=10):
    logging.info(submission.title)