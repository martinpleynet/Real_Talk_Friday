'''
This script visualizes the most popular bigrams in the
REAL TALK FRIDAY comments without stopwords
'''
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

def main():
    
    # Read in csv
    all_comments = pd.read_csv('clean_comments.csv')

    # collect all tokens
    all_comments['tokens'] = all_comments['Clean'].apply(word_tokenize)
    
    # collect all bigrams
    all_comments['bigrams'] = all_comments['tokens'].apply(lambda row: list(nltk.ngrams(row, 2)))

    # add all bigrams to list
    all_bigrams = []
    for i in range(all_comments.shape[0]):
        all_bigrams += all_comments['bigrams'][i]

    # remove bigrams with non letter characters
    bigrams1 = []
    for gram in all_bigrams:
        for word in gram:
            if gram[0].isalpha() & gram[1].isalpha():
                bigrams1.append(gram)

    # create stopwords list
    stop_words = stopwords.words('english')
    stop_words.extend(['im', 'and', 'i', 'the', 'to', 'of', 'my', 'but', 'na', 'ta'])
    
    # remove bigrams with stop words
    bigrams2 = [gram for gram in bigrams1 if not any(stop in gram for stop in stop_words)]

    # get counts of all bigrams and identify top 20
    fdist1 = FreqDist(bigrams2)
    counts = pd.Series(fdist1)
    counts.sort_values(ascending=False, inplace=True)
    counts=counts[0:20]

    # create bar plot for 20 most used bigrams
    plt.style.use('fivethirtyeight')
    ax = counts.sort_values(ascending=True).plot(kind='barh', figsize=(11, 8), fontsize=12, color='red', alpha=0.7)
    ax.set_xlabel("Frequency", fontsize=12)
    ax.set_ylabel("Bigram", fontsize=12)
    ax.set_title("Top 20 Bigrams by Frequency in McGill REAL TALK FRIDAY Comments", fontsize=18)

    # Add frequency labels
    for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width()+.1, i.get_y()+.31, str(round((i.get_width()), 2)), fontsize=10, color='dimgrey')

    plt.tight_layout()
    plt.savefig("top20bigrams.png")

if __name__ == '__main__':
    main()
