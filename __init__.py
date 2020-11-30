# cmu_112_graphics downloaded from 15-112 course website
from cmu_112_graphics import *
import pandas as pd
import random

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
        # DMC Table
        mode.dmcTable = pd.read_csv('dmctable.csv')
        mode.rgb = mode.dmcTable['RGB']
        mode.dmc = mode.dmcTable['DMC']
        mode.colorName = mode.dmcTable['Color']

        # Image
        mode.image1 = mode.loadImage('testImage2.gif')
        mode.image2 = mode.scaleImage(mode.image1, 2/3)
        mode.countOfRgb = {}
        mode.dmcOfImage = {}
        #mode.mapOfRgbValues()
        mode.threads = None

    def mapOfRgbValues(mode):
        mode.image1 = mode.image1.convert('RGB')
        mode.image2 = Image.new(mode='RGB', size=mode.image1.size)

        # Pixelate adapted from https://stackoverflow.com/questions/47143332/how-to-pixelate-a-square-image-to-256-big-pixels-with-python
        imgSmall = mode.image1.resize((100, 100),resample=Image.BILINEAR)
        result = imgSmall.resize(mode.image1.size,Image.NEAREST)
        result.save('result.png')
        mapOfRgb = []

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
        mode.threads = []
        for x in mode.countOfRgb:
            index, rgb = mode.findMinDiff(x, mode.rgb)
            numberAndName = mode.dmc[index] + ' ' + mode.colorName[index]
            if numberAndName not in mode.threads:
                mode.threads.append(numberAndName)

    # Given two sets of rgb values return the difference
    def findDiff(mode, r1, g1, b1, r2, g2, b2):
        diffr = abs(r2 - r1)
        diffg = abs(g2 - g1)
        diffb = abs(b2 - b1)
        totalDiff = diffr + diffg + diffb
        return totalDiff

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
        canvas.create_text(mode.width/2, mode.height/4, text = "Step 2: Type in the url or path to your image", font = "Verdana 30")
       
        
        

class GameMode(Mode):
    def appStarted(mode):
        mode.score = 0
        mode.randomizeDot()

    def randomizeDot(mode):
        mode.x = random.randint(20, mode.width-20)
        mode.y = random.randint(20, mode.height-20)
        mode.r = random.randint(10, 20)
        mode.color = random.choice(['red', 'orange', 'yellow', 'green', 'blue'])
        mode.dx = random.choice([+1,-1])*random.randint(3,6)
        mode.dy = random.choice([+1,-1])*random.randint(3,6)

    def moveDot(mode):
        mode.x += mode.dx
        if (mode.x < 0) or (mode.x > mode.width): mode.dx = -mode.dx
        mode.y += mode.dy
        if (mode.y < 0) or (mode.y > mode.height): mode.dy = -mode.dy

    def timerFired(mode):
        mode.moveDot()

    def mousePressed(mode, event):
        d = ((mode.x - event.x)**2 + (mode.y - event.y)**2)**0.5
        if (d <= mode.r):
            mode.score += 1
            mode.randomizeDot()
        elif (mode.score > 0):
            mode.score -= 1

    def keyPressed(mode, event):
        if (event.key == 'h'):
            mode.app.setActiveMode(mode.app.helpMode)

    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 20, text=f'Score: {mode.score}', font=font)
        canvas.create_text(mode.width/2, 50, text='Click on the dot!', font=font)
        canvas.create_text(mode.width/2, 80, text='Press h for help screen!', font=font)
        canvas.create_oval(mode.x-mode.r, mode.y-mode.r, mode.x+mode.r, mode.y+mode.r,
                           fill=mode.color)

class HelpMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text='This is the help screen!', font=font)
        canvas.create_text(mode.width/2, 250, text='(Insert helpful message here)', font=font)
        canvas.create_text(mode.width/2, 350, text='Press any key to return to the game!', font=font)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.titleScreenMode = TitleScreenMode()
        app.styleMode = StyleMode()
        app.urlAndPathMode = UrlAndPathMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.titleScreenMode)
        app.timerDelay = 50

app = MyModalApp(width=800, height=500)