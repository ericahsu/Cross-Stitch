# Erica Hsu, 11/30/2020

# Used this image for testing: https://cdn.pixabay.com/photo/2015/04/19/08/33/flower-729512__340.jpg
# Run history.py and webscrape.py first

# cmu_112_graphics downloaded from 15-112 course website: https://www.cs.cmu.edu/~112/schedule.html
from cmu_112_graphics import *
import pandas as pd
import time
import math
# Read in the csv file that has the record of patterns created
history = pd.read_csv('history.csv')

class TitleScreenMode(Mode):
    def appStarted(mode):
        mode.image = mode.loadImage('TitleScreen.png')

    def redrawAll(mode, canvas):
        # Background and title
        maxwidth = 800
        maxheight = 500
        ratio = min(maxwidth/mode.image.width, maxheight/mode.image.height)
        mode.image = mode.scaleImage(mode.image, ratio)

        canvas.create_image(400, 250, image=ImageTk.PhotoImage(mode.image))

        # Get Started button
        canvas.create_rectangle(250, 200, 550, 300, fill = "#ffdbe7")
        canvas.create_text(400, 250, text = "Get Started", font = 'Verdana 36')

        # History button
        canvas.create_rectangle(300, 350, 500, 400, fill = "#ffa6d2")
        canvas.create_text(400, 375, text = "History", font = "Verdana 24")


    def mousePressed(mode, event):
        # Enter Style mode
        if event.x >= 250 and event.x <= 550 \
            and event.y >= 200 and event.y <= 300:
            mode.app.setActiveMode(mode.app.styleMode)

        # Enter History
        elif event.x >= 300 and event.x <= 500\
             and event.y >= 350 and event.y <= 400:
             mode.app.setActiveMode(mode.app.historyMode)

class StyleMode(Mode):
    Mode.history = history
    Mode.index = len(Mode.history)
    Mode.originalImage = Mode.history['Original Image'].tolist()
    Mode.pixelated = Mode.history['Pixelated Image'].tolist()
    Mode.threads = Mode.history['Threads'].tolist()
    Mode.full = Mode.history['Full Photo'].tolist()
    Mode.centered = Mode.history['Centered'].tolist()
    Mode.fav = Mode.history['Favorites'].tolist()
    Mode.styleFull = None
    Mode.styleCenter = None

    def appStarted(mode):
        # Example images
        mode.fullPhotoEx = mode.loadImage('fullphotoex.png')
        mode.centerEx = mode.loadImage('centerex.png')

    def mousePressed(mode, event):
        # Full Photo
        if event.x >= 100 and event.x <= 300 \
            and event.y >= 175 and event.y <= 225:
            StyleMode.full.append('True')
            StyleMode.centered.append('False')
            StyleMode.fav.append('False')
            StyleMode.styleFull = True
            mode.app.setActiveMode(mode.app.urlAndPathMode)

        # Center 
        if event.x >= 500 and event.x <= 700 \
            and event.y >= 175 and event.y <= 225:
            StyleMode.full.append('False')
            StyleMode.centered.append('True')
            StyleMode.fav.append('False')
            StyleMode.styleCenter = True
            mode.app.setActiveMode(mode.app.urlAndPathMode)

        # Back Button
        elif event.x >= 25 and event.x <= 120\
            and event.y >= 25 and event.y <= 60:
            mode.app.setActiveMode(mode.app.titleScreenMode)

    def redrawAll(mode, canvas):
        # Background and instructions
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "#fac7b9")
        canvas.create_text(mode.width/2, mode.height/5, text = "Step 1: Choose your style", font = "Verdana 36")
        
        # Resize image
        maxwidth = 200
        maxheight = 200
        
        # Full photo
        canvas.create_rectangle(100, 175, 300, 225, fill = "lightpink")
        canvas.create_text(200, 200, text = "Full Photo", font = "Verdana 24")
        
        # Full photo example 
        ratio = min(maxwidth/mode.fullPhotoEx.width, maxheight/mode.fullPhotoEx.height)
        mode.fullPhotoEx = mode.scaleImage(mode.fullPhotoEx, ratio)
        canvas.create_image(200, 325, image=ImageTk.PhotoImage(mode.fullPhotoEx))
        
        # Center
        canvas.create_rectangle(500, 175, 700, 225, fill = "lightpink")
        canvas.create_text(600, 200, text = "Center", font = "Verdana 24")
        
        # Center photo example
        ratio = min(maxwidth/mode.centerEx.width, maxheight/mode.centerEx.height)
        mode.centerEx = mode.scaleImage(mode.centerEx, ratio)
        canvas.create_image(600, 325, image=ImageTk.PhotoImage(mode.centerEx))
        
        # Back Button
        canvas.create_rectangle(25, 25, 120, 60, fill = '#f7d4a8')
        canvas.create_text(72, 42, text = "Back")

