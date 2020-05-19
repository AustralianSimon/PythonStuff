## import configs & tools
#import searchConfig as cf
seekAusURL = "https://www.seek.com.au/RPA-jobs/in-All-Australia"
checkString = "/job/"
seekjoburl = "https://www.seek.com.au"

##import packages
#import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import urllib3
import os

if __name__ == "__main__":
    urlFile = 'urls.csv'
    #urlFile = os.getcwd() + "\\" + 'urls.csv'
    print(urlFile)
else:
    urlFile = os.getcwd() + "\\searchers\\" + 'urls.csv'
    #urlFile = 'urls.csv'
    print(urlFile)


http = urllib3.PoolManager()

response = http.request('GET',seekAusURL)

soup = BS(response.data, 'html.parser')

#print(response.data)

csvList = []

for link in soup.find_all('div', href=True):
    #print(link)
    testBool = checkString in str(link)

    if testBool == True:
        #print("Found, slicing")
        location = str(link).find('href')
        #print(location)
        newlink = str(link)
        location2 = location + 6
        #print(newlink[location2:])
        newlink = newlink[location2:]
        endlocation = newlink.find('?type')
        #print(endlocation)
        endlocation2 = endlocation
        newlink = newlink[:endlocation2]
        #print(newlink)
        newlink = seekjoburl + newlink
        #print(newlink)
        csvList.append(newlink)

#print(csvList)
csvList = list(dict.fromkeys(csvList))

data1 = pd.read_csv(urlFile, header=0)
newDict = {}
newDict['jobURL'] = csvList
data2 = pd.DataFrame(newDict)
mergedData = data1.append(data2)
mergedData = mergedData.drop_duplicates('jobURL')
mergedData.to_csv(urlFile, index=False)
print('Seek Aussie RPA done')