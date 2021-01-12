'''
Visualize the McGill REAL TALK FRIDAY comments from the past
4-5 years in the form of a word cloud
'''
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

def main():

    # Read in cleaned comments
    comments = pd.read_csv('clean_comments.csv')

    # Create string with all words separated by spaces
    all_comments = " ".join(comment for comment in comments['Clean'])

    # Convert all words to upper case
    all_comments = all_comments.upper()

    # Create stop words and word cloud
    stopwords = set(STOPWORDS)
    stopwords.update(['IM', 'MCGILL'])
    wordcloud = WordCloud(max_words=50, stopwords=stopwords, background_color="white", colormap="Reds").generate(all_comments)

    # Customize and display wordcloud
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('mcgill_cloud.png')

if __name__ == '__main__':
    main()
