from sty import fg
class Color:
    def __init__(self):
        self.RED=fg(197)
        self.GRN=f"\033[3m{fg(201)} ✔ "
        self.YLL=fg(226)
        self.RST='\033[0m'
        self.LMGE='\033[95m'
        self.CMNT='\033[37m\033[3m'
        self.OKGRN=f"\033[3m{fg(46)} ✔ "
