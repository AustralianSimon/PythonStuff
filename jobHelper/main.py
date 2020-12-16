#imports
import os
import glob
import docx
from docx2pdf import convert
import PyPDF2
import csv
import webbrowser


#configs
import config as cf


def run():
    getFiles(cf.fileLoc)

def setupReport(report, checkLoc):
    checkExists = os.path.exists(checkLoc + report)
    if checkExists == True:
        print('Deleting previous report.')
        os.remove(checkLoc + report)

def getFiles(check):
    tempLoc = os.getcwd() + '\\' + check
    os.chdir(tempLoc)
    setupReport(cf.reportFile, tempLoc)
    reportDict = {}
    fileList = []
    for file in glob.glob("*.docx"):
        #print(file)
        findName = os.path.basename(file)
        #Run resume rules
        if findName.lower().find('resume'):
            reportDict[file] = readPDF(findName)
            fileList.append(findName)
            #print('Resume found')
        #run cover letter rules
        elif findName.lower().find('cover'):
            reportDict[file] = readDoc(findName)
            fileList.append(findName)
            #print('Cover letter found')
        elif findName.lower().find('letter'):
            reportDict[file] = readDoc(findName)
            fileList.append(findName)
            #print('Cover letter found')
    scoreFile = writeScore(reportDict, fileList, cf.reportFile, tempLoc)
    #openResults(scoreFile)

def readDoc(file):
    doc = docx.Document(file)
    text = ""
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
        text = '\n'.join(fullText)

    if text == '':
        print('hi')

    analysisReport = analyser(text, cf.keyFile)
    return analysisReport

def readPDF(file):
    convert(file, "temp.pdf")
    print(file)
    pdfObj = open("temp.pdf", 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfObj)
    maxCount = pdfReader.numPages
    count = 0
    text = ''
    while count <= maxCount:
        pageObj = pdfReader.getPage(count)
        text.append(pageObj.extractText())
        count = count + 1
    print(text)
    os.remove("temp.pdf")
    if text == '':
        print('hi')

    analysisReport = analyser(text, cf.keyFile)
    return analysisReport


def analyser(text, keyFile):
    tempFile = os.getcwd() + '\\'
    keyFile = tempFile + keyFile
    with open(keyFile, 'r', newline='') as csvFile:
        keyWords = []
        csvData = csv.reader(csvFile, delimiter=',', quotechar='\"')
        for row in csvData:
            keyWords.append(row)
    scoreDict = {}
    print('The %s keywords used are:' % len(keyWords))
    print(keyWords)
    print(text)
    counter = 0
    while counter < len(keyWords):
        phrase = keyWords[counter][0]
        print(phrase.lower())
        result = text.lower().count(phrase.lower())
        scoreDict[phrase] = result
        #result = re.finditer(phrase, text, flags=0)
        #scoreDict[phrase] = len(result)
        counter = counter + 1
        print(counter)
    print('Printing score')
    print(scoreDict)
    return scoreDict

def writeScore(score, fileList, report, fileLoc):
    filename = fileLoc + report
    f = open(filename,'w')
    htmlWrapper = cf.htmlStructure
    tableString = """<tr><th style="border:1px solid black; border-collapse:collapse;">File Name</th><th style="border:1px solid black; border-collapse:collapse;">Key Phrase</th><th style="border:1px solid black; border-collapse:collapse;">Count</th></tr>"""
    print(score)
    for item in fileList:
        tableData = score[item]
        print(tableData)
        for result in tableData:
            colOne = item
            colTwo = result
            colThree = tableData[result]
            tableRow = """<tr><td style="border:1px solid black; border-collapse:collapse;">%s</td><td style="border:1px solid black; border-collapse:collapse;">%s</td><td style="border:1px solid black; border-collapse:collapse;">%s</td></tr>""" % (colOne, colTwo, colThree)
            tableString = tableString + tableRow
    #print(tableString)
    whole = htmlWrapper.format(code=tableString)
    f.write(whole)
    f.close()

def openResults(file):
    webbrowser.open(file, new=1)

if __name__ == '__main__':
        run()
        #try:
        #    run()
        #except:
        #    print('Something went wrong.')
        print('Finished running.')