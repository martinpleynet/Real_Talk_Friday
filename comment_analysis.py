'''
This script analyzes the comments of the REAL TALK FRIDAY posts by looking at
the top 20 words by frequency and the sentiment and subjectivity of
comments using TextBlob.
'''
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from textblob import TextBlob

def main():

    # Read in csv
    all_comments = pd.read_csv('clean_comments.csv')

    # ---------------------------------------------------------------------------------------------
    # GET FREQUENCY COUNTS OF TOP 20 WORDS
    
    # Tokenize comments by word
    all_comments['tokens'] = all_comments['Clean'].apply(word_tokenize)

    # Store all tokens in a list 
    all_tokens = []
    for i in range(all_comments.shape[0]):
        all_tokens += all_comments['tokens'][i]

    # Filter tokens that do not consist if only letters
    tokens1 = [word for word in all_tokens if word.isalpha()]

    # Create stop words list
    stop_words = stopwords.words('english')
    stop_words.extend(['im'])

    # Filter tokens that are stop words
    tokens2 = [x for x in tokens1 if x.lower() not in stop_words]

    # Get counts of all of the words and keep tp 20
    fdist1 = FreqDist(tokens2)
    counts = pd.Series(fdist1)
    counts.sort_values(ascending=False, inplace=True)
    counts=counts[0:20]

    # Create bar plot for top 20 most frequent words
    plt.style.use('fivethirtyeight')
    ax = counts.sort_values(ascending=True).plot(kind='barh', figsize=(10, 9), fontsize=12, color='red', alpha=0.7)
    ax.set_xlabel("Frequency", fontsize=12)
    ax.set_ylabel("Word", fontsize=12)
    ax.set_title("Top 20 Words by Frequency in McGill REAL TALK FRIDAY Comments", fontsize=18)

    # Add frequency labels
    for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width()+.1, i.get_y()+.31, str(round((i.get_width()), 2)), fontsize=10, color='dimgrey')

    plt.tight_layout()
    plt.savefig('top20words.png')

    # ----------------------------------------------------------------------------------------
    # EVALUATE SENTIMENT/SUBJECTIVITY OF COMMENTS
    
    # Get the polarity of individual comments - polarity is a score from -1 to 1
    # where -1 is strongly negative and 1 is strongly positive
    def get_polarity(comment):
        return TextBlob(comment).sentiment[0]

    # Add a polarity column
    all_comments['polarity'] = all_comments['Clean'].apply(get_polarity)

    # Get the subjectivity of individual comments - subjectivity is a score from 0 to 1
    # where 0 is purely fact based and 1 is purely opinion based
    def get_subjectivity(comment):
        return TextBlob(comment).sentiment[1]

    # Add a subjectivity column
    all_comments['subjectivity'] = all_comments['Clean'].apply(get_subjectivity)

    # Get distribution of sentiment scores
    num_bins1 = 50
    plt.figure(figsize=(10,6))
    n, bins, patches = plt.hist(all_comments['polarity'], num_bins1, facecolor='red', alpha=0.6)
    plt.xlabel('Polarity')
    plt.ylabel('Count')
    plt.title('Distribution of Polarity Scores of Comments')

    plt.tight_layout()
    plt.savefig('comments_sentiment.png')

    # Get distribution of subjectivity scores
    num_bins2 = 50
    plt.figure(figsize=(10,6))
    n, bins, patches = plt.hist(all_comments['subjectivity'], num_bins2, facecolor='red', alpha=0.6)
    plt.xlabel('Subjectivity')
    plt.ylabel('Count')
    plt.title('Distribution of Subjectivity Scores of Comments')

    plt.tight_layout()
    plt.savefig('comments_subjectivity.png')

    # Extract top 20 most positive comments
    positive_sentiment = all_comments.nlargest(20, 'polarity')
    positive_sentiment = positive_sentiment[['Clean', 'Date', 'polarity']]
    
    # Extract top 20 most negative comments
    negative_sentiment = all_comments.nsmallest(20, 'polarity')
    negative_sentiment = negative_sentiment[['Clean', 'Date', 'polarity']]

    # Save top 20 negative/positive comments dfs
    positive_sentiment.to_csv('top20positive.csv', index=False)
    negative_sentiment.to_csv('top20negative.csv', index=False)
     
if __name__ == '__main__':
    main()
