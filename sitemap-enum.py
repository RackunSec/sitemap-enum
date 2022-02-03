#!/usr/bin/env python3
# Sitemap-Enum - Enumeration Tool.
# Crawl and scrape sitemap.xml for URLs and store the source code of each.
# 2022 Douglas Berdeaux
#
import requests # make http requests
import sys # get args from user
import re # matching
import os # for file creation
from bs4 import BeautifulSoup # for XML parsing
from sty import fg # cool colors!
# Placing this at the top of the file to be easily updated by users:
class Interesting:
    words = ['backup','bak','api','token','key','secret','credentials','mfa','config',
        'passw','usern','azure','ldap','robots','temp','old','sensitive','priv','dev','test',
        'staging','donot','server-status','archive','archiva','filesystem','files','camera',
        'security','footage','adfs','topsec','sql','database','mariadb','postgre','sqlite','prod','multifactor',
        'authori','roles','smb','share','activedir','aws','s3','about.php','internal','intranet',
        'crypto','stash','logs','cache','session','account']
# colors obj:
class Color:
    RED=fg(197)
    GRN=f"\033[3m{fg(201)} ✔ "
    YLL=fg(226)
    RST='\033[0m'
    LMGE='\033[95m'
    CMNT='\033[37m\033[3m'
    OKGRN=f"\033[3m{fg(46)} ✔ "

# Display errors:
class Error():
    def __init__(self,color):
        self.color = color # store the object
    def say(self,msg):
        print(f"{self.color.RED} ERROR: {msg}{self.color.RST}")

# store an HTTP response to a file:
class Http():
    def __init__(self,error):
        self.error = error # todo: add more headers here:
        self.headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
    def getxml(self,url):
        filename = re.sub('^https?:..','',url) + ".txt"
        filename = re.sub('/','-',filename)
        domain = re.sub('https?:..([^/]+).*',r'\1',url)
        if not os.path.isdir(domain):
            os.mkdir(domain)
        try:
            req = requests.get(url,headers=self.headers) # get the URL
            file = open(domain+"/"+filename,"w") # open the file for writing in new directory
            file.write(req.text+"\n") # write the response.
            file.close() # close it up.
        except Exception as e:
            print(e)
            self.error(f"Fetching URL {url} failed: {e}")
    def getCode(self,url):
        domain = re.sub('https?:..([^/]+).*',r'\1',url)
        file = re.sub('^https?:..[^/]+/','',url)
        file = domain+"/"+re.sub("/","-",file)+".txt"
        # file is good.
        try:
            req = requests.get(url,headers=self.headers)
            fh = open(file,"a")
            fh.write(req.text+"\n")
            fh.close() # close up the file handle.
            return
        except Exception as e:
            self.error(f"Fetching URL {url} failed: {e}")

# simple usage:
def usage(color):
    print(f"""{color.RED}

     oooooooo8 oooo     oooo ooooooooooo
    888         8888o   888   888    88
     888oooooo  88 888o8 88   888ooo8
            888 88  888  88   888    oo
    o88oooo888 o88o  8  o88o o888ooo8888
    {color.YLL}
    Sitemap Enumerator{color.RST}
    """)
    print(f"{color.RED}[?] Usage: ./sitemap-enum.py --scrape (url){color.RST}\n")
    sys.exit(1)

def check4interesting(url,color):
    interesting = Interesting() # for interesting.words[]
    for inter in interesting.words:
        if re.search(f"[/\._-]{inter}",url,re.IGNORECASE):
            url = re.sub(inter,color.RED+inter+color.LMGE,url)
            print(f"{color.GRN}{color.CMNT} Interesting:{color.LMGE} {url}{color.RST}")

