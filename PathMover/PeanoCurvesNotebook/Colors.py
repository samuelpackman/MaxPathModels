

class bcolors:
    Green = '\033[92m' #GREEN
    Yellow = '\033[93m' #YELLOW
    Red = '\033[91m' #RED
    Blue = '\033[94m' #Blue

    RESET = '\033[0m' #RESET COLOR

    CYAN = '\033[96m' #Cyan
    GREEN = '\033[92m' #Green

    Gray = '\033[2;232m'#]''\033[38;2;100;100;100m'
    Orange  = "\033[38;5;214m"

    HEADER = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def bYellow(string):
    return bcolors.Yellow + string + bcolors.RESET

def bBlue(string):
    return bcolors.Blue + string + bcolors.RESET

def bRed(string):
    return bcolors.Red + string + bcolors.RESET

def bGreen(string):
    return bcolors.GREEN + string + bcolors.RESET

def bGray(string):
    return bcolors.Gray + string + bcolors.RESET

def bOrange(string):
    return bcolors.Orange + string + bcolors.RESET
