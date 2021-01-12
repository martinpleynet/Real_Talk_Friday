'''
This script aims to identify the most popular words by week
and their frequencies
'''
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from nltk.probability import FreqDist

def main():
    
    # Read in csv
    all_comments = pd.read_csv('clean_comments.csv')

    # Create stop words list
    stop_words = stopwords.words('english')
    stop_words.extend(['im'])
    
    # Tokenize comments by word
    all_comments['tokens'] = all_comments['Clean'].apply(word_tokenize)

    # Get all dates in a list
    dates = list(all_comments['Date'].unique())

    words_of_week = []
    # Identify top used word for each week and append to words_of_week list
    for date in dates:
        # Get df for specific date and reset index
        cur_date = all_comments.groupby('Date').get_group(date)
        cur_date.index=range(len(cur_date))

        # Add all tokens to a list
        cur_tokens = []
        for i in range(cur_date.shape[0]):
            cur_tokens += cur_date['tokens'][i]

        # Remove tokens that do not only consist if letter
        tokens1 = [word for word in cur_tokens if word.isalpha()]

        # Remove tokens that are stop words
        tokens2 = [x for x in tokens1 if x.lower() not in stop_words]

        # Identify top word of the week 
        fdist1 = FreqDist(tokens2)
        counts = pd.Series(fdist1)
        counts.sort_values(ascending=False, inplace=True)
        word = list(dict(counts).keys())[0]

        # Append word of the week to list
        words_of_week.append(word)

    # Determine top 20 most words of the weel
    fdist1 = FreqDist(words_of_week)
    counts = pd.Series(fdist1)
    counts.sort_values(ascending=False, inplace=True)
    counts=counts[0:20]

    # Graph frequency of words of the week
    plt.style.use('fivethirtyeight')
    ax = counts.sort_values(ascending=True).plot(kind='barh', figsize=(10, 9), fontsize=12, color='red', alpha=0.7)
    ax.set_xlabel("Frequency", fontsize=12)
    ax.set_ylabel("Word", fontsize=12)
    ax.set_title("Top 20 Most Word of the Weeks by Frequency", fontsize=18)
    # Add caption describing Word of the Week
    ax.text(12.5, -2.15, 'The number of times a word was the most used word for a given week', ha='center', fontdict = {'fontsize':8})

    # Add frequency labels
    for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width()+.1, i.get_y()+.31, str(round((i.get_width()), 2)), fontsize=10, color='dimgrey')

    plt.tight_layout()
    plt.savefig('top20wow.png')

if __name__ == '__main__':
    main()
