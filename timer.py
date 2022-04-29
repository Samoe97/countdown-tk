from email import header
from tkinter import *
from PIL import Image, ImageTk
import os
import pyglet
import urllib.request
import io
from datetime import datetime, timedelta

##### STYLES #####

updatableGuiElements = []

# COLORS

theme_light = {
    'textColor' : '#333333',
    'mainBg' : '#E6E6E6',
    'buttonColors' : [
        '#CCCCCC', 
        '#DDDDDD', 
        '#BBBBBB'
    ]
}

theme_dark = {
    'textColor' : '#EEEEEE',
    'mainBg' : '#222222',
    'buttonColors' : [
        '#555555', 
        '#666666', 
        '#444444'
    ]
}

theme = theme_dark

# FONTS

fontURL_MontserratMedium = 'https://samoe.me/font/montserrat/Montserrat-Medium.ttf'
montserratMediumRaw = urllib.request.urlopen(fontURL_MontserratMedium).read()
montserratMediumFile = io.BytesIO(montserratMediumRaw)
pyglet.font.add_file(montserratMediumFile)

fontURL_MontserratLight = 'https://samoe.me/font/montserrat/Montserrat-Light.ttf'
montserratLightRaw = urllib.request.urlopen(fontURL_MontserratLight).read()
montserratLightFile = io.BytesIO(montserratLightRaw)
pyglet.font.add_file(montserratLightFile)

##################

def getTime() :

    timeRef = datetime.now()
    currentTime = timeRef.strftime("%I : %M %p")
    return currentTime

def updateTimeVar() :

    currentTime = getTime()
    timeVar.set(currentTime)
    root.after(5000, updateTimeVar)

def updateLastClick(event) :

    global lastClickX
    global lastClickY
    lastClickX = event.x
    lastClickY = event.y

def drag(event) :

    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry('+' + str(int(x)) + '+' + str(int(y)))

def center(window, size, yoffset = 0) :

    x = (screen_width / 2) - size[0] / 2
    y = (screen_height / 2) - size[1] / 2 - yoffset
    window.geometry('+' + str(int(x)) + '+' + str(int(y)))

def switchTheme() :

    global theme
    if theme == theme_dark :
        theme = theme_light
    else :
        theme = theme_dark

    for i in updatableGuiElements :
        i.config(bg = theme['mainBg'])

        try :
            i.config(fg = theme['textColor'])
        except :
            pass

        try :
            if i.colors :
                i.colors = theme['buttonColors']
                i.config(bg = theme['buttonColors'][0])
        except :
            pass

    root.update()

def startTimer() :

    currentTime = datetime.now()

    timerValue = timerEntry.get()
    timerValue = timerValue.split(':')

    global timerTarget

    if len(timerValue) == 1 :
        timerTarget = currentTime + timedelta(seconds = int(timerValue))
    if len(timerValue) == 2 :
        timerTarget = currentTime + timedelta(minutes = int(timerValue[0]), seconds = int(timerValue[1]))
    if len(timerValue) == 3 :
        timerTarget = currentTime + timedelta(hours = int(timerValue[0]), minutes = int(timerValue[1]), seconds = int(timerValue[2]))

    updateTimer()

def updateTimer() :

    currentTime = datetime.now()

    currentValue = timerTarget - currentTime

    currentValue = str(currentValue)

    if not currentValue.__contains__('-1') :

        postDecimalCheck = currentValue.split('.')
        if len(postDecimalCheck) == 2 :
            postDecimalCheck[1] = postDecimalCheck[1][0:2]
            currentDecValue = '.' + postDecimalCheck[1]
        else :
            currentDecValue = '.00'

        doubleDigHourCheck = postDecimalCheck[0].split(':')
        if len(doubleDigHourCheck) == 3 :
            if int(doubleDigHourCheck[0]) < 10 :
                doubleDigHourCheck[0] = '0' + doubleDigHourCheck[0]
        currentValue = ''

        lenCheck = len(doubleDigHourCheck)
        index = 0
        for i in doubleDigHourCheck :
            index += 1
            if index != lenCheck :
                currentValue = currentValue + i + ':'
            else :
                currentValue = currentValue + i

        timerClockVar.set(currentValue)
        timerClockDecimalVar.set(currentDecValue)

        root.after(10, updateTimer)

    else :
        timerClockVar.set('00:00:00')
        timerClockDecimalVar.set('.00')

##################

class HoverButton(Label) :

    def on_hover(self, event):
        if self.selected == False :
                self.config(bg = self.colors[1])

    def on_unhover(self, event):
        if self.selected == False :
                self.config(bg = self.colors[0])
            
    def on_clicked(self, event):
        self.config(self, bg = self.colors[2])
        
        root.update()

        if self.command != None :
            self.command()

        if self.selectable == False :
            self.selected = False
            root.after(100, self.on_hover(self))

    def __init__(self, master, text, command = None, colors = theme['buttonColors']) :
        super(HoverButton, self).__init__(master)
        Label.config(self, text = text, highlightthickness = 0, bd = 0, relief = 'flat', bg = colors[0])
        self.colors = colors

        self.selectable = False
        self.selected = False

        self.command = command

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_unhover)
        self.bind("<Button-1>", self.on_clicked)

##################

root = Tk()
root.title("SAMOE'S COUNTDOWN TIMER")
root.minsize(840, 400)

root.config(bg = theme['mainBg'])

root.grid_rowconfigure(0, weight = 1)
root.grid_columnconfigure(0, weight = 1)

updatableGuiElements.append(root)

# root.resizable(width=False, height=False)
# root.attributes('-transparentcolor','#003200')

# root.overrideredirect(True)
# root.after(10, lambda: set_appwindow(mainWindow))

