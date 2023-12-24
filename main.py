import index as ind


base = "https://liquipedia.net"
terran = ["terran", "/starcraft/Category:Terran_Build_Orders", "blacklists/terran.txt"]
protoss = ["protoss", "/starcraft/Category:Protoss_Build_Orders", "blacklists/protoss.txt"]
zerg = ["zerg", "/starcraft/Category:Zerg_Build_Orders", "blacklists/zerg.txt"]



#Builds that need manual formatting:
# 3 Factory Goliaths/5 Factory Goliaths (nested lists)
# Deep Six (has three dl lists but only the first two are displayed in-line)
# Fake Fake Double Build (p element at end of list, not part of list)
# Hiya Four Factory (this one's a mess)
# 2 Gate DT vs Protoss (only build where header name is Build Orders, with an s)
# Protoss Fast Expand vs Terran

#Talk to M
# Fantasy Build
# Iloveoov
# Proxy 5 Rax
# SCV Rush



def main():
    current = terran
    blacklist = ind.getBlacklist(current[2])
    sites = ind.getListOfBuilds(current[1],blacklist)
    for site in sites:
        post = ind.getBuild(site, current[0])
        if post != None:
            print(post)
    print("Finished")



if __name__ == '__main__':
    main()