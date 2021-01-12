'''
This script collects only parent comments from all posts
on the r/mcgill subreddit entitled REAL TALK FRIDAY or
REAL TALK FRIDAYS and adds them to a df 
'''
import praw
import json
from datetime import datetime
import pandas as pd

title1 = "REAL TALK FRIDAY"
title2 = "REAL TALK FRIDAYS"

def main():
    
    # Create reddit instance
    # Check reddit profile for info
    reddit = praw.Reddit(client_id = '',
                         client_secret = '',
                         username = '',
                         password = '',
                         user_agent='')

    # look at subreddit of interest
    mcgill = reddit.subreddit('mcgill')

    comments_df = pd.DataFrame(columns=['Date', 'Comment'])

    # Search for only REAL TALK FRIDAY POSTS
    for post in mcgill.search(title1, sort='new', limit=None):
        # only collect comments from posts with exact title names
        if post.title==title1 or post.title==title2:
            date = datetime.fromtimestamp(int(post.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
            key = date.split(' ')[0]
            day_comments = []
            comments = post.comments
            for comment in comments:
                comments_df = comments_df.append({'Date':key, 'Comment':comment.body.replace('\n', ' ').strip()}, ignore_index=True)

    # save df as csv file for analysis
    comments_df.to_csv("mcgill_comments.csv", index=False)

if __name__ == '__main__':
    main()



        
