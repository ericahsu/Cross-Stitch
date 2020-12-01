# Erica Hsu, 11/30/2020

# cmu_112_graphics downloaded from 15-112 course website: https://www.cs.cmu.edu/~112/schedule.html
from cmu_112_graphics import *
import pandas as pd

class TitleScreenMode(Mode):
    def redrawAll(mode, canvas):
        # Background and title
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "powder blue")
        canvas.create_text(mode.width/2, mode.height/4, text = "Cross Stitch", font = 'Verdana 100 bold')
        # Get Started button
        canvas.create_rectangle(250, 200, 550, 300, fill = "DarkSeaGreen1")
        canvas.create_text(400, 250, text = "Get Started", font = 'Verdana 36 bold')
        # History button
        canvas.create_rectangle(300, 350, 500, 400, fill = "light cyan")
        canvas.create_text(400, 375, text = "History", font = "Verdana 24")

    def mousePressed(mode, event):
        # Enter Style mode if the get started is clicked
        if event.x >= 250 and event.x <= 550 \
            and event.y >= 200 and event.y <= 300:
            mode.app.setActiveMode(mode.app.styleMode)

class StyleMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "powder blue")
        canvas.create_text(mode.width/2, mode.height/4, text = "Step 1: Choose your style", font = "Verdana 36")
        # Full photo
        canvas.create_rectangle(100, 200, 300, 250, fill = "lightpink")
        canvas.create_text(200, 225, text = "Full Photo", font = "Verdana 24")
        # Center
        canvas.create_rectangle(500, 200, 700, 250, fill = "lightpink")
        canvas.create_text(600, 225, text = "Center", font = "Verdana 24")

    def mousePressed(mode, event):
        if event.x >= 100 and event.x <= 300 \
            and event.y >= 200 and event.y <= 250:
            mode.app.setActiveMode(mode.app.urlAndPathMode)
        if event.x >= 500 and event.x <= 700 \
            and event.y >= 200 and event.y <= 250:
            mode.app.setActiveMode(mode.app.urlAndPathMode)

class UrlAndPathMode(Mode):
    def appStarted(mode):
        # Url or Path
        mode.urlOrPath = None

    def userInput(mode):
        mode.urlOrPath = simpledialog.askstring('getUserInput', "url or path")

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "powder blue")
        canvas.create_text(mode.width/2, mode.height/4, text = "Step 2: Type in the url or path to your image", font = "Verdana 30")
        canvas.create_rectangle(100, 200, 700, 250, fill = "white")
        canvas.create_text(400, 225, text = "Click here to type in your url or path", font = "Verdana 24")

    def mousePressed(mode, event):
        if event.x >= 100 and event.x <= 700 \
            and event.y >= 200 and event.y <= 250:
            mode.userInput()

    def timerFired(mode):
        if mode.urlOrPath != None:
            PatternMode(mode.urlOrPath)
            mode.app.setActiveMode(PatternMode(mode.urlOrPath))

class PatternMode(Mode):
    def __init__(mode, urlOrPath, **kwargs):
        mode.urlOrPath = urlOrPath
        mode.app = None
        mode._appStartedCalled = False
        super().__init__(**kwargs)
        def modeActivated(mode): pass
        def modeDeactivated(mode): pass
        def loadImage(mode, path=None): return mode.app.loadImage(path)


    def appStarted(mode):

        # DMC Table
        mode.dmcTable = pd.read_csv('dmctable.csv')
        mode.rgb = mode.dmcTable['RGB']
        mode.dmc = mode.dmcTable['DMC']
        mode.colorName = mode.dmcTable['Color']
        print(mode.urlOrPath)
        # Image
        mode.image1 = mode.loadImage(mode.urlOrPath)
        mode.image2 = mode.scaleImage(mode.image1, 2/3)
        mode.imageResult = None
        mode.countOfRgb = {}
        mode.dmcOfImage = {}
        mode.threads = []
        mode.mapOfRgbValues(mode.image1)

     # Creates a 2D list of the rgb values in a given image, pixelates the image,
    # and returns the threads needed
    def mapOfRgbValues(mode, image):
        mode.image1 = mode.image1.convert('RGB')
        mode.image2 = Image.new(mode='RGB', size=mode.image1.size)

        # Pixelate adapted from https://stackoverflow.com/questions/47143332/how-to-pixelate-a-square-image-to-256-big-pixels-with-python
        imgSmall = mode.image1.resize((100, 100),resample=Image.BILINEAR)
        result = imgSmall.resize(mode.image1.size,Image.NEAREST)
        result.save('result.png')
        mode.imageResult = mode.loadImage('result.png')
        mapOfRgb = []

        # 2D list of rgb values in rows and columns
        for x in range(100):
            row = []
            for y in range(100):
                r,g,b = imgSmall.getpixel((x,y))
                row.append((r, g, b))
            mapOfRgb.append(row)

        # # Dictionary that counts the number of pixels for each rgb value
        for x in mapOfRgb:
            for y in x:
                if y in mode.countOfRgb:
                    mode.countOfRgb[y] += 1
                else:
                    mode.countOfRgb[y] = 1

        # Finds all the necessary threads
        for x in mode.countOfRgb:
            index, rgb = mode.findMinDiff(x, mode.rgb)
            numberAndName = mode.dmc[index] + ' ' + mode.colorName[index]
            if numberAndName not in mode.threads:
                mode.threads.append(numberAndName)
            # Shorten run time for now
            elif len(mode.threads) > 30:
                break

    # Given two sets of rgb values return the difference
    def findDiff(mode, r1, g1, b1, r2, g2, b2):
        diffr = abs(r2 - r1)
        diffg = abs(g2 - g1)
        diffb = abs(b2 - b1)
        totalDiff = diffr + diffg + diffb
        return totalDiff

    # Given a rgb value, compare it to the list of rgb values in the rgbTable 
    # and return the closest match
    def findMinDiff(mode, rgb1, rgbTable):
        minimum = None
        closest = None
        minIndex = None
        r1, g1, b1 = rgb1
        for index in range(len(rgbTable)):
            r2, g2, b2 = eval(rgbTable[index])
            diff = mode.findDiff(r1, g1, b1, r2, g2, b2)
            if minimum == None or diff < minimum:
                minimum = diff
                closest = rgbTable[index]
                minIndex = index
        return minIndex, closest

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "powder blue")
        canvas.create_image(200, 200, image=ImageTk.PhotoImage(mode.imageResult))

        # Text box of list of threads 
        # Adapted from Hack112 code 
        frame = Frame(canvas, height = 300, width = 300)
        frame.pack(expand = False)
        frame.place(x=400, y=100)
        frame.pack_propagate(0)
        # text window
        text=Text(frame, width=100, height=150, font='Arial 18',\
                    spacing1=5, spacing2=5, wrap=WORD)
        text.pack(side=RIGHT)
        text.insert(END, f"{mode.threads}")

class MyModalApp(ModalApp):
    def appStarted(app):
        app.titleScreenMode = TitleScreenMode()
        app.styleMode = StyleMode()
        app.urlAndPathMode = UrlAndPathMode()
        app.setActiveMode(app.titleScreenMode)

app = MyModalApp(width=800, height=500)

