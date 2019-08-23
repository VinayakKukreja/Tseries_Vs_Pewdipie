'''''
--> Package Information:
    --------------------
    This package enables analysis of T-Series's Top 20 videos and plot graphs based
    on various criteria. For instance, videos in the order of most liked, most 
    disliked, most viewed, and most commented

--> Version Control:
    ----------------
    Source:
    -------
        version 1.0, Date: April 23, 2019  
'''''

# ------------< Importing packages >------------
from googleapiclient.discovery import build
import pandas as pd
import matplotlib.pyplot as plt
import time
from nltk.probability import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
import scipy
import pylab
import operator

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = ""
YOUTUBE_API_VERSION = ""
channelId = ""

#------------< Private Credentials required by youtube API >------------

def loginCredentials():
    global DEVELOPER_KEY
    DEVELOPER_KEY = "AIzaSyBJsW9LdfwvbYaHENbRUtb4wH4TVcLGw-g"
    global YOUTUBE_API_SERVICE_NAME
    YOUTUBE_API_SERVICE_NAME = "youtube"
    global YOUTUBE_API_VERSION
    YOUTUBE_API_VERSION = "v3"
    global channelId
    channelId = "UCq-Fj5jknLsUf-MWSy4_brA"

loginCredentials()
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

#------------< Getting videos from channel ID provided >------------

def get_videos_FromChanel(youtube, channelId, order):
    try:
        search_response = youtube.search().list(
            channelId=channelId,
            type="video",
            part="id,snippet",
            maxResults=50,
            order=order
        ).execute()

        return search_response.get("items", [])
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

videos = get_videos_FromChanel(youtube, channelId,"viewCount")

#------------< Getting comments from the videos IDs extracted earlier >------------

def get_comment_threads(youtube, videos):
    try:
        tempComments = []
        for video in videos:
            time.sleep(1.0)
            try:
                results = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video["id"]["videoId"],
                    textFormat="plainText",
                    maxResults=20,
                    order='relevance'
                ).execute()
            except:
                continue
            for item in results["items"]:
                comment = item["snippet"]["topLevelComment"]
                tempComment = dict(videoId=video["id"]["videoId"], videoName=video["snippet"]["title"],
                                   nbrReplies=item["snippet"]["totalReplyCount"],
                                   author=comment["snippet"]["authorDisplayName"], likes=comment["snippet"]["likeCount"],
                                   publishedAt=comment["snippet"]["publishedAt"],
                                   text=comment["snippet"]["textDisplay"].encode('utf-8').strip())
                tempComments.append(tempComment)
        return tempComments
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

#------------< Getting top 20 most viewed videos from the channel and plotting its graph >------------

