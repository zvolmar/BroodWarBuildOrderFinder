from bs4 import BeautifulSoup
import requests
import re
import time

base = "https://liquipedia.net"
ext = "/starcraft/Category:Terran_Build_Orders"

tableTestUrl = "https://liquipedia.net/starcraft/1_Rax_FE_(vs._Protoss)"
listTestUrl = "https://liquipedia.net/starcraft/2_Port_Wraith"

url = base + ext
def getPage(url):

    response = requests.get(url)

    return response.text




def getListOfBuilds (url):

    builds = []
    page = getPage(url)
    soup = BeautifulSoup(page, 'html.parser')

    listBlock = soup.find('div', class_="mw-content-ltr")
    if listBlock is not None:
        for link in listBlock.find_all('a'):
            builds.append(link.get("href"))
        return builds
    else:
        print("Couldn't find block")
        return
        

sites = getListOfBuilds(base+ext)

def getBuildOrder():
    content = []
    for site in sites:

        tic = time.perf_counter()
        page = getPage(base+site)
        soup = BeautifulSoup(page, 'html.parser')
        headers = soup.find_all('h2')
        for i in headers:
            if i.find('span', id="Build_Order"):
                head = i

        if head.find_next_sibling("center"):
            parent = head.find_next_sibling("center")
            for line in parent.find_all(['ul', 'dt']):
                content.append(line.get_text())
        else:
            siblings = head.find_next_siblings("h2")
            for sibling in siblings:
                if sibling.name == "h2":
                    break
                else:
                    content.append(sibling.get_text())
        toc = time.perf_counter()
        print(f"Got page {base+site} in {toc - tic:0.4f} seconds")
            

    


getBuildOrder()