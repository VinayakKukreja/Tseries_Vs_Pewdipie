'''''
--> Package Information:
    --------------------
    This package enables to plot the data retrieved from the web scraping performed

--> Version Control:
    ----------------
    Source:
    -------
        version 1.0, Date: April 23, 2019  
'''''

# ------------< Importing packages >------------

import csv
from matplotlib import rcParams
import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt; plt.rcdefaults()
from threading import Thread


class plotWebScrape(Thread):

    # ------------< Plotting Web-Scraped data for PewDiPie >------------

    def plot_pew(self):
        xs = []
        ys = []
        with open('./data/web_scrape/plot_pew.csv', 'w') as outfile:
            pass
        with open('./data/web_scrape/pewdipie.csv', 'r') as textfile:
            for row in reversed(list(csv.reader(textfile))):
                if row[0] == 'Dates' and row[1] == 'SubscriberCount':
                    pass

                else:
                    with open('./data/web_scrape/plot_pew.csv', 'a') as outfile:
                        newStr = row[1].replace(",","")
                        outfile.writelines(newStr+','+row[0]+"\n")
                        xs.append(row[0])
                        ys.append(int(newStr))
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(xs, ys, label="PewDiPie")
            ax.set_xlabel("28-Jun-2014 to 26-Apr-2019")
            ax.set_ylabel("Subscribers Count")
            plt.xticks([])
            t = []
            for x in xs:

                if x == 'October 5, 2018':
                    ax.axvline(x, color='red', drawstyle='steps', marker='o')
                    t.append(x)
                    plt.xticks(t)
                if x == 'March 31, 2019':
                    ax.axvline(x, color='red', drawstyle='steps', marker='o')
                    t.append(x)
                    plt.xticks(t)

            fig.autofmt_xdate()
            rcParams['axes.titlepad'] = 20
            plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
            plt.title("Increase in growth percentage after PewDiPie's controversial songs")
            plt.legend()
            plt.tight_layout()
            plt.savefig("data/web_scrape/plot_pew.png", dpi=300)

    # ------------< Plotting Web-Scraped data for T-Series >------------
    def plot_ts(self):
        xs = []
        ys = []
        with open('./data/web_scrape/plot_ts.csv', 'w') as outfile:
            pass
        with open('./data/web_scrape/tseries.csv', 'r') as textfile:
            for row in reversed(list(csv.reader(textfile))):
                if row[0] == 'Dates' and row[1] == 'SubscriberCount':
                    pass
                else:
                    with open('./data/web_scrape/plot_ts.csv', 'a') as outfile:
                        newStr = row[1].replace(",","")
                        outfile.writelines(newStr+','+row[0]+"\n")
                        xs.append(row[0])
                        ys.append(int(newStr))
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(xs, ys, label="T-Series")
            ax.set_xlabel("28-Jun-2014 to 26-Apr-2019")
            ax.set_ylabel("Subscribers Count")
            plt.xticks([])
            t = []
            for x in xs:
                if x == 'October 5, 2018':
                    ax.axvline(x, color='red', drawstyle='steps', marker='o')
                    t.append(x)
                    plt.xticks(t)
                if x == 'March 31, 2019':
                    ax.axvline(x, color='red', drawstyle='steps', marker='o')
                    t.append(x)
                    plt.xticks(t)

            fig.autofmt_xdate()
            rcParams['axes.titlepad'] = 20
            plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
            plt.title("Increase in growth percentage after PewDiPie's controversial songs")
            plt.legend()
            plt.tight_layout()
            plt.savefig("data/web_scrape/plot_ts.png", dpi=300)

# ------------< Plotting Calls Begin Here >------------
plotWebScrape().plot_pew()
plotWebScrape().plot_ts()