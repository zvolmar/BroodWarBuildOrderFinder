from bs4 import BeautifulSoup
import requests
import json
import re
import time
import numpy
import main




def getListOfBuilds(ext,blacklist):
  

    builds = []
    page = getPage(ext)
    soup = BeautifulSoup(page, 'html.parser')
    #Finds block full of links
    listBlock = soup.find('div', class_="mw-content-ltr")
    if listBlock is not None:
        for link in listBlock.find_all('a'):
            if link.get("href") not in blacklist:
                builds.append(link.get("href"))
        return builds
    else:
        print(f"Couldn't find block at {ext}")
        return



def getPage(ext):
    response = requests.get(main.base+ext)
    stuff = response.text
    response.close()
    return stuff



def getBuild(site, race):
    print(site)
    header = None
    notations = []
    references = []
    page = getPage(site)
    soup = BeautifulSoup(page, 'html.parser')
    header = site.replace("/starcraft/", '')
    header = site.replace("_", '')
    buildTable = soup.find("table", class_="wikitable collapsible")
    if buildTable != None:
        pass
        contents = buildTable.find_all(["tr"])

        #The first row is always the title (not nullable)
        header = contents[0].get_text()

        #The second to last row is usually references (nullable)
        if contents[-2] != None:
            references = parseReferences(contents[-2])

        #The second row is always the notations (not nullable)
        notations = parseTableNotations(contents[1])

        
    else:
        span = soup.find("span", id="Build_Order")
        h = span.find_parent()
        ul = h.find_next_sibling("ul")
        notations = parseListNotations(ul)



    print(handleJSON(header, race, notations, references))
    




def parseTableNotations(notations):
    #Gets the table cell that holds all the notations

    #Array of arrays to store build order
    #2D Array 
    entries = []
    for entry in notations.find_all('ul'):

        #Array to append to entries
        uls = []

        #Each list is checked to see if it's a boilerplate build order (list) or has variations (dt)

        #If cell header found, label the array with "dt" for cell
        if entry.find_previous_sibling('dl') or entry.find_previous_sibling('p'):
            uls.append("dt")
            uls.append(entry.find_previous_sibling().get_text())
        else:
            #Normal list gets list label
            uls.append("list")
        #Converts resultset to string
        for line in entry.find_all('li'):
            uls.append(line.get_text())

        entries.append(uls)
    return entries



def parseReferences(references):
    entries = []
    i=1
    for entry in references.find_all('span', class_="reference-text"):
        entries.append(f"{i}: {entry.get_text()}")
        i+=1
    return entries

def parseListNotations(notations):
    entries = []
    for entry in notations.find_all("li"):
        entries.append(entry.get_text())
    return entries

def getBlacklist(path):
    blacklist = []
    file = open(path,'r')
    while True:
        line = file.readline()
        if not line:
            break
        blacklist.append(line.strip())
    return blacklist


def handleJSON(head, race, nota, ref):
        jsonDict =  {
                        "title":head,
                        "race": race,
                        "notations":nota,
                        "references":ref
                    }
        obj = json.dumps(jsonDict, indent=4, separators=(',',':'))
        return obj