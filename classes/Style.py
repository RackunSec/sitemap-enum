from sty import fg
import re # for variable message colors
class Style:
    def __init__(self):
        self.RED=fg(197) # pretty red
        self.YLL=fg(226) # pretty yellow
        self.GRN=fg(46) # nice green color
        self.RST='\033[0m' # reset the color to terminal default
        self.LMGE='\033[95m' # light magenta
        self.CMNT='\033[37m\033[3m' # comment-like text
        self.PPIN=fg(171) # purplish-pink
        self.PPUR=fg(135) # nice purple
        self.PINK=fg(201) # pink color
        self.NET=self.PPUR+' 🖧  '+self.RST # show network icon
        self.FILE=self.PPUR+' 🗁  '+self.RST # Show file icon
        self.OK = f"\033[3m{fg(200)}" # OK text color only

    ## Print an arrow for indentation:
    def arrow(self): # This is just " --> " but fancyier.
        return f"{self.CMNT}{self.RED} →{self.CMNT}"

    ## Prompt User for Question:
    def ques(self): # This just asks "[?]" much fancier:
        return f"{self.PINK}[{self.PPUR}?{self.PINK}]{self.RST}"

    ## Print Information to user:
    def info(self): # This just says "[i]" much fancier:
        return f"{self.PINK}[{self.PPUR}i{self.PINK}]{self.RST}"

    ## Print [ OK ]
    def ok(self,msg): # This just says "[ok]" much fancier:
        print(f"\033[3m{fg(200)} ✔ {fg(201)}{msg}{self.RST}")

    ## Print Failures:
    def fail(self,msg): # This handles all failures during runtime
        msg = re.sub("([\[\]])",f"{self.LMGE}\\1{self.RED}",msg) # color the brackets
        msg = re.sub("([\(\)])",f"{self.LMGE}\\1{self.RED}",msg) # color the brackets
        print(f"\033[3m{fg(196)} ✖ {self.RED}{msg}{self.RST}")

    ## Print headings:
    def header(self,msg): # 28 total
        header_len = len(msg)
        divider = f"\n{self.RED}+"
        for i in range(13):
            divider += f"{self.PPIN}-{self.PPUR}-"
        divider += f"{self.RED}+{self.RST}\n"
        print(divider+f"{self.PINK}▒ {msg} {' ' * (23-header_len)} ▒{self.RST}"+divider)


    def usage(self,title):
        print(f"""{self.RED}
     oooooooo8 oooo     oooo ooooooooooo
    888         8888o   888   888    88
     888oooooo  88 888o8 88   888ooo8
            888 88  888  88   888    oo
    o88oooo888 o88o  8  o88o o888ooo8888

    {self.LMGE}{title}{self.RST}
        """)
        ## Update the following for your specific app's usage:
        self.header("HELP CMD")
        usage = "Usage: ./sitemap-enum.py (--scrape) (url)"
        ## This will color it for you:
        usage = re.sub("([\[\]])",f"{self.LMGE}\\1{self.CMNT}",usage) # color the brackets
        usage = re.sub("([\(\)])",f"{self.LMGE}\\1{self.CMNT}",usage) # color the brackets
        usage = re.sub("(./[^\s]+)",f"{self.GRN}\\1{self.RST}",usage) # color the brackets
        usage = f"{self.CMNT} "+usage
        print(f"{self.ques()}{usage}{self.RST}\n")