def getVideoInfosForViewCount(videos):
    try:
        videoList = {}
        for search_result in videos:
             if search_result["id"]["kind"] == "youtube#video":
                 videoList[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
        s = ','.join(videoList.keys())
        videos_list_response = youtube.videos().list(id=s,part='id,statistics').execute()
        res = []
        for i in videos_list_response['items']:
             temp_res = dict(v_title = videoList[i['id']])
             temp_res.update(i['statistics'])
             res.append(temp_res)
        data = pd.DataFrame.from_dict(res)
        data['viewCount'] = data['viewCount'].map(lambda x : float(x))
        return data
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

infosView = getVideoInfosForViewCount(videos)

#------------< Plotting the graph for most viewed videos >------------

def plotVideoViewCountGraph(infosView):
    try:
        plt.rcParams["figure.figsize"] = (15,15)
        values = infosView.sort_values('viewCount', ascending=0).head(20).plot.bar(x='v_title',y='viewCount', color="Orange")
        values.set_xlabel("Most Viewed Videos")
        values.set_ylabel("View Count")
        plt.title("Top 20 most viewed videos of T-Series")
        plt.setp(values.get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.tight_layout()
        plt.savefig('./data/graphical_analysis_tseries/tseries_most_viewed.png')
        plt.show()
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

plotVideoViewCountGraph(infosView)


#------------< Getting top 20 most commented videos from the channel and plotting its graph >------------

def getVideoInfosForCommentCount(videos):
    try:
        videoList = {}
        for search_result in videos:
             if search_result["id"]["kind"] == "youtube#video":
                 videoList[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
        s = ','.join(videoList.keys())
        videos_list_response = youtube.videos().list(id=s,part='id,statistics').execute()
        res = []
        for i in videos_list_response['items']:
             temp_res = dict(v_title=videoList[i['id']])
             temp_res.update(i['statistics'])
             res.append(temp_res)
        data = pd.DataFrame.from_dict(res)
        data['commentCount'] = data['commentCount'].map(lambda x : float(x))
        return data
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

infosComment = getVideoInfosForCommentCount(videos)

#------------< Plotting the graph for most commented videos >------------

def plotVideoCommentCountGraph(infosComment):
    try:
        plt.rcParams["figure.figsize"] = (15,15)
        values = infosComment.sort_values('commentCount', ascending=0).head(20).plot.bar(x='v_title',y='commentCount', color="Green")
        values.set_xlabel("Most Commented Videos")
        values.set_ylabel("Comment Count")
        plt.title("Top 20 most commented videos of T-Series")
        plt.setp(values.get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.tight_layout()
        plt.savefig('./data/graphical_analysis_tseries/tseries_most_commented.png')
        plt.show()
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

plotVideoCommentCountGraph(infosComment)


#------------< Getting top 20 most liked videos from the channel and plotting its graph >------------

def getVideoInfosForLikesCount(videos):
    try:
        videoList = {}
        for search_result in videos:
             if search_result["id"]["kind"] == "youtube#video":
                 videoList[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
        s = ','.join(videoList.keys())
        videos_list_response = youtube.videos().list(id=s,part='id,statistics').execute()
        res = []
        for i in videos_list_response['items']:
             temp_res = dict(v_title=videoList[i['id']])
             temp_res.update(i['statistics'])
             res.append(temp_res)
        data = pd.DataFrame.from_dict(res)
        data['likeCount'] = data['likeCount'].map(lambda x : float(x))
        return data
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

infosLikes = getVideoInfosForLikesCount(videos)

#------------< Plotting the graph for most liked videos >------------

def plotVideoLikesCountGraph(infosLikes):
    try:
        plt.rcParams["figure.figsize"] = (15,15)
        values = infosLikes.sort_values('likeCount', ascending=0).head(20).plot.bar(x='v_title',y='likeCount', color="Blue")
        values.set_xlabel("Most Liked Videos")
        values.set_ylabel("Like Count")
        plt.title("Top 20 most liked videos of T-Series")
        plt.setp(values.get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.tight_layout()
        plt.savefig('./data/graphical_analysis_tseries/tseries_most_liked.png')
        plt.show()
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

plotVideoLikesCountGraph(infosLikes)

#------------< Getting top 20 most disliked videos from the channel and plotting its graph >------------

def getVideoInfosForDislikesCount(videos):
    try:
        videoList = {}
        for search_result in videos:
             if search_result["id"]["kind"] == "youtube#video":
                 videoList[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
        s = ','.join(videoList.keys())
        videos_list_response = youtube.videos().list(id=s,part='id,statistics').execute()
        res = []
        for i in videos_list_response['items']:
             temp_res = dict(v_title=videoList[i['id']])
             temp_res.update(i['statistics'])
             res.append(temp_res)
        data = pd.DataFrame.from_dict(res)
        data['dislikeCount'] = data['dislikeCount'].map(lambda x : float(x))
        return data
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

infosDislikes = getVideoInfosForDislikesCount(videos)

#------------< Plotting the graph for most disliked videos >------------

def plotVideoDislikesCountGraph(infosDislikes):
    try:
        plt.rcParams["figure.figsize"] = (15,15)
        values = infosDislikes.sort_values('dislikeCount', ascending=0).head(20).plot.bar(x='v_title',y='dislikeCount', color="Gold")
        values.set_xlabel("Most Disliked Videos")
        values.set_ylabel("Dislike Count")
        plt.title("Top 20 most disliked videos of T-Series")
        plt.setp(values.get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.tight_layout()
        plt.savefig('./data/graphical_analysis_tseries/tseries_most_disliked.png')
        plt.show()
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

plotVideoDislikesCountGraph(infosDislikes)

commentThreads = get_comment_threads(youtube,videos)
commentDataJson = pd.DataFrame.from_dict(commentThreads).to_json("./json_files/commentsJSON_TsrTop20V.json", orient="table")
commentDataCsv = pd.DataFrame.from_dict(commentThreads).to_csv("./csv_files/commentsCSV_TsrTop20V.csv", encoding='utf-8')

#------------< Getting top 20 most used words in the comments of videos retrieved >------------
def getMostUsedWords():
    try:
        all = pd.read_csv("./csv_files/commentsCSV_TsrTop20V.csv")
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
def plotMostUsedWordsGraph():
    try:
        fd = getMostUsedWords()
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
        plt.title("Top 20 used words in videos retrieved")
        plt.tight_layout()
        plt.savefig('./data/graphical_analysis_tseries/wordFrequency.png')
        fig.show()
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))

plotMostUsedWordsGraph()


#------------< Training data and Sentiment Analysis >------------

def word_feats(words):
    return dict([(word, True) for word in words])


def trainingClassifierNaiveBayes():
    try:
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')
        negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
        posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
        trainfeats = negfeats + posfeats
        classifier = NaiveBayesClassifier.train(trainfeats)
        all = pd.read_csv("./csv_files/commentsCSV_TsrTop20V.csv")
        all['tokenized'] = all['text'].apply(lambda x: [t.lower().strip(":,.!?") for t in x.split()])
        all['sentiment'] = all['tokenized'].apply(
            lambda x: classifier.prob_classify(word_feats(x)).prob('pos') - classifier.prob_classify(word_feats(x)).prob('neg'))
        videos = all.videoId.unique()
        for video in videos:
            tempDataFrame = all[all.videoId == video]
            videoname = tempDataFrame.iloc[0, 7]
            tempDataFrame.plot(kind='scatter', x='sentiment', y='likes', figsize=(15, 15))
            plt.title("Sentiment Analysis of " + videoname)
            plt.savefig('./data/sentiment_analysis_tseries/tseries_'+videoname+'.png')
            plt.show()
    except Exception as e:
        print("The exception occurred is: \t{0}".format(e))


trainingClassifierNaiveBayes()