class UrlAndPathMode(Mode):
    Mode.urlOrPath = None

    def appStarted(mode):
        mode.urlOrPath = None 
        mode.error = False
        mode.info = False

    def userInput(mode):
        mode.urlOrPath = simpledialog.askstring('getUserInput', "url or path")
        UrlAndPathMode.urlOrPath = mode.urlOrPath

    def information(mode, canvas):
        canvas.create_rectangle(200, 100, 600, 400, fill = 'white')
        urlText = 'How to find the url of an image \n 1. Search for the image \n 2. Right-click image \n 3. Click "Open image in new tab" \n 4. Copy the url'
        canvas.create_text(350, 150, text = urlText)
        macPathText = 'How to find the path of an image for Mac \n 1. Locate desired image in finder \n 2. Right-click the image file \n 3. Hold down the Option key \n 4. Click "Copy image as Pathname"'
        canvas.create_text(370, 250, text = macPathText)
        windowsPathText = 'How to find the path of an image for Windows \n 1. Locate desired image \n 2. Hold down the Shift key and right-click the image \n 4. Click "Copy as Path"'
        canvas.create_text(400, 350, text = windowsPathText)
    
    def redrawAll(mode, canvas):
        # Background and instructions
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "#fac7b9")
        canvas.create_text(mode.width/2, mode.height/4, text = "Step 2: Type in the url or path to your image", font = "Verdana 30")
        
        # Box for typing in url or path
        canvas.create_rectangle(100, 200, 700, 250, fill = "white")
        canvas.create_text(400, 225, text = "Click here to type in your url or path", font = "Courier 24")
        
        # Back Button
        canvas.create_rectangle(25, 25, 120, 60, fill = '#f7d4a8')
        canvas.create_text(72, 42, text = "Back")
        
        # More information icon
        canvas.create_oval(715, 200, 765, 250, fill = 'white')
        canvas.create_text(740, 225, text = 'i', font = 'Courier 24')

        # Error Message
        if mode.error:
            canvas.create_text(400, 275, text = "Error: That url or path does not exist. Please try again.", font = "Verdana 18", fill = "Red")
        
        # Information window
        if mode.info:
            mode.information(canvas)

    def mousePressed(mode, event):
        # Gets input
        if event.x >= 100 and event.x <= 700 \
            and event.y >= 200 and event.y <= 250 and mode.info == False:
            mode.userInput()

        # Back Button, reset StyleMode attributes
        elif event.x >= 25 and event.x <= 120\
            and event.y >= 25 and event.y <= 60 and mode.info == False:
            StyleMode.originalImage = StyleMode.history['Original Image'].tolist()
            StyleMode.pixelated = StyleMode.history['Pixelated Image'].tolist()
            StyleMode.threads = StyleMode.history['Threads'].tolist()
            StyleMode.full = StyleMode.history['Full Photo'].tolist()
            StyleMode.centered = StyleMode.history['Centered'].tolist()
            StyleMode.fav = StyleMode.history['Favorites'].tolist()
            StyleMode.styleFull = None
            StyleMode.styleCenter = None
            mode.app.setActiveMode(mode.app.styleMode)

        # Information
        elif event.x >= 715 and event.x <= 765\
            and event.y >= 200 and event.y <= 250: 
            mode.info = True

        elif mode.info:
            mode.info = False

    def timerFired(mode):
        if mode.urlOrPath != None:
            try:
                mode.loadImage(mode.urlOrPath)
                mode.app.setActiveMode(mode.app.loadMode)
            except:
                mode.error = True

class LoadMode(Mode):
    def appStarted(mode):
        mode.time = time.time()

    def patternMode(mode):
        PatternMode(UrlAndPathMode.urlOrPath)
        mode.app.setActiveMode(PatternMode(UrlAndPathMode.urlOrPath))

    def timerFired(mode):
        if time.time() - mode.time > 1:
            mode.patternMode()

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "#fac7b9")
        canvas.create_text(400, 250, text = "Loading...", font = "Courier 36")