def main(args):
    color = Color()
    # check arguments:
    if len(args) == 1:
        usage(color)
    else:
        error = Error(color)
        http = Http(error)

        if len(args)==2:
            url = args[1]
        else: # determine the URL
            for arg in args:
                if(re.match("^http.*\.xml",arg)):
                    url = arg
        if re.match("^http.*\.xml",url):
            try:
                domain = re.sub('^https?:..([^/]+).*',r'\1',url)
                sites = [] # store the sites
                sitemaps = [] # store nested sitemaps
                req = requests.get(url) # make HTTP request for sitemap
                if req.status_code!=200: # if not found (I think except would pick this up too):
                    error.say(f"URL not accessible. Got response code: {req.status_code}")
                else:
                    soup = BeautifulSoup(req.text,features="lxml") # send text of HTTP response into BS
                    tags = soup.find_all("loc") # Pull out the "loc" tags only
                    filename = domain+"-sitemap.xml-urls.txt"
                    file = open(filename,"a")
                    for site in tags: # loop over the "loc" tags and print the text only:
                        sites.append(site.text) # add the site to oour list
                        file.write(site.text+"\n") # Write the site to the file.
                        check4interesting(site.text,color) # check 4 interesting words
                        # List nested sitemaps:
                        if(re.search("sitemap.*\.xml",site.text)):
                            sitemaps.append(site.text) # add the nested sitemap to crwal later.
                            url = re.sub("(sitemap.*\.xml)",rf"{color.RED}\1{color.CMNT}",site.text)
                            print(f"{color.CMNT}{color.RED}-->{color.CMNT} Nested Sitemap: {url}{color.RST}")
                    file.close()
                    # Crawl all nested sitemaps:
                    if len(sitemaps)>0:
                        ans = input(f"{color.LMGE}[{color.RED}?{color.LMGE}]{color.RST} Would you like me to crawl nested sitemaps? {color.LMGE}({color.RED}{len(sitemaps)}{color.LMGE}) [{color.RED}y/n{color.LMGE}]? {color.RST}")
                        if ans == "y":
                            # Crate a space to log these nested sitemaps:
                            if not os.path.isdir(domain):
                                os.mkdir(domain)
                            if not os.path.isdir(domain+"/nested-sitemaps"):
                                os.mkdir(domain+"/nested-sitemaps") # make the directory
                            for sitemap in sitemaps:
                                print(f"{color.OKGRN}{color.RST} Crawling: {color.RED}{sitemap}{color.RST}")
                                check4interesting(sitemap,color)
                                file = re.sub("[?=&]","-",sitemap)
                                file = re.sub("^.*(sitemap.*\.xml)",r"\1",file)
                                fh = open(domain+"/nested-sitemaps/"+file,"w") # open the file handler for logging
                                req = requests.get(sitemap) # get the text of the nested sitemap
                                soup = BeautifulSoup(req.text,features="lxml") # parse the XML
                                tags = soup.find_all("loc")
                                for site in tags:
                                    check4interesting(site.text,color)
                                    fh.write(site.text+"\n")
                                fh.close() # close up the file.


                    print(f"{color.OKGRN} Log file written as {color.RED}\"{filename}\"{color.LMGE} ({color.RED}{len(sites)}{color.RST} URLs discovered{color.LMGE}){color.RST}")
                    if len(args)==3:
                        if args[1]=="--scrape" or args[2]=="--scrape":
                            if not os.path.isdir(domain): # check if it exists
                                os.mkdir(domain) # create a place to put them
                            i = 0
                            for url in sites: # loop over all URLs pulled from XML file
                                i=i+1 # token for math below:
                                percentdone = round((i/len(sites))*100,2)
                                print(f"{color.CMNT}Scraping sites:{color.RED} {percentdone}% {color.LMGE}{i}{color.CMNT}/{color.LMGE}{len(sites)}{color.RST} ...                        \r",end="")
                                http.getCode(url)
                            print(f"{color.OKGRN} Scraping completed.                             {color.RST}")
            except Exception as e: # let the user know what happened:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                error.say(f"Something went wrong: {e} {exc_tb.tb_lineno}")
        else: # Not a .xml file and URL:
            error.say(f"Malformed XML URL: {args[1]}")

if __name__ == "__main__": # Our main function.
    main(sys.argv)
