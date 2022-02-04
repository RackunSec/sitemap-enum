from sty import fg
class Style:
    def __init__(self):
        self.RED=fg(197) # pretty red
        self.YLL=fg(226) # pretty yellow
        self.RST='\033[0m' # reset the color to terminal default
        self.LMGE='\033[95m' # light magenta
        self.CMNT='\033[37m\033[3m' # comment-like text

    def arrow(self): # This is just " --> " but fancyier.
        return f"{self.CMNT}{self.RED}-->{self.CMNT}"
    def ques(self): # This just asks "[?]" much fancier:
        return f"{self.LMGE}[{self.RED}?{self.LMGE}]{self.RST}"
    def info(self): # This just says "[i]" much fancier:
        return f"{self.LMGE}[{self.RED}i{self.LMGE}]{self.RST}"
    def ok(self,msg): # This just says "[ok]" much fancier:
        print(f"\033[3m{fg(201)} ✔ {msg}{self.RST}")
    def fail(self,msg): # THis handles all failures during runtime
        print(f"\033[3m{fg(197)} ✖ {msg}{self.RST}")
    def banner(self): # Place ASCII art and app title:
        print(f"""
    {self.RED}

     oooooooo8 oooo     oooo ooooooooooo
    888         8888o   888   888    88
     888oooooo  88 888o8 88   888ooo8
            888 88  888  88   888    oo
    o88oooo888 o88o  8  o88o o888ooo8888
    {self.YLL}
    Sitemap Enumerator{self.RST}
        """)

    def usage(self):
        self.banner()
        print(f"{self.RED}[?] Usage: ./sitemap-enum.py (--scrape) (url){self.RST}\n")

