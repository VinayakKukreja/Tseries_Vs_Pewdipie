'''''
--> Package Information:
    --------------------
    This package enables creation of word clouds from analyzing the csv files of the comments 
    retrieved of various videos and plotting the top twenty words as a word cloud of the 
    respective videos
    
--> Version Control:
    ----------------
    Source:
    -------
        version 1.0, Date: April 23, 2019  
'''''

# ------------< Importing packages >------------

import pandas as pd
import os
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from nltk.probability import *

# ------------< Creating class >------------
class CreatingWordCloud:

    # ------------< Creating respective wordclouds according to path >------------
    def word_Cloud(self, path):
        top_20_words = self.getMostUsedWords(path)
        wordcloud = WordCloud(width=800, height=400, max_words=20, background_color="white").generate_from_frequencies(top_20_words)
        plt.figure(figsize=(20, 10), facecolor=None)
        plt.tight_layout(pad=0)
        plt.axis("off")
        save_with_name = os.path.basename(os.path.normpath(path))
        wordcloud.to_file("./data/word_clouds/word_cloud_"+save_with_name+".png")

    # ------------< Getting top 20 most used words in the comments of videos >------------
    def getMostUsedWords(self, path):
        try:
            all = pd.read_csv(path)
            stop_eng = stopwords.words('english')
            customstopwords = []
            tokens = []
            sentences = []
            tokenizedSentences = []
            for txt in all.text:
                sentences.append(txt.lower())
                tokenized = [t.lower().strip(":,.!?") for t in txt.split()]
                tokens.extend(tokenized)
                tokenizedSentences.append(tokenized)
            hashtags = [w for w in tokens if w.startswith('#')]
            ghashtags = [w for w in tokens if w.startswith('+')]
            mentions = [w for w in tokens if w.startswith('@')]
            links = [w for w in tokens if w.startswith('http') or w.startswith('www')]
            filtered_tokens = [w for w in tokens if
                               not w in stop_eng and not w in customstopwords and w.isalpha() and not len(
                                   w) < 3 and not w in hashtags and not w in ghashtags and not w in links and not w in mentions]
            wordFrequency = FreqDist(filtered_tokens)
            return wordFrequency
        except Exception as e:
            print("The exception occurred is: \t{0}".format(e))


# ------------< Execution starts here >------------

if __name__ == "__main__":
    # ------------< Paths to analyze >------------
    paths_to_analyze = ["./csv_files/commentsCSV_PewTop20V.csv",
                        "./csv_files/commentsCSV_Bitch Lasagna Song.csv",
                        "./csv_files/commentsCSV_Congratulations.csv",
                        "./csv_files/commentsCSV_Flare TV.csv",
                        "./csv_files/commentsCSV_TsrTop20V.csv",
                        "./csv_files/commentsCSV_Pewdiepie vs T Series.csv"]
    # ------------< Creating object of class >------------
    obj = CreatingWordCloud()

    # ------------< Analysis begins >------------
    for path in paths_to_analyze:
        obj.word_Cloud(path)