from __future__ import print_function
import io
from datetime import datetime

INPUT_FILE = "harsha.txt"

def stripInvalidChar(inputFile):
    outputFile = inputFile[:-4] + "_parsed.txt"
    with io.open(inputFile,'r',encoding='utf-8',errors='ignore') as infile, \
         io.open(outputFile,'w',encoding='ascii',errors='ignore') as outfile:
        for line in infile:
            print(*line.split(), file=outfile)
    return outputFile

def isNewMsg(line):
    return len(line) > 2 and (line[1] == '/' or line[2] == '/')

def whoSend(msgLine):
    dashI = msgLine.find(' - ')
    nextSlice = msgLine[dashI + 3:]
    return nextSlice[:nextSlice.find(':')]

def whatMsg(msgLine):
    return msgLine[msgLine.find(':', msgLine.find(':') + 1) + 2:]

def main(inputFile, profileName):
    myData = []
    newFile = stripInvalidChar(inputFile)
    outFile = newFile[:-4] + ".out"
    f = open(stripInvalidChar(inputFile))
    g = open(outFile, 'w')

    currentSender = ""
    currentMsg = ""
    prevSender = ""
    
    for line in f:
        line = line.strip()
        if not isNewMsg(line):
            currentMsg += " " + line
        else:
            if prevSender == currentSender:
                #myData.append("")
                g.write("\n")

            #myData.append(currentMsg)
            g.write(currentMsg + "\n")
            prevSender = currentSender
            
            currentSender = whoSend(line)
            currentMsg = whatMsg(line)
    f.close()
    g.close()
    return myData

main(INPUT_FILE, "Duc Vu")
