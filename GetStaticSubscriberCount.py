'''''
--> Package Information:
    --------------------
    This package enables retrieval and saving of the current subscriber counts 
    and difference between sub-counts at the time between T-Series and 
    PewDiPie.

--> Version Control:
    ----------------
    Source:
    -------
        version 1.0, Date: April 23, 2019  
'''''

# ------------< Importing packages >------------

import json
import datetime
import matplotlib; matplotlib.use("TkAgg")
import googleapiclient.discovery
import matplotlib.pyplot as plt; plt.rcdefaults()
from threading import Thread

# ------------< Getting static subscriber count and difference >------------

class GettingSubscriberCount(Thread):

    def __init__(self):
        Thread.__init__(self)

    # ----------------------< Getting subscriber count at the current moment and saving in JSON format >--------------------

    def getSubscriberCount(self):
        try:
            api_service_name = "youtube"
            api_version = "v3"
            DEVELOPER_KEY = "AIzaSyBJsW9LdfwvbYaHENbRUtb4wH4TVcLGw-g"  # Enter your API developer key here

            youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

            # Requesting PewDiPie data
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id="UC-lHJZR3Gqxm24_Vd_AJ5Yw")
            response_pewdipie = request.execute()

            #Storing PewDiPie data
            with open('./data/static_analysis/pewdipie_subscriber_data.json', 'w', encoding='utf-8') as outfile:
                json.dump(response_pewdipie, outfile)

            # Requesting T-Series data
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id="UCq-Fj5jknLsUf-MWSy4_brA")
            response_tseries = request.execute()

            # Storing T-Series data
            with open('./data/static_analysis/tseries_subscriber_data.json', 'w', encoding='utf-8') as outfile:
                json.dump(response_tseries, outfile)

            # Retrieving respective subscriber counts
            pewDiPie_sub_count = response_pewdipie["items"][0]["statistics"]["subscriberCount"]
            tseries_sub_count = response_tseries["items"][0]["statistics"]["subscriberCount"]

            # Storing current subscriber count data
            file = open("./data/static_analysis/currentSubscriberCount.txt", "w", encoding='utf-8')
            file.writelines("PewDiPie Subscribers at {0} is: {1}\n".format(str(datetime.datetime.now()), pewDiPie_sub_count))
            file.writelines("T-Series Subscribers at {0} is: {1}\n".format(str(datetime.datetime.now()), tseries_sub_count))
            file.writelines("The Subscribers Difference at {0} is: {1}\n\n".format(str(datetime.datetime.now()), abs(int(tseries_sub_count)-int(pewDiPie_sub_count))))
            file.close()

        except Exception as e:
            print("The exception occured is: \t{0}".format(e))


# ------------< Execution starts here >------------
def main():
    sc = GettingSubscriberCount()
    sc.getSubscriberCount()

if __name__ == "__main__":
    main()