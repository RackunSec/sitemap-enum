from classes.Color import Color
# Display errors:
class Error():
    def __init__(self):
        self.color = Color() # store the object
    def say(self,msg):
        print(f"{self.color.RED} ERROR: {msg}{self.color.RST}")
