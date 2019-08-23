'''''
--> Package Information:
    --------------------
    This package enables retrieval of comments from Video Names/ Video ID provided by the user
    and saving them to JSON as well as CSV format for further analysis

--> Version Control:
    ----------------
    Source:
    -------
        version 1.0, Date: April 23, 2019  
'''''

# ------------< Importing packages >------------

from googleapiclient.discovery import build
import pandas as pd
import traceback

# ------------< Getting comments by video name >------------

class GetAllComments:

    API_SERVICE_NAME = ""
    API_VERSION = ""
    DEVELOPER_KEY = ""
    youtube = None
    saved_page_token = None
    current_page_token = None
    video_id = ""
    filename = ""
    videoname = ""
    tempComments = []
    index = 0
    flag = 0

    # ------------< Constructor >------------

    def __init__(self):
        self.API_SERVICE_NAME = ""
        self.API_VERSION = ""
        self.DEVELOPER_KEY = ""
        self.youtube = None
        self.saved_page_token = None
        self.current_page_token = None
        self.video_id = ""
        self.filename = ""
        self.videoname = ""
        self.tempComments = []
        self.index = 0
        self.flag = 0

    # ------------< Setting API Service Name >------------

    def setAPI_SERVICE_NAME(self, API_SERVICE_NAME_R):
        self.API_SERVICE_NAME = API_SERVICE_NAME_R
        return self.API_SERVICE_NAME

    # ------------< Setting API Version >------------

    def setAPI_VERSION(self, API_VERSION_R):
        self.API_VERSION = API_VERSION_R
        return self.API_VERSION

    # ------------< Setting Developer Key >------------

    def setDeveloperKey(self, DEVELOPER_KEY_R):
        self.DEVELOPER_KEY = DEVELOPER_KEY_R
        return self.DEVELOPER_KEY

    # ------------< Setting value for YouTube build >------------

    def setYoutube(self, youtube_R):
        self.youtube = youtube_R
        return self.youtube

    # ------------< Running the first instance of comments retrieval and setting values >------------

    def Run(self, API_SERVICE_NAME_R, API_VERSION_R, DEVELOPER_KEY_R, youtube_R, name_R):
        self.tempComments.clear()
        self.API_SERVICE_NAME = self.setAPI_SERVICE_NAME(API_SERVICE_NAME_R)
        self.API_VERSION = self.setAPI_VERSION(API_VERSION_R)
        self.DEVELOPER_KEY = self.setDeveloperKey(DEVELOPER_KEY_R)
        self.youtube = self.setYoutube(youtube_R)
        self.setVideoID(name_R)
        try:
            match = self.get_comment_threads(self.youtube, self.video_id)
            if match == 1:
                raise Exception
            next_page_token = match["nextPageToken"]
            self.load_comments(match)
            self.getComments(next_page_token, match)
        except Exception as e:
            print("Exception in 1: \t{0}".format(e))
            newKey = self.switch_keys()
            self.youtube = self.buildAgain(newKey)
            match = self.get_comment_threads(self.youtube, self.video_id)
            while match == 1:
                match = self.get_comment_threads(self.youtube, self.video_id)
            next_page_token = match["nextPageToken"]
            self.saved_page_token = next_page_token
            self.load_comments(match)
            self.getComments(next_page_token, match)

    # ------------< Setting Video ID w.r.t Video Name received >------------

    def setVideoID(self, nameReceived):
        if nameReceived == "Flare TV":
            self.videoname = nameReceived
            self.video_id = "V2Afni3S-ok"
            self.filename = nameReceived.strip()
            self.filename = self.filename.replace("/", "")
        elif nameReceived == "Bitch Lasagna Song":
            self.videoname = nameReceived
            self.video_id = "6Dh-RL__uN4"
            self.filename = nameReceived.strip()
            self.filename = self.filename.replace("/", "")
        elif nameReceived == "Congratulations":
            self.videoname = nameReceived
            self.video_id = "PHgc8Q6qTjc"
            self.filename = nameReceived.strip()
            self.filename = self.filename.replace("/", "")
        elif nameReceived == "Pewdiepie vs T Series":
            self.videoname = nameReceived
            self.video_id = "dOsladVO250"
            self.filename = nameReceived.strip()
            self.filename = self.filename.replace("/", "")

    # ------------< Building the API call with values provided >------------

    def buildAgain(self, DEVELOPER_KEY_R):
        self.DEVELOPER_KEY = self.setDeveloperKey(DEVELOPER_KEY_R)
        self.youtube = build(self.API_SERVICE_NAME, self.API_VERSION, developerKey=self.DEVELOPER_KEY)
        return self.youtube

    # ------------< Functionality to switch keys if data limit for a key is reached >------------

    def switch_keys(self):
        self.index = self.index + 1
        DEVELOPER_KEYS = ["AIzaSyBJsW9LdfwvbYaHENbRUtb4wH4TVcLGw-g",
                          "AIzaSyBXZntmDOzjFTcy05m8H-PD_v26S9i7xV0",
                          "AIzaSyAxRh9HjEeYVnfyFypPmZ-o0omgxNo4pig",
                          "AIzaSyA88ITY494L5AK5a2qXnE9pcx-0U1J7OXo",
                          "AIzaSyA_upEvfP1nQrtrIZlsWzCuNKjN-CpW2aE",
                          "AIzaSyB6u2MbAP7D2faf77YPsx_A-oWz3yo2TsI",
                          "AIzaSyCQeOt1sn3EQ41khaYCj4GtJ3zu5Q-bF24",
                          "AIzaSyCQT1-HA-ObFP2-I8NwRg21otRXs17qqzQ",
                          "AIzaSyAOXVj_iOCNM3Cc3h54mPDgdbZh0EpwjAk",
                          "AIzaSyC2B6E2sMLDw_QpR73lsB0fyf15xfu_UE8",
                          "AIzaSyDfQlDehzE3LQoKiKQHztH7FIi-sTn8WdI",
                          "AIzaSyAE_Tvq5CnvEQn13xtiEdnDCb1XVEMbKt8",
                          "AIzaSyCldl6Q2cv_e-VvQFrT4D24IAMOJ4oy9J8",
                          "AIzaSyD5Errgc-rwY8c1e0PurjfWHtTcO67R6HY",
                          "AIzaSyBmxCr7YKeCt_qD69qv2M0Qd1Ua8xdLdbc",
                          "AIzaSyCxyXPcKgZ--7CM2jLy1-nfwRHLUMlKzBw",
                          "AIzaSyCB35W5cShnOv9Zq5IxPIdkKSEE65Jy2nA",
                          "AIzaSyAlx6d-kIJbZv_fEFLKba3wv-8FNse-TXo",
                          "AIzaSyBEshwo4tjTnMoZeMA6dfxV6qYjnHE-7FE",
                          "AIzaSyBR6v1Mgb38r9UIdEfHtgpCEu0O9wa5jDs"]

        if self.index >= DEVELOPER_KEYS.__len__():
            self.index = 0
        self.DEVELOPER_KEY = DEVELOPER_KEYS[self.index]
        return self.DEVELOPER_KEY

    # ------------< Loading comments to a format suitable for saving >------------

    def load_comments(self, match):
        for item in match["items"]:
            comment = item["snippet"]["topLevelComment"]
            self.tempComment = dict(videoId=self.video_id, videoName=self.videoname,
                               nbrReplies=item["snippet"]["totalReplyCount"],
                               author=comment["snippet"]["authorDisplayName"], likes=comment["snippet"]["likeCount"],
                               publishedAt=comment["snippet"]["publishedAt"],
                               text=comment["snippet"]["textDisplay"].encode('utf-8').strip())
            self.tempComments.append(self.tempComment)

    # ------------< Getting comment threads with a max limit of 100 results per request >------------

    def get_comment_threads(self, youtube, video_id, pageToken=""):
        try:
            results = youtube.commentThreads().list(
                part="snippet",
                pageToken=pageToken,
                maxResults=100,
                videoId=video_id,
                textFormat="plainText"
            ).execute()
            return results
        except:
            print("\n\n------------------------------------------------------------\n")
            print("\t Key exhausted, trying again!!")
            print("\n------------------------------------------------------------\n\n")
            newKey = self.switch_keys()
            self.youtube = self.buildAgain(newKey)
            try:
                results = youtube.commentThreads().list(
                    part="snippet",
                    pageToken=pageToken,
                    maxResults=100,
                    videoId=video_id,
                    textFormat="plainText"
                ).execute()
                return results
            except:
                return 1

    # ------------< Retrieving comments and saving to JSON and CSV formats when no nextPageToken is found >------------

    def getComments(self, next_page_token, match):
        try:
            while next_page_token:
                self.current_page_token = next_page_token
                print("\nPrevious page token: \t{0}\n".format(self.current_page_token))
                self.flag = self.flag + 1
                match = self.get_comment_threads(self.youtube, self.video_id, match["nextPageToken"])
                while match == 1:
                    if self.saved_page_token == self.current_page_token:
                        match = self.get_comment_threads(self.youtube, self.video_id, self.saved_page_token)
                    else:
                        match = self.get_comment_threads(self.youtube, self.video_id, self.current_page_token)
                print("\nCurrent VideoID:\t" + str(self.video_id) +" Videoname: "+ str(self.videoname))
                print("\nThe number of comments retrieved:\t" + str(self.flag) + "00")
                print("\nCurrent developer key is: \t{0}\n".format(self.DEVELOPER_KEY))
                if match != 1:
                    print("Next page token: \t{0}\n".format(next_page_token))
                    next_page_token = match["nextPageToken"]
                    self.load_comments(match)
            commentDataJson = pd.DataFrame.from_dict(self.tempComments).to_json("./json_files/commentsJSON_" + self.filename.strip() + ".json", orient="table")
            commentDataCsv = pd.DataFrame.from_dict(self.tempComments).to_csv("./csv_files/commentsCSV_" + self.filename.strip() + ".csv", encoding='utf-8')
        except Exception as e:
            print("Exception in 2 is:\t{0}".format(e))
            traceback.print_exc()
            commentDataJson = pd.DataFrame.from_dict(self.tempComments).to_json(
                "./json_files/commentsJSON_" + self.filename.strip() + ".json",
                orient="table")
            commentDataCsv = pd.DataFrame.from_dict(self.tempComments).to_csv("./csv_files/commentsCSV_" + self.filename.strip() + ".csv",
                                                                         encoding='utf-8')
            return

# ------------< Execution begins here >------------

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
DEVELOPER_KEY = "AIzaSyBJsW9LdfwvbYaHENbRUtb4wH4TVcLGw-g"
youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)
gettingComments = GetAllComments()

# ------------< Main Thread >------------

def main():
    name = "Flare TV"
    gettingComments.Run(API_SERVICE_NAME, API_VERSION, DEVELOPER_KEY, youtube, name)
    name = "Bitch Lasagna Song"
    gettingComments.Run(API_SERVICE_NAME, API_VERSION, DEVELOPER_KEY, youtube, name)
    name = "Congratulations"
    gettingComments.Run(API_SERVICE_NAME, API_VERSION, DEVELOPER_KEY, youtube, name)
    name = "Pewdiepie vs T Series"
    gettingComments.Run(API_SERVICE_NAME, API_VERSION, DEVELOPER_KEY, youtube, name)

if __name__ == "__main__":
    main()


