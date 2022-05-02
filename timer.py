from tkinter import *
import pyglet
import urllib.request
import io
from datetime import datetime, timedelta

playing = False
paused = False

##### STYLES #####

updatableGuiElements = [] # ADD ANY WIDGETS TO BE MODIFIED BY THE THEME TO THIS LIST

# COLORS

theme_light = {
    'name' : 'light', # THEME NAME
    'textColor' : '#333333', # TEXT COLOR
    'mainBg' : '#E6E6E6', # BACKGROUND
    'buttonColors' : [
        '#CCCCCC', # IDLE
        '#DDDDDD', # HOVERED
        '#BBBBBB'  # CLICKED
    ]
}

theme_dark = {
    'name' : 'dark',
    'textColor' : '#EEEEEE',
    'mainBg' : '#222222',
    'buttonColors' : [
        '#555555', 
        '#666666', 
        '#444444'
    ]
}

theme_blue_dark = {
    'name' : 'blue_dark',
    'textColor' : '#FFFFFF',
    'mainBg' : '#3D4855',
    'buttonColors' : [
        '#E79F6D',
        '#EFAA7F',
        '#BF845B'
    ]
}

theme_blue_light = {
    'name' : 'blue_light',
    'textColor' : '#3D4855',
    'mainBg' : '#FFFFFF',
    'buttonColors' : [
        '#E79F6D',
        '#EFAA7F',
        '#BF845B'
    ]
}

theme_see_Thru = {
    'name' : 'see_Thru',
    'textColor' : '#EEEEEE',
    'mainBg' : '#222222',
    'buttonColors' : [
        '#555555', 
        '#666666', 
        '#444444'
    ]
}

themes = [
    theme_light,
    theme_dark,
    theme_blue_dark,
    theme_blue_light,
    theme_see_Thru
]

theme = theme_dark

# FONTS

print('Initializing font: Montserrat-Medium')
try :
    fontURL_MontserratMedium = 'https://samoe.me/font/montserrat/Montserrat-Medium.ttf'
    montserratMediumRaw = urllib.request.urlopen(fontURL_MontserratMedium).read() # OPEN THE URL AND READ ITS CONTENTS
    montserratMediumFile = io.BytesIO(montserratMediumRaw) # TURN THE DATA INTO A USABLE FILE REFERENCE
    pyglet.font.add_file(montserratMediumFile) # ADD A NON-SYSTEM-INSTALLED FONT TO TKINTER
    print('Success.')
except :
    print('Failure. Using default font instead.')

print('Initializing font: Montserrat-Light')
try :
    fontURL_MontserratLight = 'https://samoe.me/font/montserrat/Montserrat-Light.ttf'
    montserratLightRaw = urllib.request.urlopen(fontURL_MontserratLight).read()
    montserratLightFile = io.BytesIO(montserratLightRaw)
    pyglet.font.add_file(montserratLightFile)
    print('Success.')
except :
    print('Failure. Using default font instead.')

##################

def getTime() :

    timeRef = datetime.now()
    currentTime = timeRef.strftime("%I : %M %p")
    return currentTime

def updateTimeVar() :

    currentTime = getTime()
    timeVar.set(currentTime)
    root.after(5000, updateTimeVar)

def center(window, size, yoffset = 0) :

    x = (screen_width / 2) - size[0] / 2
    y = (screen_height / 2) - size[1] / 2 - yoffset
    window.geometry('+' + str(int(x)) + '+' + str(int(y)))

def resize(event) :
    windowWidth = root.winfo_width()
    newFontSize = int(windowWidth / 10)

    timerClock.config(font = ('Montserrat-Light', newFontSize))
    timerClockDecimal.config(font = ('Montserrat-Light', newFontSize))

    timerFrame.grid_columnconfigure(0, weight = 1, minsize = windowWidth / 4)
    timerFrame.grid_columnconfigure(1, weight = 1, minsize = windowWidth / 4.75)

def flashWindow() :
    previousTheme = theme
    if theme != theme_light :
        themeFlash = theme_light
    else :
        themeFlash = theme_dark

    switchTheme(themeToSwitchTo = themeFlash)
    root.after(100, switchTheme(themeToSwitchTo = previousTheme))
    root.after(100, switchTheme(themeToSwitchTo = themeFlash))
    root.after(100, switchTheme(themeToSwitchTo = previousTheme))
    root.after(100, switchTheme(themeToSwitchTo = themeFlash))
    root.after(100, switchTheme(themeToSwitchTo = previousTheme))

def switchTheme(themeToSwitchTo = None) :

    global theme
    previousTheme = theme

    if themeToSwitchTo != None :
        theme = themeToSwitchTo
    else :
        themeIndex = themes.index(theme)
        try : 
            theme = themes[themeIndex + 1]
        except :
            theme = themes[0]

    if theme is theme_see_Thru :
        root.wm_attributes("-transparentcolor", "#222222")
    else :
        root.wm_attributes("-transparentcolor", "#00FF00")

    for i in updatableGuiElements :
        i.config(bg = theme['mainBg'])

        try : # USE A TRY/EXCEPT BECAUSE NOT ALL WIDGETS HAVE FG OPTION
            i.config(fg = theme['textColor'])
        except :
            pass

        try :
            if i.colors : # IF I HAS 'COLORS', IT'S PROB A HOVERBUTTON
                if i.colors == previousTheme['buttonColors'] :
                    i.colors = theme['buttonColors']
                    i.config(bg = theme['buttonColors'][0])
                    i.config(fg = theme['textColor'])
                else :
                    i.config(bg = i.colors[0])
                    i.config(fg = 'white')
        except :
            pass

    root.update()