class PatternMode(Mode):

    def __init__(mode, urlOrPath, **kwargs):
        mode.urlOrPath = urlOrPath
        StyleMode.originalImage.append(f'{mode.urlOrPath}')
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

        # Initialize variables
        mode.imageResult = None
        mode.threads = []
        mode.pages = None
        mode.page = 1
        mode.mapOfGray = []
        mode.mapOfRgb = []
        mode.maxPixels = 50

        # Filters for edge detection
        mode.horizontalFilter = [[-1,0,1], [-2,0,2], [-1,0,1]]
        mode.verticalFilter = [[-1,-2,-1], [0,0,0], [1,2,1]]

        # Images
        mode.image1 = mode.loadImage(mode.urlOrPath)
        mode.image1 = mode.image1.convert('RGB')
        mode.image2 = Image.new(mode='RGB', size=mode.image1.size)
        mode.image3 = Image.new("L", size=mode.image1.size)
        mode.image4 = Image.new("L", size=mode.image1.size)
        
        # Depending on the style, call fullPhoto or centerImage
        if StyleMode.styleFull:
            mode.result = mode.fullPhoto()
        elif StyleMode.styleCenter:
            mode.result = mode.centerImage()

    # Multiplies the two matrices given
    def multiplyMatrices(mode, m1, m2):
        final = []
        for x in range(len(m1)):
            row = []
            for y in range(len(m1[0])):
                element = m1[x][y] * m2[x][y]
                row.append(element)
            final.append(row)
        return final

    # Sums up all the values in a matrix
    def sumValues(mode, m):
        total = 0
        for x in range(len(m)):
            for y in range(len(m[0])):
                if isinstance(m[x][y], int):
                    total += m[x][y]
                else:
                    total = total
        return total

    def centerImage(mode):
        # Greyscales the image
        for x in range(mode.image2.width):
            row = []
            for y in range(mode.image2.height):
                r,g,b = mode.image1.getpixel((x,y))
                grayscale = ((0.3 * r) + (0.59 * g) + (0.11 * b))
                grayscale = int(grayscale)
                row.append(grayscale)
                mode.image3.putpixel((x, y), grayscale)
            mode.mapOfGray.append(row)

        # Learned algorithm for edge detection from: https://towardsdatascience.com/edge-detection-in-python-a3c263a13e03
        for x in range(0, mode.image3.width - 2, 3):
            for y in range(0, mode.image3.height - 2, 3):
                # Creates 3x3 matrix
                new = []
                new.append(mode.mapOfGray[x][y:y+3])
                new.append(mode.mapOfGray[x + 1][y:y+3])
                new.append(mode.mapOfGray[x + 2][y:y + 3])

                # Multiply matrix by vertical and horizontal filter
                verticalPixels = mode.multiplyMatrices([[-1,-2,-1], [0,0,0], [1,2,1]], new)
                verticalScore = mode.sumValues(verticalPixels)/4
                horizontalPixels = mode.multiplyMatrices([[-1,0,1], [-2,0,2], [-1,0,1]], new)
                horizontalScore = mode.sumValues(horizontalPixels)/4

                # Find edge score
                edgeScore = (verticalScore**2 + horizontalScore**2)**.5
                edgeScore = int(edgeScore)

                # Depending on the edge score, place a black or white pixel down
                for a in range(x, x + 3):
                    for b in range(y, y + 3):
                        if edgeScore >= 30:
                            mode.image4.putpixel((a, b), 255)
                        elif edgeScore < 30:
                            mode.image4.putpixel((a, b), 0)     

        # Places down white pixels until it reaches a white pixel, which is the edge 
        # From left to right 
        for y in range(mode.image4.height):
            for x in range(mode.image4.width):
                if mode.image4.getpixel((x, y)) == 0:
                    mode.image1.putpixel((x, y), (255, 255, 255))
                if mode.image4.getpixel((x, y)) != 0:
                    break
        
        # From right to left
        for y in range(mode.image4.height-1, -1, -1):
            for x in range(mode.image4.width-1, -1, -1):
                if mode.image4.getpixel((x, y)) == 0:
                    mode.image1.putpixel((x, y), (255, 255, 255))
                if mode.image4.getpixel((x, y)) != 0:
                    break
        
        # From top to bottom
        for x in range(mode.image4.width - 1, -1, -1):
            for y in range(mode.image4.height - 1, -1, -1):
                if mode.image4.getpixel((x, y)) == 0:
                    mode.image1.putpixel((x, y), (255, 255, 255))
                if mode.image4.getpixel((x, y)) != 0:
                    break
        
        # From bottom to top
        for x in range(mode.image4.width):
            for y in range(mode.image4.height):
                if mode.image4.getpixel((x, y)) == 0:
                    mode.image1.putpixel((x, y), (255, 255, 255))
                if mode.image4.getpixel((x, y)) != 0:
                    break
        mode.fullPhoto()

    # Creates a 2D list of the rgb values in a given image, pixelates the image,
    # and returns the threads needed
    def fullPhoto(mode):
        # 2D list of rgb values in rows and columns
        for x in range(mode.image1.width):
            row = []
            for y in range(mode.image1.height):
                r,g,b = mode.image1.getpixel((x,y))
                row.append((r, g, b))
            mode.mapOfRgb.append(row)

        # Pixelate and get list of threads
        size = max(mode.image2.width/mode.maxPixels, mode.image2.height/mode.maxPixels)
        size = int(size)
        for x in range(0, mode.image2.width - size, size):
            for y in range(0, mode.image2.height - size, size):
                new = []
                sumr = 0
                sumg = 0
                sumb = 0
                for z in range(size):
                    for w in range(size):
                        r, g, b = mode.mapOfRgb[x + z][y + w]
                        sumr += r
                        sumg += g
                        sumb += b
                sumr = int(sumr/(size ** 2))
                sumg = int(sumg/(size ** 2))
                sumb = int(sumb/(size ** 2))
                index, rgb = mode.findMinDiff((sumr, sumg, sumb), mode.rgb)
                numberAndName = mode.dmc[index] + ' ' + mode.colorName[index]
                if numberAndName not in mode.threads:
                    mode.threads.append(numberAndName)
                for a in range(x, x + size):
                    for b in range(y, y + size):
                        mode.image2.putpixel((a, b), rgb)
        mode.pages = math.ceil(len(mode.threads)/20)
        StyleMode.threads.append(mode.threads)

        result = mode.image2
        result.save(f'result{StyleMode.index}.png')
        mode.imageResult = mode.loadImage(f'result{StyleMode.index}.png')
        # Add pixelated image to the history.csv
        StyleMode.pixelated.append(f'result{StyleMode.index}.png')

        # df = pd.DataFrame(list(zip(StyleMode.originalImage, StyleMode.pixelated, StyleMode.threads, StyleMode.full, StyleMode.centered, StyleMode.fav)),\
        # columns = ['Original Image', 'Pixelated Image', 'Threads','Full Photo', 'Centered', 'Favorites'])
        # df.to_csv('history.csv')

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
                closest = (r2, g2, b2)
                minIndex = index
        return minIndex, closest

    def drawThreads(mode, canvas, page):
        y1 = 100
        for x in mode.threads[20 * (page - 1):20 * page]:
            canvas.create_text(600, y1, text = x)
            y1 += 15

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "#fac7b9")
        
        # Image
        maxwidth = 300
        maxheight = 300
        ratio = min(maxwidth/mode.imageResult.width, maxheight/mode.imageResult.height)
        mode.imageResult = mode.scaleImage(mode.imageResult, ratio)
        canvas.create_image(200, 250, image=ImageTk.PhotoImage(mode.imageResult))
        canvas.create_text(200, 50, text = "Pattern", font = "Courier 18")
        canvas.create_text(200, 65, text = "Click on the pattern for a more detailed view", font = "Courier 12")

        # Draws the threads
        canvas.create_text(600, 50, text = "List of threads", font = "Courier 18")
        canvas.create_text(600, 65, text = "Use the left and right arrow keys to see all the threads", font = "Courier 12")
        mode.drawThreads(canvas, mode.page)

        # Arrows
        canvas.create_rectangle(450, 237, 475, 262, fill = 'white')
        canvas.create_polygon(452, 250, 472, 260, 472, 239, fill = 'black')
        canvas.create_rectangle(725, 237, 750, 262, fill = 'white')
        canvas.create_polygon(747, 250, 727, 260, 727, 239, fill = 'black')

    def mousePressed(mode, event):
        if event.x >= 50 and event.x <= 350\
            and event.y >= 100 and event.y <= 400:
            mode.app.setActiveMode(mode.app.patternOnlyMode)

        # Left Arrow
        elif event.x >= 450 and event.x <= 475\
            and event.y >= 237 and event.y <= 262:
            mode.page -= 1
            if mode.page < 1:
                mode.page += 1
        
        # Right Arrow
        elif event.x >= 725 and event.x <= 750\
            and event.y >= 237 and event.y <= 262:
            mode.page += 1
            if mode.page > mode.pages:
                mode.page -= 1

    def keyPressed(mode, event):
        if event.key == 'Right':
            mode.page += 1
            if mode.page > mode.pages:
                mode.page -= 1
        if event.key == 'Left':
            mode.page -= 1
            if mode.page < 1:
                mode.page += 1

