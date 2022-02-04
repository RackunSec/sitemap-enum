#!/usr/bin/env python3
# Sitemap-Enum - Enumeration Tool.
# Crawl and scrape sitemap.xml for URLs and store the source code of each.
# 2022 Douglas Berdeaux
#

import sys # get args from user
import re # matching
import os # for file creation
from bs4 import BeautifulSoup # for XML parsing
from classes.Color import Color
from classes.Error import Error
from classes.Http import Http

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

def main(args):
    color = Color()
    # check arguments:
    if len(args) == 1:
        usage(color)
    else:
        # set up variables:
        error = Error()
        http = Http()
        # grab the URL:
        if len(args)==2:
            url = args[1]
        else: # determine the URL
            for arg in args:
                if(re.match("^http.*\.xml",arg)):
                    url = arg
        # Check URL for correctedness:
        if re.match("^http.*\.xml",url):
            try: # scrape the sitemap first:
                sites = http.getxml(url) # make HTTP request for sitemap
                if len(args)==3: # scrape each individual link from the sitemap:
                    if args[1]=="--scrape" or args[2]=="--scrape":
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
