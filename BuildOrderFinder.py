from bs4 import BeautifulSoup
import requests
import re
import time

base = "https://liquipedia.net"
ext = "/starcraft/Category:Terran_Build_Orders"
#url = "https://liquipedia.net/starcraft/Category:Terran_Build_Orders"
tableTestUrl = "https://liquipedia.net/starcraft/1_Rax_FE_(vs._Protoss)"
listTestUrl = "https://liquipedia.net/starcraft/2_Port_Wraith"

url = base + ext
def  getPage(url):

    response = requests.get(url)

    return response.text





def getListOfBuilds (url):

    builds = []
    page = getPage(url)
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
        
#print(getListOfBuilds(url))
sites = getListOfBuilds(base+ext)

def getBuildOrder():
    i=1
    header = None
    notations = []
    references = []
    for site in sites:
        tic = time.perf_counter()
        page = getPage(base+site)
        soup = BeautifulSoup(page, 'html.parser')
        buildTable = soup.find("table", class_="wikitable collapsible")
        if buildTable == None:
            pass
        else:
            contents = buildTable.find_all(["tr"])
            header = contents[0].get_text()
            tutorialLink = contents[-1].get_text()
            references = contents[-2].get_text()
            notations = contents[1]
            splits = notations.find_all("tr")
            print(f"{len(splits)} at {site}")
            

            i+=1
    print(i)


        #toc = time.perf_counter()
        #print(f"Got page {base+site} in {toc - tic:0.4f} seconds")
            

    


getBuildOrder()