class LoadPatternMode(Mode):

    def __init__(mode, image, threads, **kwargs):
        mode.image = image
        mode.threads = threads
        mode.app = None
        mode._appStartedCalled = False
        super().__init__(**kwargs)
        def modeActivated(mode): pass
        def modeDeactivated(mode): pass
        def loadImage(mode, path=None): return mode.app.loadImage(path)

    def appStarted(mode):
        mode.imageResult = mode.loadImage(mode.image)
        mode.pages = math.ceil(len(mode.threads)/20)
        mode.page = 1

    def drawThreads(mode, canvas, page):
        y1 = 100
        for x in mode.threads[20 * (page - 1):20 * page]:
            canvas.create_text(600, y1, text = x)
            y1 += 15

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "#fac7b9")
        
        # Image
        maxwidth = 300
        maxheight = 300
        ratio = min(maxwidth/mode.imageResult.width, maxheight/mode.imageResult.height)
        mode.imageResult = mode.scaleImage(mode.imageResult, ratio)
        canvas.create_image(200, 250, image=ImageTk.PhotoImage(mode.imageResult))
        canvas.create_text(200, 50, text = "Pattern", font = "Courier 18")
        canvas.create_text(200, 65, text = "Click on the pattern for a more detailed view", font = "Courier 12")

        # Draws the threads
        canvas.create_text(600, 50, text = "List of threads", font = "Courier 18")
        canvas.create_text(600, 65, text = "Use the left and right arrow keys to see all the threads", font = "Courier 12")
        mode.drawThreads(canvas, mode.page)

        # Arrows
        canvas.create_rectangle(450, 237, 475, 262, fill = 'white')
        canvas.create_polygon(452, 250, 472, 260, 472, 239, fill = 'black')
        canvas.create_rectangle(725, 237, 750, 262, fill = 'white')
        canvas.create_polygon(747, 250, 727, 260, 727, 239, fill = 'black')

    def mousePressed(mode, event):
        if event.x >= 50 and event.x <= 350\
            and event.y >= 100 and event.y <= 400:
            mode.app.setActiveMode(mode.app.patternOnlyMode)

        # Left Arrow
        elif event.x >= 450 and event.x <= 475\
            and event.y >= 237 and event.y <= 262:
            mode.page -= 1
            if mode.page < 1:
                mode.page += 1
        
        # Right Arrow
        elif event.x >= 725 and event.x <= 750\
            and event.y >= 237 and event.y <= 262:
            mode.page += 1
            if mode.page > mode.pages:
                mode.page -= 1

    def keyPressed(mode, event):
        if event.key == 'Right':
            mode.page += 1
            if mode.page > mode.pages:
                mode.page -= 1
        if event.key == 'Left':
            mode.page -= 1
            if mode.page < 1:
                mode.page += 1

