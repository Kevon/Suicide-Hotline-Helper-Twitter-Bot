import praw
from collections import Counter

r = praw.Reddit(user_agent='kevons5252')
submission = r.get_subreddit('suicidewatch').get_top(limit=1000)
posts = ""
for post in submission:
	posts = posts+post.selftext
words = posts.split()
wordCount = Counter(words)

print wordCount
