'''''
--> Package Information:
    --------------------
    This package enables performing sentiment analysis of the data provided via 
    the csv files retrieved from analysis before

--> Version Control:
    ----------------
    Source:
    -------
        version 1.0, Date: April 23, 2019  
'''''

# ------------< Importing packages >------------

import pandas as pd
import matplotlib.pyplot as plt
from nltk.probability import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
import scipy
import pylab
import operator
import os


class SentimentAnalysis:

    #------------< Getting top 20 most used words in the comments of videos retrieved >------------

    def getMostUsedWords(self, path):
        try:
            all = pd.read_csv(path)
            stop_eng = stopwords.words('english')
            customstopwords = []
            tokens = []
            sentences = []
            tokenizedSentences =[]
            for txt in all.text:
                sentences.append(txt.lower())
                tokenized = [t.lower().strip(":,.!?") for t in txt.split()]
                tokens.extend(tokenized)
                tokenizedSentences.append(tokenized)
            hashtags = [w for w in tokens if w.startswith('#')]
            ghashtags = [w for w in tokens if w.startswith('+')]
            mentions = [w for w in tokens if w.startswith('@')]
            links = [w for w in tokens if w.startswith('http') or w.startswith('www')]
            filtered_tokens = [w for w in tokens if not w in stop_eng and not w in customstopwords and w.isalpha() and not len(w)<3 and not w in hashtags and not w in ghashtags and not w in links and not w in mentions]
            wordFrequency = FreqDist(filtered_tokens)
            return wordFrequency
        except Exception as e:
            print("The exception occurred is: \t{0}".format(e))

    #------------< Plotting graph for most used words >------------

    def plotMostUsedWordsGraph(self, path):
        try:
            fd = self.getMostUsedWords(path)
            sortedTuples = sorted(fd.items(), key=operator.itemgetter(1), reverse=True)
            a = [i[0] for i in sortedTuples[0:20]]
            b = [i[1] for i in sortedTuples[0:20]]
            plt.rcParams["figure.figsize"] = (15,15)
            x = scipy.arange(len(b))
            y = scipy.array(b)
            fig = pylab.figure()
            ax = fig.add_subplot(111)
            ax.bar(x, y, align='center')
            ax.set_xticks(x)
            ax.set_xticklabels(a)
            ax.set_xlabel("Words")
            ax.set_ylabel("Word Count")
            plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
            save_with_name = os.path.basename(os.path.normpath(path))
            plt.title("Top 20 used words in: "+ save_with_name)
            plt.tight_layout()
            plt.savefig('./data/graphical_analysis_videos/'+ save_with_name.strip() +'.png')
        except Exception as e:
            print("The exception occurred is: \t{0}".format(e))

    #------------< Training data and Sentiment Analysis >------------

    def word_feats(self, words):
        return dict([(word, True) for word in words])

    def trainingClassifierNaiveBayes(self, path):
        try:
            negids = movie_reviews.fileids('neg')
            posids = movie_reviews.fileids('pos')
            negfeats = [(self.word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
            posfeats = [(self.word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
            trainfeats = negfeats + posfeats
            classifier = NaiveBayesClassifier.train(trainfeats)
            all = pd.read_csv(path)
            all['tokenized'] = all['text'].apply(lambda x: [t.lower().strip(":,.!?") for t in x.split()])
            all['sentiment'] = all['tokenized'].apply(
                lambda x: classifier.prob_classify(self.word_feats(x)).prob('pos') - classifier.prob_classify(self.word_feats(x)).prob('neg'))
            videos = all.videoId.unique()
            if path == "./csv_files/commentsCSV_PewTop20V.csv" or path == "./csv_files/commentsCSV_TsrTop20V.csv":
                fl = 0
                for video in videos:
                    if fl >= 2:
                        break
                    tempDataFrame = all[all.videoId == video]
                    videoname = tempDataFrame.iloc[0, 7]
                    tempDataFrame.plot(kind='scatter', x='sentiment', y='likes', figsize=(15, 15))
                    plt.title("Sentiment Analysis of " + videoname)
                    noSpaceVideoName = videoname.strip()
                    noSpaceVideoName = noSpaceVideoName.replace("/", "")
                    plt.savefig('./data/sentiment_analysis_videos/'+noSpaceVideoName+'.png')
                    fl += 1
                    plt.show()
            else:
                for video in videos:
                    tempDataFrame = all[all.videoId == video]
                    videoname = tempDataFrame.iloc[0, 7]
                    tempDataFrame.plot(kind='scatter', x='sentiment', y='likes', figsize=(15, 15))
                    plt.title("Sentiment Analysis of " + videoname)
                    noSpaceVideoName = videoname.strip()
                    noSpaceVideoName = noSpaceVideoName.replace("/", "")
                    plt.savefig('./data/sentiment_analysis_videos/' + noSpaceVideoName + '.png')
                    plt.show()
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
    obj = SentimentAnalysis()

    # ------------< Analysis begins >------------
    for path in paths_to_analyze:
        obj.plotMostUsedWordsGraph(path)
        obj.trainingClassifierNaiveBayes(path)