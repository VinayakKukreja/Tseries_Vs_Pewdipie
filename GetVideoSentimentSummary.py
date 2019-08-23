'''''
--> Package Information:
    --------------------
    This package enables performing sentiment analysis of any video mentioned 
    via the youtube video id with the help of youtube_sentiment library

--> Version Control:
    ----------------
    Source:
    -------
        version 1.0, Date: April 23, 2019  
'''''

# ------------< Importing packages >------------

import youtube_sentiment as yt

# ------------< Enter Developer key here >------------

DEVELOPER_KEY = "AIzaSyBR6v1Mgb38r9UIdEfHtgpCEu0O9wa5jDs"

# ------------< Retrieving sentiment analysis summary via library >------------
yt.video_summary(DEVELOPER_KEY, "6Dh-RL__uN4", 5, "lr_sentiment_basic.pkl")
yt.video_summary(DEVELOPER_KEY, "6Dh-RL__uN4", 5, "lr_sentiment_cv.pkl")

temp = yt.video_summary(DEVELOPER_KEY, "dOsladVO250", 5, "lr_sentiment_basic.pkl")
