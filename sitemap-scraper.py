#!/usr/bin/env python3
# Sitemap-Scraper - Enumeration Tool.
# Scrape sitemap.xml for URLs and store the source code of each.
#
# 2022 Douglas Berdeaux
import requests # make http requests
import sys # get args from user
import re # matching
import os # for file creation
from bs4 import BeautifulSoup # for XML parsing
# simple usage:
def usage():
    print("Usage: ./sitemap-scraper.py --scrape (url)")
# store an HTTP response to a file:
def httpget(url,domain):
    filename = re.sub('^https?:..','',url) + ".txt"
    filename = re.sub('/','-',filename)
    try:
        req = requests.get(url) # get the URL
        file = open(domain+"/"+filename,"w") # open the file for writing in new directory
        file.write(req.text+"\n") # write the response.
        file.close() # close it up.
    except Exception as e:
        error(f"Fetching URL {url} failed: {e}")
# display errors:
def error(msg):
    print(f"ERROR: {msg}")
# check arguments:
if len(sys.argv) == 1:
    usage()
else:
    if len(sys.argv)==2:
        url = sys.argv[1]
    else: # determine the URL
        for arg in sys.argv:
            if(re.match("^http.*\.xml",arg)):
                url = arg
    if re.match("^http.*\.xml",url):
        try:
            domain = re.sub('^https?:..([^/]+).*',r'\1',url)
            sites = [] # store the sites
            req = requests.get(url) # make HTTP request for sitemap
            if req.status_code!=200: # if not found (I think except would pick this up too):
                error(f"URL not accessible. Got reaponse code: {req.status_code}")
            else:
                soup = BeautifulSoup(req.text,features="lxml") # send text of HTTP response into BS
                tags = soup.find_all("loc") # Pull out the "loc" tags only
                filename = domain+"-sitemap.xml-urls.txt"
                file = open(filename,"a")
                for site in tags: # loop over the "loc" tags and print the text only:
                    sites.append(site.text) # add the site to oour list
                    file.write(site.text+"\n") # Write the site to the file.
                file.close()
                print(f"[i] Log file written as {filename} ({len(sites)} URLs discovered)")
                if len(sys.argv)==3:
                    if sys.argv[1]=="--scrape" or sys.argv[2]=="--scrape":
                        os.mkdir(domain) # create a place to put them
                        i = 0
                        for url in sites:
                            i=i+1
                            percentdone = round((i/len(sites))*100,2)
                            print(f"Scraping sites: {percentdone}% {i}/{len(sites)} ...                        \r",end="")
                            httpget(url,domain)
                        print("[i] Scraping completed.                             ")
        except Exception as e: # let the user know what happened:
            error(f"Something went wrong: {e}")
    else: # Not a .xml file and URL:
        error(f"Malformed URL: {url}")
