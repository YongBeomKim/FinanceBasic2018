import sys

import numpy as np
from IPython.core.display import Image

import praw


reddit = praw.Reddit(user_agent='wh', client_id='hDXtEHtUx1SFTQ', client_secret='NIO08EyBSAZnPYlw07Ntc5ruBmE')
#reddit = praw.Reddit("BayesianMethodsForHackers")

subreddit  = reddit.subreddit('showerthoughts')
#subreddit  = reddit.subreddit("showerthoughts")

#top_submissions = subreddit.top(limit=100)
top_submissions = subreddit.top(limit=100)


n_sub = int( sys.argv[1] ) if sys.argv[1] else 1

i = 0
while i < n_sub:
    top_submission = next(top_submissions)
    i+=1

top_post = top_submission.title

upvotes = []
downvotes = []
contents = []

for sub in top_submissions:
    try:
        print(reddit.get_submission(sub.permalink))
        ratio = reddit.get_submission(sub.permalink).upvote_ratio
        ups = int(round((ratio*sub.score)/(2*ratio - 1)) if ratio != 0.5 else round(sub.score/2))
        upvotes.append(ups)
        downvotes.append(ups - sub.score)
        contents.append(sub.title)
        
    except Exception as e:
        continue
votes = np.array( [ upvotes, downvotes] ).T

print(len(votes))
