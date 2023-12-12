from bs4 import BeautifulSoup
import requests
import json
import re
import time
import numpy

base = "https://liquipedia.net"
terran = "/starcraft/Category:Terran_Build_Orders"
protoss = "/starcraft/Category:Protoss_Build_Orders"
zerg = "/starcraft/Category:Zerg_Build_Orders"



#Builds that need manual formatting:
# 3 Factory Goliaths/5 Factory Goliaths (nested lists)
# 4 Barracks Sunken Break (table cell headers are p, not dl)
# Deep Six (has three dl lists but only the first two are displayed in-line)
# Fake Fake Double Build (table cell headers are p, not dl)
# Hiya Four Factory (this one's a mess)

#Blacklist
# TVPBuilds
# Terran Strategy


def main():
    current = terran
    sites = getListOfBuilds(current)
    i = 0
    for site in sites:
        print(f"{i}: {site}")
        i+=1
    for site in sites:
        post = getBuild(site, "terran")
        if post != None:
            print(post)
            #pass
            
            



def getListOfBuilds(ext):
    blacklist = ["/starcraft/Terran_Strategy", "/starcraft/TVPBuilds"]
    builds = []
    page = getPage(ext)
    soup = BeautifulSoup(page, 'html.parser')
    #Finds block full of links
    listBlock = soup.find('div', class_="mw-content-ltr")
    if listBlock is not None:
        for link in listBlock.find_all('a'):
            print(link)
            if link.get("href") not in blacklist:
                builds.append(link.get("href"))
        return builds
    else:
        print(f"Couldn't find block at {ext}")
        return



def getPage(ext):
    response = requests.get(base+ext)
    stuff = response.text
    response.close()
    return stuff



def getBuild(site, race):
    header = None
    notations = []
    references = []
    page = getPage(site)
    soup = BeautifulSoup(page, 'html.parser')
    buildTable = soup.find("table", class_="wikitable collapsible")
    if buildTable != None:
        contents = buildTable.find_all(["tr"])

        #The first row is always the title (not nullable)
        header = contents[0].get_text()

        #The second to last row is usually references (nullable)
        if contents[-2] != None:
            references = parseReferences(contents[-2])

        #The second row is always the notations (not nullable)
        notations = parseNotations(contents[1])

        jsonDict =  {
                        "title":header,
                        "race": race,
                        "notations":notations,
                        "references":references
                    }
        obj = json.dumps(jsonDict, indent=4, separators=(',',':'))
        return obj
    else:
        return



def parseNotations(notations):
    #Gets the table cell that holds all the notations

    #Array of arrays to store build order
    #2D Array 
    entries = []
    for entry in notations.find_all('ul'):

        #Array to append to entries
        uls = []

        #Each list is checked to see if it's a boilerplate build order (list) or has variations (dt)

        #If cell header found, label the array with "dt" for cell
        if entry.find_previous_sibling('dl'):
            uls.append("dt")
            uls.append(entry.find_previous_sibling('dl').get_text())
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



if __name__ == '__main__':
    main()