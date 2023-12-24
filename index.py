from bs4 import BeautifulSoup
import requests
import main
import base64





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

    page = getPage(site)
    soup = BeautifulSoup(page, 'html.parser')
    header = site.replace('/starcraft/', '')
    header = header.replace('_', ' ')
    buildTable = soup.find("table", class_="wikitable collapsible")

    if buildTable != None:

        contents = buildTable.find_all(["tr"])
        #The second to last row is usually references (nullable)
        references = parseReferences(contents[-2])
        #The second row is always the notations (not nullable)
        notations = parseTableNotations(contents[1])
        
    else:

        span = soup.find("span", id="Build_Order")
        h = span.find_parent()
        ul = h.find_next_sibling("ul")
        notations = parseListNotations(ul)
        references = []

    print(f"Header: {header}\n\nNotations: {notations}\n\nReferences: {references}\n\n\n")



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

            uls.append(base64.b64encode("dl".encode()))
            entry_text = entry.find_previous_sibling().get_text()
            encoded_text = entry_text.encode()
            uls.append(base64.b64encode(encoded_text))

        else:
            #Normal list gets list label
            uls.append(base64.b64encode("list".encode()))

        #Converts resultset to string
        for line in entry.find_all('li'):
            uls.append(encodeText(line))

        entries.append(uls)
    return entries



def parseReferences(references):

    entries = []
    for entry in references.find_all('span', class_="reference-text"):
        entries.append(encodeText(entry))
    return entries



def parseListNotations(notations):

    entries = []
    for entry in notations.find_all("li"):
        entries.append(encodeText(entry))
    return entries



def encodeText(text):

    entry_text = text.get_text()
    encoded_text = entry_text.encode()
    final_text = (base64.b64encode(encoded_text))
    return final_text



def getBlacklist(path):

    blacklist = []
    file = open(path,'r')

    while True:
        line = file.readline()
        if not line:
            break
        blacklist.append(line.strip())
    return blacklist

