'''''
--> Package Information:
    --------------------
    This package enables to view the live subscriber count between T-Series and 
    PewDiPie through this code

--> Version Control:
    ----------------
    Source:
    -------
        version 1.0, Date: April 23, 2019  
'''''

# ------------< Importing packages >------------

import sys
import os
import time
import json
import datetime
import matplotlib; matplotlib.use("TkAgg")
import googleapiclient.discovery
import matplotlib.dates as mdates
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.animation as animation
from matplotlib import style
from threading import Thread

index = 0

# ------------< To switch keys if data limit is reached for the API >------------

def switch_keys():
    global index
    index = index + 1
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

    if index >= DEVELOPER_KEYS.__len__():
        index = 0
    DEVELOPER_KEY = DEVELOPER_KEYS[index]
    return DEVELOPER_KEY

# ------------< Functionality to save the dynamically retrieved subscriber information >------------

class myClass(Thread):
    def run(self):
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyCxyXPcKgZ--7CM2jLy1-nfwRHLUMlKzBw"  # Enter your API developer key here
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
        with open("./data/dynamic_analysis/PewDict.txt", "w"):
            pass
        with open("./data/dynamic_analysis/TsDict.txt", "w"):
            pass
        with open("./data/dynamic_analysis/currentSubscriberCount.txt", "a", encoding='utf-8'):
            pass
        with open('./data/dynamic_analysis/pewdipie_subscriber_data.json', 'w', encoding='utf-8') as pListfile:
            json.dump([], pListfile)
        with open('./data/dynamic_analysis/tseries_subscriber_data.json', 'w', encoding='utf-8') as tListfile:
            json.dump([], tListfile)
        print("Press Ctrl+C to stop dynamic retrieval of subscriber count: \t")
        print("\n")
        i = 0
        try:
            while True:
                i = i + 1
                print("Retrieval Cycle: \t{0}\n".format(i))
                request = youtube.channels().list(
                    part="snippet,contentDetails,statistics",
                    id="UC-lHJZR3Gqxm24_Vd_AJ5Yw")                      # ------------< Requesting PewDiPie's data >------------
                response_pewdipie = request.execute()
                with open('./data/dynamic_analysis/pewdipie_subscriber_data.json', 'r', encoding='utf-8') as routfile:
                    feeds = json.load(routfile)
                with open('./data/dynamic_analysis/pewdipie_subscriber_data.json', 'w', encoding='utf-8') as outfile:
                    feeds.append(response_pewdipie)
                    json.dump(feeds, outfile)
                request = youtube.channels().list(
                    part="snippet,contentDetails,statistics",
                    id="UCq-Fj5jknLsUf-MWSy4_brA")                      # ------------< Requesting T-Series data >------------
                response_tseries = request.execute()
                with open('./data/dynamic_analysis/tseries_subscriber_data.json', 'r', encoding='utf-8') as routfile:
                    feeds = json.load(routfile)
                with open('./data/dynamic_analysis/tseries_subscriber_data.json', 'w', encoding='utf-8') as woutfile:
                    feeds.append(response_tseries)
                    json.dump(feeds, woutfile)
                pewDiPie_sub_count = response_pewdipie["items"][0]["statistics"]["subscriberCount"]
                tseries_sub_count = response_tseries["items"][0]["statistics"]["subscriberCount"]
                date = mdates.date2num(datetime.datetime.now())
                file = open("./data/dynamic_analysis/currentSubscriberCount.txt", "a", encoding='utf-8')
                file.writelines("PewDiPie Subscribers at {0} is: {1}\n".format(date, pewDiPie_sub_count))
                file.writelines("T-Series Subscribers at {0} is: {1}\n".format(date, tseries_sub_count))
                file.writelines("The Subscribers Difference at {0} is: {1}\n\n".format(date, abs(
                    int(tseries_sub_count) - int(pewDiPie_sub_count))))
                file1 = open("./data/dynamic_analysis/PewDict.txt", "a")
                file1.writelines(str(i) + "," + pewDiPie_sub_count)
                file1.writelines("\n")
                file2 = open("./data/dynamic_analysis/TsDict.txt", "a")
                file2.writelines(str(i) + "," + tseries_sub_count)
                file2.writelines("\n")
                file.close()
                file1.close()
                file2.close()
                time.sleep(1)
        except Exception as e:
            print("The exception occured is: \t{0}".format(e))


# ------------< Functionality to animate data to display live subscriber count graph >------------

def animate(i):
    print("/nI:\t", i)
    pew_graph_data = open("./data/dynamic_analysis/PewDict.txt", "r").read()
    pew_lines = pew_graph_data.split("\n")
    pew_xs = []
    pew_ys = []
    j = []
    for line in pew_lines:
        if len(line) > 1:
            x, y = line.split(',')
            pew_xs.append(x)
            j.append(int(y))
            pew_ys.append(int(y))
    ts_graph_data = open("./data/dynamic_analysis/TsDict.txt", "r").read()
    ts_lines = ts_graph_data.split("\n")
    ts_xs = []
    ts_ys = []
    j = []
    for line in ts_lines:
        if len(line) > 1:
            x, y = line.split(',')
            ts_xs.append(x)
            j.append(int(y))
            ts_ys.append(int(y))
    ax.clear()
    bx.clear()
    plt.xlabel("Time in seconds")
    plt.ylabel("Subscriber Count")
    plt.autoscale(enable=True, axis='y', tight=None)
    ax.plot(pew_xs, pew_ys, color='blue', label='PewDiPie')
    ax.legend(loc='upper left')
    bx.plot(ts_xs, ts_ys, color='red', label='T-Series')
    bx.legend(loc='upper left')
    ax.set_xlim(left=max(0, i-10), right=None)
    bx.set_xlim(left=max(0, i - 10), right=None)
    fig.autofmt_xdate()
    return i


# ------------< Execution starts here >------------
if __name__=='__main__':
    try:
        style.use('fivethirtyeight')
        prev = 0
        flag = 0
        a=myClass()
        a.start()
        fig = plt.figure()
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
        fig.set_tight_layout(True)
        ax = fig.add_subplot(1, 2, 1)
        bx = fig.add_subplot(1, 2, 2)
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()
        if a.is_alive():
            os._exit(0)
            sys.exit(0)

    except Exception as e:
        print(e)



