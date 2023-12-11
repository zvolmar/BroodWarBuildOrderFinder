from bs4 import BeautifulSoup
import requests
import re
import time
import numpy

base = "https://liquipedia.net"
terran = "/starcraft/Category:Terran_Build_Orders"
protoss = "/starcraft/Category:Protoss_Build_Orders"
zerg = "/starcraft/Category:Zerg_Build_Orders"








def main():
    current = terran
    sites = getListOfBuilds(current)
    for site in sites:
        print(getBuild(site, "terran"))



def getPage(ext):

    response = requests.get(base+ext)

    return response.text


def getListOfBuilds(ext):

    builds = []
    page = getPage(ext)
    print(f"Arrived at {ext}")
    soup = BeautifulSoup(page, 'html.parser')
    #Finds block full of links
    listBlock = soup.find('div', class_="mw-content-ltr")
    if listBlock is not None:
        for link in listBlock.find_all('a'):
            builds.append(link.get("href"))
        return builds
    else:
        print("Couldn't find block")
        return

def getBuild(site, race):
    header = None
    notations = []
    references = []
    page = getPage(base+site)
    soup = BeautifulSoup(page, 'html.parser')
    buildTable = soup.find("table", class_="wikitable collapsible")
    if buildTable != None:
        contents = buildTable.find_all(["tr"])

        #The first row is always the title (not nullable)
        header = contents[0].get_text()

        #The second to last row is usually references (nullable)
        references = parseReferences(contents[-2])

        #The second row is always the notations (not nullable)
        notations = parseNotations(contents[1])

        jsonDict =  {
                        "title":header,
                        "race": race,
                        "notations":notations,
                        "references":references
                    }
        return jsonDict
    else:
        print(f"Table not found at {page}")


def parseNotations(notations):
    #Gets the table cell that holds all the notations

    #Array of arrays to store build order
    #2D Array 
    entries = numpy.array()
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
            uls.append(line)

    entries.append(uls)
    return entries

        
def parseReferences(references):
    entries = []
    for entry in references.find('li'):
        entries.append(entry.get_text())
    return entries




if __name__ == '__main__':
    main()