## import configs & tools
import config
import searchers.seekAustralia as seekAUS


##import packages
#import requests
#from bs4 import BeautifulSoup as BS
import logging
import pandas as pd
import os

def loadJobs(fromLoc, toLoc):
    data1 = pd.read_csv(fromLoc, header=0)
    data2 = pd.read_csv(toLoc, header=0)
    mergedData = data1.append(data2)
    mergedData = mergedData.drop_duplicates('jobURL')
    print(mergedData)
    mergedData.to_csv(toLoc, index=False)

def runProcess():
    logging.info("Begin run process.")
    try:
        logging.info("Attempt seekAUS.")
        seekAUS
        urlFile = os.getcwd() + "\\searchers\\" + 'urls.csv'
        loadJobs(urlFile, 'uploads.csv')
    except BaseException as e:
        logging.error(str(e))






def run():
    print('Starting run.')
    runProcess()
    print('Finished.')

run()