class PatternOnlyMode(Mode):
    def appStarted(mode):
        mode.maxwidth = 400
        mode.maxheight = 400
        mode.imageResult = mode.loadImage(f'result{StyleMode.index}.png')
        mode.singleImage = mode.loadImage(f'result{StyleMode.index}.png')
        mode.ratio = min(mode.maxwidth/mode.imageResult.width, mode.maxheight/mode.imageResult.height)
        mode.image = mode.scaleImage(mode.imageResult, mode.ratio)
        mode.ratio2 = min(mode.maxwidth/mode.singleImage.width, mode.maxheight/mode.singleImage.height)
        mode.singleImage = mode.scaleImage(mode.singleImage, mode.ratio2)
        mode.singleColor = False
        mode.colorCodeOrName = None
        mode.originalRgb = None
        mode.newRgb = None
        mode.error = False
        mode.threads = StyleMode.threads[-1]
        mode.pages = math.ceil(len(mode.threads)/20)
        mode.page = 1
        # DMC Table
        mode.dmcTable = pd.read_csv('dmctable.csv')
        mode.rgb = mode.dmcTable['RGB']
        mode.dmc = mode.dmcTable['DMC']
        mode.colorName = mode.dmcTable['Color']

    # Finds the color at a given x, y point after scaling the image
    def findColor(mode, x, y):
        r,g,b = mode.image.getpixel((x,y))
        return r, g, b

    def oneColorImage(mode, rgb):
        for x in range(mode.image.width):
            for y in range(mode.image.height):
                if mode.image.getpixel((x,y)) != rgb:
                    mode.singleImage.putpixel((x, y), (255, 255, 255))

    def userInput(mode):
        mode.colorCodeOrName = simpledialog.askstring('getUserInput', "Color code or name")

    def replaceColor(mode):
        for index in range(len(mode.dmc)):
            if mode.dmc[index] == mode.colorCodeOrName:
                mode.newRgb = mode.rgb[index]
                break
        if mode.newRgb == None:
            mode.error = True
        else:
            mode.error = False
        if mode.error == False:
            for x in range(mode.image.width):
                for y in range(mode.image.height):
                    if mode.image.getpixel((x, y)) == mode.originalRgb:
                        mode.image.putpixel((x, y), eval(mode.newRgb))

    def drawThreads(mode, canvas, page):
        y1 = 175
        for x in mode.threads[20 * (page - 1):20 * page]:
            canvas.create_text(675, y1, text = x, font = 'Courier 10')
            y1 += 10

    # def drawGrid(mode, canvas):
    #     for x in range(100, 501, 8):
    #         canvas.create_line(x, 50, x, 450)
    #     for y in range(50, 451, 8):
    #         canvas.create_line(100, y, 500, y)

    def keyPressed(mode, event):
        if event.key == 'Right':
            mode.page += 1
            # if mode.page > mode.pages:
            #     mode.page -= 1
        if event.key == 'Left':
            mode.page -= 1
            # if mode.page < 1:
            #     mode.page += 1

    def mousePressed(mode, event):
        width = mode.image.width
        height = mode.image.height
        borderx = (400 - width)/2
        bordery = (400 - height)/2

        # If you click on the image, show only the pixels with the same color as 
        # where you clicked
        if event.x >= 100 + borderx and event.x <= 500 - borderx\
            and event.y >= 50 + bordery and event.y <= 450 - bordery:
            if mode.singleColor == False:
                mode.singleColor = True
                mode.originalRgb = mode.findColor(event.x - (borderx + 100), event.y - (bordery + 50))
                mode.oneColorImage(mode.originalRgb)
            elif mode.singleColor == True:
                mode.singleImage = mode.image              
                mode.singleColor = False 
        # Click on search bar
        elif event.x >= 600 and event.x <= 750 \
            and event.y >= 125 and event.y <= 150:
            mode.userInput()
        # Change color
        elif event.x >= 625 and event.y <= 725\
            and event.y >= 50 and event.y <= 100\
            and mode.originalRgb != None and mode.colorCodeOrName != None:
            mode.replaceColor()
            mode.singleColor = False
        # Back Button
        elif event.x >= 15 and event.x <= 90\
            and event.y >= 15 and event.y <= 50:
            LoadPatternMode(StyleMode.pixelated[-1], StyleMode.threads[-1])
            mode.app.setActiveMode(LoadPatternMode(StyleMode.pixelated[-1], StyleMode.threads[-1]))
        # List of threads
        elif event.x >= 600 and event.x <= 750\
            and event.y >= 175 and event.y <= 375:
            if mode.singleColor:
                mode.singleImage = mode.image
                mode.singleColor = False
            else:
                mode.singleColor = True
                threads = mode.threads[20 * (mode.page - 1): 20 * mode.page]
                index = int((event.y - 175)/10)
                thread = threads[index]
                code = thread.split(' ')
                for i in range(len(mode.dmc)):
                    if code[0] == mode.dmc[i]:
                        codeIndex = i
                mode.originalRgb = eval(mode.rgb[codeIndex])
                mode.oneColorImage(mode.originalRgb)
        # Reset
        elif event.x >= 600 and event.x <= 675\
            and event.y >= 400 and event.y <= 430:
            mode.image = mode.loadImage(f'result{StyleMode.index}.png')
            mode.ratio = min(mode.maxwidth/mode.image.width, mode.maxheight/mode.image.height)
            mode.image = mode.scaleImage(mode.image, mode.ratio)
        # Save
        elif event.x >= 675 and event.x <= 750\
            and event.y >= 400 and event.y <= 430:
            mode.image.save(f'resultmod{StyleMode.index}.png')
            mode.imageResult = mode.image
            StyleMode.pixelated[-1] = f'resultmod{StyleMode.index}.png'
            df = pd.DataFrame(list(zip(StyleMode.originalImage, StyleMode.pixelated, StyleMode.threads, StyleMode.full, StyleMode.centered, StyleMode.fav)),\
            columns = ['Original Image', 'Pixelated Image', 'Threads','Full Photo', 'Centered', 'Favorites'])
            df.to_csv('history.csv')

    def redrawAll(mode, canvas):
        # Draws the background and image
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "#fac7b9")
        maxwidth = 400
        maxheight = 400
        if mode.singleColor != True:
            canvas.create_image(300, 250, image=ImageTk.PhotoImage(mode.image))
        else:
            mode.ratio = min(maxwidth/mode.singleImage.width, maxheight/mode.singleImage.height)
            mode.singleImage = mode.scaleImage(mode.singleImage, mode.ratio)
            canvas.create_image(300, 250, image=ImageTk.PhotoImage(mode.singleImage))
            for i in range(len(mode.rgb)):
                if f'{mode.originalRgb}' == mode.rgb[i]:
                    index = i
                    canvas.create_text(300, 475, text = f'{mode.dmc[index]} {mode.colorName[index]}')
                    break
        # Change color
        canvas.create_rectangle(625, 50, 725, 100, fill = "#ecccff")
        canvas.create_text(675, 75, text = "Change Color")
        # Type in color name or code
        canvas.create_rectangle(600, 125, 750, 150, fill = "white")
        canvas.create_text(675, 138, text = "Click to type")
        # Error
        if mode.error:
            canvas.create_text(675, 155, text = "Color could not be found.\n Please try again.",\
                fill = 'red')
        # Back Button
        canvas.create_rectangle(15, 15, 90, 50, fill = '#f7d4a8')
        canvas.create_text(52, 32, text = "Back")
        # Save Button
        canvas.create_rectangle(675, 400, 750, 430, fill = '#e89797')
        canvas.create_text(713, 415, text = "Save")
        # Reset Button
        canvas.create_rectangle(600, 400, 675, 430, fill = '#e89797')
        canvas.create_text(637, 415, text = "Reset")        
        # Threads
        mode.drawThreads(canvas, mode.page)

