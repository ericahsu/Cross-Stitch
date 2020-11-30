from cmu_112_graphics import *
import pandas as pd

class MyApp(App):
    def appStarted(self):
        # DMC Table
        self.dmcTable = pd.read_csv('dmctable.csv')
        self.rgb = self.dmcTable['RGB']
        self.dmc = self.dmcTable['DMC']
        self.colorName = self.dmcTable['Color']

        # Image
        self.urlOrPath = None
        self.image1 = self.loadImage('testImage2.gif')
        self.image2 = self.scaleImage(self.image1, 2/3)
        self.countOfRgb = {}
        self.dmcOfImage = {}
        self.mapOfRgbValues()
        self.titleScreen = True
        self.urlMode = False
        self.pathMode = False
        #print(self.findMinDiff((68, 12, 20), self.rgb))

    def drawTitleScreen(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill = "CadetBlue1")
        canvas.create_text(self.width/2, self.height/4, text = "Cross Stitch Pattern Maker", font = "Arial 24")
        canvas.create_rectangle(250, 200, 350, 250, fill = "white")
        canvas.create_text(300, 225, text = "URL")
        canvas.create_rectangle(450, 200, 550, 250, fill = "white")
        canvas.create_text(500, 225, text = "Path")

    def drawUrlMode(self, canvas):
        pass

    def drawPathMode(self, canvas):
        pass

    def mousePressed(self, event):
        if event.x > 250 and event.x < 350 and event.y < 250 and event.y > 200\
            and self.titleScreen:
            self.urlMode = True
            self.titleScreen = False
        if event.x > 450 and event.x < 550 and event.y < 250 and event.y > 200\
            and self.titleScreen:
            self.pathMode = True
            self.titleScreen = False
    # def changeUrlMode(self):
    #     self.urlMode = True

    # def changePathMode(self):
    #     return self.pathMode

    # def buildButtons(self, canvas):
    #     canvas.pack()
    #     b1 = Button(canvas, text=" URL  ", command=self.changeUrlMode())
    #     b2 = Button(canvas, text="Path", command=self.changePathMode())
    #     b1.pack(side=LEFT)
    #     b2.pack(side=LEFT)

    def redrawAll(self, canvas):
        self.drawTitleScreen(canvas)
        if self.urlMode:
            self.drawUrlMode(canvas)
        elif self.pathMode:
            self.drawPathMode(canvas)
        # self.buildButtons(canvas)
        # canvas.create_image(200, 300, image=ImageTk.PhotoImage(self.image1))
        # canvas.create_image(500, 300, image=ImageTk.PhotoImage(self.image2))
        
    def mapOfRgbValues(self):
        self.image1 = self.image1.convert('RGB')
        self.image2 = Image.new(mode='RGB', size=self.image1.size)

        imgSmall = self.image1.resize((100, 100),resample=Image.BILINEAR)

        # Scale back up using NEAREST to original size
        result = imgSmall.resize(self.image1.size,Image.NEAREST)

        # Save
        result.save('result.png')
        mapOfRgb = []

        for x in range(100):
            row = []
            for y in range(100):
                r,g,b = imgSmall.getpixel((x,y))
                row.append((r, g, b))
            mapOfRgb.append(row)
        # for x in range(self.image2.width):
        #     row = []
        #     for y in range(self.image2.height):
        #         r,g,b = self.image1.getpixel((x,y))
        #         row.append((r, g, b))
        #     mapOfRgb.append(row)

        # # Dictionary that counts the number of pixels for each rgb value
        for x in mapOfRgb:
            for y in x:
                if y in self.countOfRgb:
                    self.countOfRgb[y] += 1
                else:
                    self.countOfRgb[y] = 1
        threads = []
        for x in self.countOfRgb:
            index, rgb = self.findMinDiff(x, self.rgb)
            numberAndName = self.dmc[index] + ' ' + self.colorName[index]
            if numberAndName not in threads:
                threads.append(numberAndName)
        print(threads)
        print(len(threads))

    # Given two sets of rgb values return the difference
    def findDiff(self, r1, g1, b1, r2, g2, b2):
        diffr = abs(r2 - r1)
        diffg = abs(g2 - g1)
        diffb = abs(b2 - b1)
        totalDiff = diffr + diffg + diffb
        return totalDiff

    def findMinDiff(self, rgb1, rgbTable):
        minimum = None
        closest = None
        minIndex = None
        r1, g1, b1 = rgb1
        for index in range(len(rgbTable)):
            r2, g2, b2 = eval(rgbTable[index])
            diff = self.findDiff(r1, g1, b1, r2, g2, b2)
            if minimum == None or diff < minimum:
                minimum = diff
                closest = rgbTable[index]
                minIndex = index
        return minIndex, closest
        
        

MyApp(width=800, height=500)
