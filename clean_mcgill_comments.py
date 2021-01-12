'''
This script cleans the comments df created using
the scrape_mcgill_comments script
'''
import pandas as pd

def main():

    # read in comments df
    comments = pd.read_csv("mcgill_comments.csv")
    
    # remove all rows with [deleted] as a comment
    comments = comments[comments['Comment'] != '[deleted]']

    # remove all non alphanumeric characters from comments column
    comments['Clean'] = comments['Comment'].str.replace("[^\w\s\d']",' ')

    # convert all charcters to lowercase
    comments['Clean'] = comments['Clean'].str.lower()
    
    # convert string dates to datetime objects
    comments['Date'] = pd.to_datetime(comments['Date'])
    # create a new column for year
    comments['Year'] = comments['Date'].dt.year
    # create a new column for month
    comments['Month'] = comments['Date'].dt.month

    # Delete original text column
    del comments['Comment']
    
    comments.to_csv('clean_comments.csv', index=False)

if __name__ == '__main__':
    main()