# bgImagePath = os.path.dirname(__file__) + '/timer-bg.png'
# bgImageRef = Image.open(bgImagePath)
# bgImageTk = ImageTk.PhotoImage(bgImageRef)

# bgImage = Label(root, image = bgImageTk)
# bgImage.place(x = 0, y = 0)
# bgImage.bind('<Button-1>', updateLastClick)
# bgImage.bind('<B1-Motion>', drag)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

rootSize = (int(screen_width / 3), int(screen_height / 3))
root.geometry(str(rootSize[0]) + 'x' + str(rootSize[1]))

center(root, rootSize, yoffset = int(screen_height / 32))

##########

rootFrame = Frame(root, bg = theme['mainBg'])
rootFrame.grid(column = 0, row = 0, sticky = 'NEWS', padx = 32, pady = 32)

rootFrame.grid_rowconfigure(0, weight = 1, minsize = 24)
rootFrame.grid_rowconfigure(1, weight = 500, minsize = 200)
rootFrame.grid_rowconfigure(2, weight = 1, minsize = 64)
rootFrame.grid_columnconfigure(0, weight = 1)

updatableGuiElements.append(rootFrame)

##########

headerFrame = Frame(rootFrame, bg = theme['mainBg'])
headerFrame.grid(column = 0, row = 0, sticky = 'NEWS')

headerFrame.grid_columnconfigure(0, weight = 1, minsize = 50)
headerFrame.grid_columnconfigure(1, weight = 500, minsize = 200)
headerFrame.grid_columnconfigure(2, weight = 1, minsize = 50)
headerFrame.grid_rowconfigure(0, weight = 1)

spacer = Frame(headerFrame, bg = theme['mainBg'], width = 50)
spacer.grid(column = 0, row = 0, sticky = 'NEWS')

timeVar = StringVar()
timeVar.set(getTime)

clockText = Label(headerFrame, fg = theme['textColor'], bg = theme['mainBg'], textvariable = timeVar, justify = 'c', font = ('Montserrat-Medium', 22))
clockText.grid(column = 1, row = 0, sticky = 'NEWS')

themeButton = HoverButton(headerFrame, text = 'Theme', colors = theme['buttonColors'], command = switchTheme)
themeButton.config(width = 4, height = 2)
themeButton.grid(column = 2, row = 0, sticky = 'NEWS')

updatableGuiElements.append(headerFrame)
updatableGuiElements.append(spacer)
updatableGuiElements.append(clockText)
updatableGuiElements.append(themeButton)

##########

timerFrame = Frame(rootFrame, bg = theme['mainBg'])
timerFrame.grid(column = 0, row = 1, sticky = 'NEWS')

timerFrame.grid_columnconfigure(0, weight = 1000)
timerFrame.grid_columnconfigure(1, weight = 1, minsize = 230)

timerClockVar = StringVar()
timerClockVar.set('00:00:00')

timerClockDecimalVar = StringVar()
timerClockDecimalVar.set('.00')

timerClock = Label(timerFrame, fg = theme['textColor'], bg = theme['mainBg'], justify = 'right', font = ('Montserrat-Light', 84), textvariable = timerClockVar)
timerClock.grid(column = 0, row = 0, sticky = 'NSE')

timerClockDecimal = Label(timerFrame, fg = theme['textColor'], bg = theme['mainBg'], justify = 'left', font = ('Montserrat-Light', 84), textvariable = timerClockDecimalVar)
timerClockDecimal.grid(column = 1, row = 0, sticky = 'NSW')

updatableGuiElements.append(timerClock)
updatableGuiElements.append(timerClockDecimal)
updatableGuiElements.append(timerFrame)

##########

controlsFrame = Frame(rootFrame, bg = theme['mainBg'])
controlsFrame.grid(column = 0, row = 2, sticky = 'NS')

controlsFrame.grid_columnconfigure(0, weight = 1)
controlsFrame.grid_columnconfigure(1, weight = 2)
controlsFrame.grid_columnconfigure(2, weight = 1)
controlsFrame.grid_rowconfigure(0, weight = 1, minsize = 40)
controlsFrame.grid_rowconfigure(1, weight = 1, minsize = 40)

resetButton = HoverButton(controlsFrame, text = 'RESET', colors = theme['buttonColors'])
resetButton.config(width = 8, height = 4, fg = theme['textColor'], font = ('Montserrat-Medium', 16))
resetButton.grid(column = 0, row = 0, padx = 24, pady = 16, sticky = 'NES')

playPauseButton = HoverButton(controlsFrame, text = 'START', colors = theme['buttonColors'], command = startTimer)
playPauseButton.config(width = 8, height = 4, fg = theme['textColor'], font = ('Montserrat-Medium', 16))
playPauseButton.grid(column = 1, row = 0, padx = 24, pady = 16, sticky = 'NEWS')

clearButton = HoverButton(controlsFrame, text = 'CLEAR', colors = ['#cc0000', '#ee0000', '#aa0000'])
clearButton.config(width = 8, height = 4, fg = 'white', font = ('Montserrat-Medium', 16))
clearButton.grid(column = 2, row = 0, padx = 24, pady = 16, sticky = 'NWS')

timerEntry = Entry(controlsFrame, bg = theme['mainBg'], fg = theme['textColor'], font = ('Montserrat-Medium', 16), width = 8, justify = 'c')
timerEntry.grid(column = 1, row = 1, ipady = 2)

timerEntry.insert('end', '00:00:00')

updatableGuiElements.append(controlsFrame)
updatableGuiElements.append(resetButton)
updatableGuiElements.append(playPauseButton)
updatableGuiElements.append(clearButton)
updatableGuiElements.append(timerEntry)

##########

updateTimeVar()
root.mainloop()