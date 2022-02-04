from sty import fg
class Color:
    def __init__(self):
        self.RED=fg(197) # pretty red
        self.YLL=fg(226) # pretty yellow
        self.RST='\033[0m' # reset the color to terminal default
        self.LMGE='\033[95m' # light magenta
        self.CMNT='\033[37m\033[3m' # comment-like text

    def arrow(self):
        return f"{self.CMNT}{self.RED}-->{self.CMNT}"
    def ques(self):
        return f"{self.LMGE}[{self.RED}?{self.LMGE}]{self.RST}"
    def info(self):
        return f"{self.LMGE}[{self.RED}i{self.LMGE}]{self.RST}"
    def ok(self,msg):
        print(f"\033[3m{fg(201)} ✔ {msg}{self.RST}")
    def fail(self,msg):
        print(f"\033[3m{fg(197)} ✖ {msg}{self.RST}")
