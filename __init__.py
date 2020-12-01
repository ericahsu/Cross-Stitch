# Erica Hsu, 11/30/2020

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

        # List of Threads Text 
        # Adapted from Hack112 code
        frame = Frame(canvas, height = 300, width = 300)
        frame.pack(expand = False)
        frame.place(x=400, y=100)
        frame.pack_propagate(0)
        # text window
        text=Text(frame, width=100, height=150, font='Arial 18',\
                    spacing1=5, spacing2=5, wrap=WORD)
        text.pack(side=RIGHT)
        
        # Scroll bar
        # scroll=tk.Scrollbar(frame, command=text.yview)
        # scroll.pack(side=RIGHT,fill=Y)
        # # connect scroll bar to text window
        # scroll.config(command=text.yview)
        # text.config(yscrollcommand=scroll.set)
        text.insert(END, f"{mode.threads}")
        #text.config(state = "disabled")

class MyModalApp(ModalApp):
    def appStarted(app):
        app.titleScreenMode = TitleScreenMode()
        app.styleMode = StyleMode()
        app.urlAndPathMode = UrlAndPathMode()
        #app.patternMode = PatternMode()
        app.setActiveMode(app.titleScreenMode)

app = MyModalApp(width=800, height=500)

'''['310 Black', '3750 Antique Blue - VY DK', '500 Blue Green - VY DK', '924 Gray Green - VY DK',
 '3802 Antique Mauve - VY DK', '154 Red - VY DK', '3799 Pewter Gray - VY DK', '223 Shell Pink - LT', 
 '3350 Dusty Rose - ULT DK', '3687 Mauve', '317 Pewter Gray', '939 Blue - VY DK', '3722 Shell Pink - MED',
  '961 Dusty Rose - DK', '938 Coffee Brown - ULT DK', '3790 Beige Gray - ULT DK', '646 Beaver Gray - DK', 
  '3731 Dusty Rose - VY DK', '316 Antique Mauve - MED', '3688 Mauve - MED', '3860 Cocoa', '414 Steel Gray - DK',
   '935 Avocado Green - DK', '962 Dusty Rose - MED', '899 Rose - MED', '779 Brown', '3733 Dusty Rose', 
   '3833 Raspberry - LT', '760 Salmon', '3021 Brown Gray - VY DK', '3835 Grape - MED', '315 Antique Mauve - MED DK',
    '498 Red - DK', '169 Pewter Gray', '3861 Cocoa - LT', '352 Coral - LT', '815 Garnet - MED', '902 Garnet - VY DK', 
    '930 Antique Blue - DK', '3024 Brown Gray - VY LT', '3033 Mocha Brown - VY LT', '543 Beige Brown - ULT VY LT', 
    '453 Shell Gray - LT', '3772 Desert Sand - VY DK', '3773 Desert Sand - MED', '758 Terra Cotta - VY LT', '3778 Terra Cotta - LT',
     '347 Salmon - VY DK', '3726 Antique Mauve - DK', '991 Aquamarine - DK', '644 Beige Gray - MED', '640 Beige Gray - VY DK', 
     '3859 Rosewood - LT', '898 Coffee Brown - VY DK', '3328 Salmon - DK', '610 Drab Brown - DK', '3768 Gray Green - DK',
      '648 Beaver Gray - LT', '452 Shell Gray - MED', '3863 Mocha Beige - MED', '839 Beige Brown - DK', '3685 Mauve - VY DK', '814 Garnet - DK', '817 Coral Red - VY DK', '890 Pistachio Green - ULT DK', '733 Olive Green - MED', '734 Olive Green - LT', '832 Golden Olive', '840 Beige Brown - MED', '838 Beige Brown - VY DK', '321 Red', '150 Red - BRIGHT', '816 Garnet', '934 Avocado Green - BLACK', '502 Blue Green', '501 Blue Green - DK', '561 Jade - VY DK', '3819 Moss Green - LT', '307 Lemon', '973 Canary - BRIGHT', '3820 Straw - DK', '370 Mustard - MED', '666 Red - BRIGHT', '3805 Cyclamen Pink', '3760 Wedgewood - MED', '844 Beaver Gray - ULT DK', '3821 Straw', '3828 Hazelnut Brown', '3804 Cyclamen Pink - DK', '3806 Cyclamen Pink - LT', '3371 Black Brown', '3787 Brown Gray - DK', '309 Rose - DK', '3608 Plum - VY LT', '413 Pewter Gray - DK', '3803 Mauve - DK', '780 Topaz - ULT VY DK', '782 Topaz - DK', '728 Golden Yellow', '3607 Plum - LT', '535 Ash Gray - VY LT', '3826 Golden Brown', '742 Tangerine - LT', '725 Topaz', '3834 Grape - DK', '221 Shell Pink - VY DK', '917 Plum - MED', '602 Cranberry - MED', '3853 Autumn Gold - DK', '868 Hazel Nut Brown', '915 Plum - DK', '434 Brown - LT', '3831 Raspberry - DK', '356 Terra Cotta - MED', '3857 Rosewood - DK', '400 Mahogany - DK', '919 Red Copper', '926 Gray Green - MED', '304 Red - MED', '601 Cranberry - DK', '718 Plum', '645 Beaver Gray - VY DK', '3712 Salmon - MED', '3808 Turquoise - ULT VY DK', '603 Cranberry', '783 Topaz - MED', '921 Copper', '920 Copper - MED', '680 Old Gold - DK', '611 Drab Brown', '300 Mahogany - VY DK', '3721 Shell Pink - DK', '3858 Rosewood - MED', '900 Burnt Orange - DK', '740 Tangerine', '834 Golden Olive - VY LT', '918 Red Copper - DK', '3832 Raspberry - MED', '3852 Straw - VY DK', '720 Orange Spice - DK', '167 Khaki Brown', '3740 Antique Violet - DK', '326 Rose - VY DK', '976 Golden Brown - MED', '3326 Rose - LT', '3779 Terra Cotta - ULT VY LT', '632 Desert Sand - ULT VY DK', '729 Old Gold - MED', '841 Beige Brown - LT', '451 Shell Gray - DK', '801 Coffee Brown - DK', '3041 Antique Violet - MED', '842 Beige Brown - VY LT', '471 Avocado Green - VY LT', '781 Topaz - VY DK', '433 Brown - MED', '3864 Mocha Beige - LT', '3045 Yellow Beige - DK', '970 Pumpkin - LT', '778 Antique Mauve - VY LT', '3072 Beaver Gray - VY LT', '972 Canary - DEEP', '320 Pistachio Green - MED', '822 Beige Gray - LT', '647 Beaver Gray - MED', '977 Golden Brown - LT', '3012 Khaki Green - MED', '928 Gray Green - VY LT', '761 Salmon - LT', '3363 Pine Green - MED', '301 Mahogany - MED', '3052 Green Gray - MED', '503 Blue Green - MED', '168 Silver Gray', '415 Pearl Gray', '927 Gray Green - LT', '3042 Antique Violet - LT', '3023 Brown Gray - LT', '3815 Celadon Green - DK', '726 Topaz - LT', '3862 Mocha Beige - DK', '931 Antique Blue - MED', '3781 Mocha Brown - DK', '3847 Teal Green - DK', '3809 Turquoise - VY DK', '437 Tan - LT', '600 Cranberry - VY DK', '891 Carnation - DK', '335 Rose', '950 Desert Sand - LT', '3816 Celadon Green', '407 Desert Sand - DK', '3064 Desert Sand', '402 Mahogany - VY LT', '318 Steel Gray - LT', '422 Hazelnut Brown - LT', '3782 Mocha Brown - LT', '3032 Mocha Brown - MED', '3830 Terra Cotta', '3848 Teal Green - MED', '3364 Pine Green', '833 Golden Olive - LT', '3822 Straw - LT', '777 Red - DEEP', '163 Green', '975 Golden Brown - DK', '604 Cranberry - LT', '371 Mustard', '3777 Terra Cotta - VY DK', '355 Terra Cotta - DK', '946 Burnt Orange - MED', '420 Hazelnut Brown - DK', '367 Pistachio Green - DK', '3829 Old Gold - VY DK', '166 Lime Green', '932 Antique Blue - LT', '612 Drab Brown - LT', '869 Hazelnut Brown - VY DK', '436 Tan', '349 Coral - DK']
220'''