def playPause() :

    def pause() :

        global pauseTime
        global paused
        global playing

        currentTime = datetime.now()

        currentValue = timerTarget - currentTime
        pauseTime = str(currentValue)

        paused = True
        playing = False
        playPauseButton.config(text = 'RESUME')

    def play() :

        global paused
        if paused == True :
            paused = False
            startTimer(pauseTime)
        else :
            startTimer()

        playPauseButton.config(text = 'PAUSE')
        global playing
        playing = True

    if playing == True :

        pause()

    else :

        play()

def startTimer(customTime = None) :

    currentTime = datetime.now()

    if customTime == None :
        timerValue = timerEntry.get()
    else :
        timerValue = customTime.split('.')[0]

    timerValue = timerValue.split(':')

    global timerTarget

    if len(timerValue) > 3 :
        pass

    if len(timerValue) == 1 :
        timerTarget = currentTime + timedelta(seconds = int(timerValue[0]))
    if len(timerValue) == 2 :
        timerTarget = currentTime + timedelta(minutes = int(timerValue[0]), seconds = int(timerValue[1]))
    if len(timerValue) == 3 :
        timerTarget = currentTime + timedelta(hours = int(timerValue[0]), minutes = int(timerValue[1]), seconds = int(timerValue[2]))

    updateTimer()

def updateTimer() :

    if paused == False : # IF PAUSED IS SET TO TRUE, BREAK THE LOOP

        currentTime = datetime.now()
        currentValue = timerTarget - currentTime
        currentValue = str(currentValue)

        if not currentValue.__contains__('-1') :

            # THIS IS ALL JUST TEXT FORMATTING STUFF
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

            # NOW ADD THE STRING BACK TOGETHER

            currentValue = ''
            index = 1
            for i in doubleDigHourCheck :
                # PUT A COLON AFTER EACH PLACE OF THE TIME STRING, EXCEPT THE LAST
                if index == len(doubleDigHourCheck) :
                    currentValue = currentValue + i
                else :
                    index += 1
                    currentValue = currentValue + i + ':'

            timerClockVar.set(currentValue)
            timerClockDecimalVar.set(currentDecValue)

            root.after(10, updateTimer) # LOOP BACK TO THE TOP

        else :
            flashWindow()
            resetTimer() # RESET WHEN FINISHED

def resetTimer() :

    def setPausedFalse() :
        global paused
        paused = False

    global paused
    global playing
    paused = True
    playing = False
    timerClockVar.set('00:00:00')
    timerClockDecimalVar.set('.00')

    playPauseButton.config(text = 'START')

    root.after(20, setPausedFalse)

def clearTimer() :
    resetTimer()
    timerEntry.delete(0, 'end')

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

root.bind('<Configure>', resize)

root.grid_rowconfigure(0, weight = 1)
root.grid_columnconfigure(0, weight = 1)

updatableGuiElements.append(root)

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
rootFrame.grid_rowconfigure(2, weight = 1, minsize = 24)
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
timerFrame.grid(column = 0, row = 1, sticky = 'NEWS', pady = 32)

timerFrame.grid_columnconfigure(0, weight = 1, minsize = 300)
timerFrame.grid_columnconfigure(1, weight = 1, minsize = 200)
timerFrame.grid_rowconfigure(0, weight = 1)

timerClockVar = StringVar()
timerClockVar.set('00:00:00')

timerClockDecimalVar = StringVar()
timerClockDecimalVar.set('.00')

timerClock = Label(timerFrame, fg = theme['textColor'], bg = theme['mainBg'], font = ('Montserrat-Light', 96), textvariable = timerClockVar)
timerClock.grid(column = 0, row = 0, sticky = 'NES')

timerClockDecimal = Label(timerFrame, fg = theme['textColor'], bg = theme['mainBg'], font = ('Montserrat-Light', 96), textvariable = timerClockDecimalVar)
timerClockDecimal.grid(column = 1, row = 0, sticky = 'NWS')

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

resetButton = HoverButton(controlsFrame, text = 'RESET', colors = theme['buttonColors'], command = resetTimer)
resetButton.config(width = 8, height = 2, fg = theme['textColor'], font = ('Montserrat-Medium', 16))
resetButton.grid(column = 0, row = 0, padx = 24, ipady = 16, pady = 16, sticky = 'NES')

playPauseButton = HoverButton(controlsFrame, text = 'START', colors = theme['buttonColors'], command = playPause)
playPauseButton.config(width = 12, height = 2, fg = theme['textColor'], font = ('Montserrat-Medium', 16))
playPauseButton.grid(column = 1, row = 0, padx = 24, ipady = 16, pady = 16, sticky = 'NEWS')

clearButton = HoverButton(controlsFrame, text = 'CLEAR', colors = ['#cc0000', '#ee0000', '#aa0000'], command = clearTimer)
clearButton.config(width = 8, height = 2, fg = 'white', font = ('Montserrat-Medium', 16))
clearButton.grid(column = 2, row = 0, padx = 24, ipady = 16, pady = 16, sticky = 'NWS')

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