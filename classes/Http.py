import requests # make http requests
from classes.Color import Color
from bs4 import BeautifulSoup # for parsing the XML
import re
import os # for directory creation/path stuff
class Http():
    # Initialization:
    def __init__(self):
        self.color = Color()
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        self.interesting = ['backup','bak','api','token','key','secret','credentials','mfa','config',
        'passw','usern','azure','ldap','robots','temp','old','sensitive','priv','dev','test',
        'staging','donot','server-status','archive','archiva','filesystem','files','camera',
        'security','footage','adfs','topsec','sql','database','mariadb','postgre','sqlite','prod','multifactor',
        'authori','roles','smb','share','activedir','aws','s3','about.php','internal','intranet',
        'crypto','stash','logs','cache','session','account']

    # This returns an object that can be used for BeautifulSoup:
    def getxml(self,url):
        try:
            reqdata = requests.get(url,headers=self.headers) # get the URL
            # create the log directory:
            domain = re.sub('https?:..([^/]+).*',r'\1',url)
            file = domain+"/"+domain+"-sitemap.xml-urls.txt"
            if not os.path.isdir(domain):
                os.mkdir(domain)
            fh = open(file,"w") # open the file handler for logging
            soup = BeautifulSoup(reqdata.text,features="lxml") # send text of HTTP response into BS
            tags = soup.find_all("loc") # Pull out the "loc" tags only
            sitemaps = [] # store nested sitemaps
            sites = [] # to return for further inspection
            for site in tags: # loop over the "loc" tags and print the text only:
                sites.append(site.text)
                fh.write(site.text+"\n") # Write the site to the file.
                self.check4interesting(site.text) # check 4 interesting words
                # List nested sitemaps:
                if(re.search("sitemap.*\.xml",site.text)):
                    url2 = re.sub("(sitemap.*\.xml)",rf"{self.color.RED}\1{self.color.CMNT}",site.text)
                    print(f"{self.color.arrow()} Nested Sitemap: {url2}{self.color.RST}")
                    sitemaps.append(site.txt)
            fh.close() # close the file.
            self.color.ok(f"Log file written as {self.color.RED}\"{file}\"{self.color.LMGE} ({self.color.RED}{len(tags)}{self.color.RST} URLs discovered{self.color.LMGE}){self.color.RST}")
            # Crawl all nested sitemaps:
            if len(sitemaps)>0:
                if len(sitemaps)==1: # This is to check if only 1 sitemap and it's itself.
                    if sitemaps[0]==url:
                        pass
                else:
                    ans = input(f"{color.ques()} Would you like me to crawl nested sitemaps? {self.color.LMGE}({self.color.RED}{len(sitemaps)}{self.color.LMGE}) [{self.color.RED}y/n{self.color.LMGE}]? {self.color.RST}")
                    if ans == "y":
                        for sitemap in sitemaps:
                            self.color.ok(f"Crawling: {self.color.RED}{sitemap}{self.color.RST}")
                            http.getxml(sitemap) # grab the sitemap response object
                            file = re.sub("[?=&]","-",sitemap) # create a filename to store it.
                            file = re.sub("^.*(sitemap.*\.xml)",r"\1",file)
                            fh = open(domain+"/nested-sitemaps/"+file,"w") # open the file handler for logging
                            http.getxml(sitemap) # get the text of the nested sitemap
                            soup = BeautifulSoup(req.text,features="lxml") # parse the XML
                            tags = soup.find_all("loc")
                            for site in tags:
                                http.check4interesting(site.text,color)
                                fh.write(site.text+"\n")
                            fh.close() # close up the file.
            return sites
        except Exception as e:
            self.error(f"Fetching URL {url} failed: {e}")

    # Scraping actual source code of each page:
    def getCode(self,url):
        domain = re.sub('https?:..([^/]+).*',r'\1',url)
        file = re.sub('^https?:..[^/]+/','',url)
        file = domain+"/"+re.sub("/","-",file)+".txt"
        try:
            req = requests.get(url,headers=self.headers)
            fh = open(file,"a")
            fh.write(req.text+"\n")
            fh.close() # close up the file handle.
            return
        except Exception as e:
            self.error(f"Fetching URL {url} failed: {e}")


    # Check the URLs for interetsing terms:
    def check4interesting(self,url):
        for inter in self.interesting:
            if re.search(f"[/\._-]{inter}",url,re.IGNORECASE):
                url = re.sub(inter,self.color.RED+inter+self.color.LMGE,url)
                print(f"{self.color.info()}{self.color.CMNT} Interesting:{self.color.LMGE} {url}{self.color.RST}")
