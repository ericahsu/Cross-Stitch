# Erica Hsu, 11/30/2020

# Used this image for testing: https://cdn.pixabay.com/photo/2015/04/19/08/33/flower-729512__340.jpg
# Run history.py and webscrape.py first

# cmu_112_graphics downloaded from 15-112 course website: https://www.cs.cmu.edu/~112/schedule.html
from cmu_112_graphics import *
import pandas as pd

# Read in the csv file that has the record of patterns created
history = pd.read_csv('history.csv')

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

        if event.x >= 300 and event.x <= 500\
             and event.y >= 350 and event.y <= 400:
             mode.app.setActiveMode(mode.app.historyMode)

class StyleMode(Mode):
    Mode.history = history
    Mode.index = len(Mode.history)
    Mode.originalImage = Mode.history['Original Image'].tolist()
    Mode.pixelated = Mode.history['Pixelated Image'].tolist()
    Mode.full = Mode.history['Full Photo'].tolist()
    Mode.centered = Mode.history['Centered'].tolist()
    Mode.fav = Mode.history['Favorites'].tolist()
    Mode.styleFull = None
    Mode.styleCenter = None

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
            StyleMode.full.append('True')
            StyleMode.centered.append('False')
            StyleMode.fav.append('False')
            StyleMode.styleFull = True
            mode.app.setActiveMode(mode.app.urlAndPathMode)
        if event.x >= 500 and event.x <= 700 \
            and event.y >= 200 and event.y <= 250:
            StyleMode.full.append('False')
            StyleMode.centered.append('True')
            StyleMode.fav.append('False')
            StyleMode.styleCenter = True
            mode.app.setActiveMode(mode.app.urlAndPathMode)

class UrlAndPathMode(Mode):
    def appStarted(mode):
        mode.urlOrPath = None 

    def userInput(mode):
        mode.urlOrPath = simpledialog.askstring('getUserInput', "url or path")

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "powder blue")
        canvas.create_text(mode.width/2, mode.height/4, text = "Step 2: Type in the url or path to your image", font = "Verdana 30")
        canvas.create_rectangle(100, 200, 700, 250, fill = "white")
        canvas.create_text(400, 225, text = "Click here to type in your url or path", font = "Verdana 24")
        # Back Button
        canvas.create_rectangle(25, 25, 120, 60, fill = 'green')
        canvas.create_text(72, 42, text = "Back")

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
        # Image
        mode.image1 = mode.loadImage(mode.urlOrPath)
        mode.image2 = mode.scaleImage(mode.image1, 2/3)
        mode.image3 = Image.new("L", size=mode.image1.size)
        mode.image4 = Image.new("L", size=mode.image1.size)
        mode.image1 = mode.image1.convert('RGB')
        mode.image2 = Image.new(mode='RGB', size=mode.image1.size)
        mode.imageResult = None
        mode.countOfRgb = {}
        mode.dmcOfImage = {}
        mode.threads = []
        mode.mapOfGray = []
        mode.mapOfRgb = []
        mode.mapOfRgbPix = []
        mode.horizontalFilter = [[-1,0,1], [-2,0,2], [-1,0,1]]
        mode.verticalFilter = [[-1,-2,-1], [0,0,0], [1,2,1]]
        if StyleMode.styleFull:
            mode.result = mode.mapOfRgbValues(mode.image1)
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
        mode.mapOfRgbValues(mode.image1)

    # Creates a 2D list of the rgb values in a given image, pixelates the image,
    # and returns the threads needed
    def mapOfRgbValues(mode, image):

        # 2D list of rgb values in rows and columns
        for x in range(mode.image1.width):
            row = []
            for y in range(mode.image1.height):
                r,g,b = mode.image1.getpixel((x,y))
                row.append((r, g, b))
            mode.mapOfRgb.append(row)

        # Pixelate
        for x in range(0, mode.image2.width - 10, 10):
            for y in range(0, mode.image2.height - 10, 10):
                new = []
                sumr = 0
                sumg = 0
                sumb = 0
                for z in range(10):
                    for w in range(10):
                        r, g, b = mode.mapOfRgb[x + z][y+w]
                        sumr += r
                        sumg += g
                        sumb += b
                sumr = int(sumr/100)
                sumg = int(sumg/100)
                sumb = int(sumb/100)
                index, rgb = mode.findMinDiff((sumr, sumg, sumb), mode.rgb)
                numberAndName = mode.dmc[index] + ' ' + mode.colorName[index]
                if numberAndName not in mode.threads:
                    mode.threads.append(numberAndName)
                for a in range(x, x + 10):
                    for b in range(y, y + 10):
                        mode.image2.putpixel((a, b), rgb)
                

        result = mode.image2
        result.save(f'result{StyleMode.index}.png')
        mode.imageResult = mode.loadImage(f'result{StyleMode.index}.png')

        # Add pixelated image to the history.csv
        StyleMode.pixelated.append(f'result{StyleMode.index}.png')

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

    def listOfThread(mode):
        result = ''
        for thread in mode.threads:
            result = result + thread + '\n'
        return result

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "powder blue")
        # Resize image
        maxwidth = 300
        maxheight = 300
        ratio = min(maxwidth/mode.imageResult.width, maxheight/mode.imageResult.height)
        mode.imageResult = mode.scaleImage(mode.imageResult, ratio)
        canvas.create_image(200, 250, image=ImageTk.PhotoImage(mode.imageResult))
        frame = Frame(canvas, height = 300, width = 300)
        frame.pack(expand = False)
        frame.place(x=400, y=100)
        frame.pack_propagate(0)
        # text window
        text=Text(frame, width=100, height=150, font='Arial 18',\
                    spacing1=5, spacing2=5, wrap=WORD)
        text.pack(side=RIGHT)
        text.insert(END, f"{mode.listOfThread()}")

class HistoryMode(Mode):
    def appStarted(mode):
        mode.favorites = False
        mode.full = False
        mode.center = False
        mode.image = None

    def images(mode, imageName):
        mode.image = mode.loadImage(imageName)
        mode.maxwidth = 200
        mode.maxheight = 200
        ratio = min(mode.maxwidth/mode.image.width, mode.maxheight/mode.image.height)
        mode.image = mode.scaleImage(mode.image, ratio)
            
    def drawFilterImage(mode, canvas, filter = None, filter2 = None, filter3 = None):
        imagecx = 350
        imagecy = 150
        x1, y1, x2, y2 = (250, 50, 450, 250)
        for i in range(len(StyleMode.originalImage)):
            if filter == None:
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
            elif filter3 != None:
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
        if event.x >= 60 and event.x <= 70\
            and event.y >= 60 and event.y <= 70:
            mode.favorites = not mode.favorites
        elif event.x >= 60 and event.x <= 70\
            and event.y >= 80 and event.y <= 90:
            mode.center = not mode.center
        elif event.x >= 60 and event.x <= 70\
            and event.y >= 100 and event.y <= 110:
            mode.full = not mode.full

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "powder blue")
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

class MyModalApp(ModalApp):
    def appStarted(app):
        app.titleScreenMode = TitleScreenMode()
        app.styleMode = StyleMode()
        app.urlAndPathMode = UrlAndPathMode()
        app.historyMode = HistoryMode()
        app.setActiveMode(app.titleScreenMode)
        

app = MyModalApp(width=800, height=500)


df = pd.DataFrame(list(zip(StyleMode.originalImage, StyleMode.pixelated, StyleMode.full, StyleMode.centered, StyleMode.fav)),\
    columns = ['Original Image', 'Pixelated Image', 'Full Photo', 'Centered', 'Favorites'])
df.to_csv('history.csv')