class HistoryMode(Mode):
    def appStarted(mode):
        mode.favorites = False
        mode.full = False
        mode.center = False
        mode.image = None
        mode.imagecx = 350
        mode.imagecy = 150

    def images(mode, imageName):
        mode.image = mode.loadImage(imageName)
        mode.maxwidth = 200
        mode.maxheight = 200
        ratio = min(mode.maxwidth/mode.image.width, mode.maxheight/mode.image.height)
        mode.image = mode.scaleImage(mode.image, ratio)
            
    def drawFilterImage(mode, canvas, filter = None, filter2 = None, filter3 = None):
        imagecx = mode.imagecx
        imagecy = mode.imagecy
        x1, y1, x2, y2 = (250, 50, 450, 250)
        for i in range(len(StyleMode.originalImage)):
            if filter3 != None:
                if filter[i] == True and filter2[i] == True and filter3[i] == True:
                    mode.images(StyleMode.pixelated[i])
                    canvas.create_rectangle(x1, y1, x2, y2, fill = 'white')
                    canvas.create_image(imagecx, imagecy, image=ImageTk.PhotoImage(mode.image))
                    imagecx += 250
                    x1 += 250
                    x2 += 250
                    if imagecx > 600:
                        imagecx = 350
                        imagecy += 250
                        x1, x2 = (250, 450)
                        y1 += 250
                        y2 += 250
            elif filter2 != None:
                if filter[i] == True and filter2[i] == True:
                    mode.images(StyleMode.pixelated[i])
                    canvas.create_rectangle(x1, y1, x2, y2, fill = 'white')
                    canvas.create_image(imagecx, imagecy, image=ImageTk.PhotoImage(mode.image))
                    imagecx += 250
                    x1 += 250
                    x2 += 250
                    if imagecx > 600:
                        imagecx = 350
                        imagecy += 250
                        x1, x2 = (250, 450)
                        y1 += 250
                        y2 += 250
            elif filter != None:
                if filter[i] == True:
                    mode.images(StyleMode.pixelated[i])
                    canvas.create_rectangle(x1, y1, x2, y2, fill = 'white')
                    canvas.create_image(imagecx, imagecy, image=ImageTk.PhotoImage(mode.image))
                    imagecx += 250
                    x1 += 250
                    x2 += 250
                    if imagecx > 600:
                        imagecx = 350
                        imagecy += 250
                        x1, x2 = (250, 450)
                        y1 += 250
                        y2 += 250
            elif filter == None:
                mode.images(StyleMode.pixelated[i])
                canvas.create_rectangle(x1, y1, x2, y2, fill = 'white')
                canvas.create_image(imagecx, imagecy, image=ImageTk.PhotoImage(mode.image))
                imagecx += 250
                x1 += 250
                x2 += 250
                if imagecx > 600:
                    imagecx = 350
                    imagecy += 250
                    x1, x2 = (250, 450)
                    y1 += 250
                    y2 += 250            

 
    def drawFilter(mode, canvas):
        # Favorites
        if mode.favorites:
            canvas.create_rectangle(60, 60, 70, 70, fill = 'black')
        else:
            canvas.create_rectangle(60, 60, 70, 70)
        canvas.create_text(125, 65, text = "Favorites")

        # Center
        if mode.center:
            canvas.create_rectangle(60, 80, 70, 90, fill = 'black')
        else:
            canvas.create_rectangle(60, 80, 70, 90)
        canvas.create_text(125, 85, text = "Center")

        # Full Photo
        if mode.full:
            canvas.create_rectangle(60, 100, 70, 110, fill = 'black')
        else:
            canvas.create_rectangle(60, 100, 70, 110)
        canvas.create_text(125, 105, text = "Full Photo")

    def mousePressed(mode, event):
        # Check boxes
        if event.x >= 60 and event.x <= 70\
            and event.y >= 60 and event.y <= 70:
            mode.favorites = not mode.favorites
        elif event.x >= 60 and event.x <= 70\
            and event.y >= 80 and event.y <= 90:
            mode.center = not mode.center
        elif event.x >= 60 and event.x <= 70\
            and event.y >= 100 and event.y <= 110:
            mode.full = not mode.full

        # Arrows
        elif event.x >= 210 and event.x <= 235\
            and event.y >= 230 and event.y <= 270:
            mode.imagecy += 500
            if mode.imagecy > 250:
                mode.imagecy -= 500
        elif event.x >= 715 and event.x <= 740\
            and event.y >= 230 and event.y <= 270:
            mode.imagecy -= 500
            if mode.imagecy < -250 * math.ceil(StyleMode.index/4):
                mode.imagecy += 500 

        # Back Button
        elif event.x >= 15 and event.x <= 90\
            and event.y >= 15 and event.y <= 45:
            mode.app.setActiveMode(mode.app.titleScreenMode)          

    def keyPressed(mode, event):
        if event.key == 'Left':
            mode.imagecy += 250
            if mode.imagecy > 250:
                mode.imagecy -= 250
        elif event.key == 'Right':
            mode.imagecy -= 250
            if mode.imagecy < -250 * math.ceil(StyleMode.index/4):
                mode.imagecy += 250

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "#fac7b9")
        # Filter
        canvas.create_rectangle(50, 50, 200, 450, fill = "white")
        mode.drawFilter(canvas)
        if mode.favorites == False and mode.full == False and mode.center == False:
            mode.drawFilterImage(canvas)
        elif mode.favorites and mode.center:
            mode.drawFilterImage(canvas, StyleMode.fav, StyleMode.centered)
        elif mode.favorites and mode.full:
             mode.drawFilterImage(canvas, StyleMode.fav, StyleMode.full)
        elif mode.full and mode.center:
            mode.drawFilterImage(canvas, StyleMode.full, StyleMode.centered)
        elif mode.favorites:
            mode.drawFilterImage(canvas, StyleMode.fav)
        elif mode.full:
            mode.drawFilterImage(canvas, StyleMode.full)
        elif mode.center:
            mode.drawFilterImage(canvas, StyleMode.centered)
        
        # Arrows
        canvas.create_rectangle(210, 230, 235, 270, fill = 'white')
        canvas.create_polygon(212, 250, 233, 232, 232, 268, fill = 'black')
        canvas.create_rectangle(715, 230, 740, 270, fill = 'white')
        canvas.create_polygon(738, 250, 717, 232, 717, 268, fill = 'black')

        # Back Button
        canvas.create_rectangle(15, 15, 90, 45, fill = '#f7d4a8')
        canvas.create_text(52, 32, text = "Back")

class MyModalApp(ModalApp):
    def appStarted(app):
        app.titleScreenMode = TitleScreenMode()
        app.styleMode = StyleMode()
        app.urlAndPathMode = UrlAndPathMode()
        app.loadMode = LoadMode()
        app.historyMode = HistoryMode()
        app.patternOnlyMode = PatternOnlyMode()
        app.setActiveMode(app.titleScreenMode)

app = MyModalApp(width=800, height=500)


df = pd.DataFrame(list(zip(StyleMode.originalImage, StyleMode.pixelated, StyleMode.threads, StyleMode.full, StyleMode.centered, StyleMode.fav)),\
    columns = ['Original Image', 'Pixelated Image', 'Threads','Full Photo', 'Centered', 'Favorites'])
df.to_csv('history.csv')
