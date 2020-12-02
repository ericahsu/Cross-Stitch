from cmu_112_graphics import *
import pandas as pd

class MyApp(App):
    def appStarted(self):
        url = 'https://tinyurl.com/great-pitch-gif'
        url = 'https://cdn.pixabay.com/photo/2015/04/19/08/32/marguerite-729510__340.jpg'
        self.image1 = self.loadImage(url)
        self.image1 = self.image1.convert('RGB')
        self.image2 = Image.new("L", size=self.image1.size)
        self.image3 = Image.new("L", size=self.image1.size)
        self.mapOfGray = []
        self.mapOfGrayscale()
        self.horizontalFilter = [[-1,0,1], [-2,0,2], [-1,0,1]]
        self.verticalFilter = [[-1,-2,-1], [0,0,0], [1,2,1]]


    def multiplyMatrices(self, m1, m2):
        final = []
        for x in range(len(m1)):
            row = []
            for y in range(len(m1[0])):
                element = m1[x][y] * m2[x][y]
                row.append(element)
            final.append(row)
        return final

    def sumValues(self, m):
        total = 0
        for x in range(len(m)):
            for y in range(len(m[0])):
                if isinstance(m[x][y], int):
                    total += m[x][y]
                else:
                    total = total
        return total

    def mapOfGrayscale(self):
        for x in range(self.image2.width):
            row = []
            for y in range(self.image2.height):
                r,g,b = self.image1.getpixel((x,y))
                grayscale = ((0.3 * r) + (0.59 * g) + (0.11 * b))
                grayscale = int(grayscale)
                row.append(grayscale)
            self.mapOfGray.append(row)


        for x in range(self.image2.width):
            for y in range(self.image2.height):
                r,g,b = self.image1.getpixel((x,y))
                grayscale = ((0.3 * r) + (0.59 * g) + (0.11 * b))
                grayscale = int(grayscale)
                self.image2.putpixel((x, y), grayscale)

        for x in range(0, self.image2.width - 2, 3):
            for y in range(0, self.image2.height - 2, 3):
                new = []
                new.append(self.mapOfGray[x][y:y+3])
                new.append(self.mapOfGray[x + 1][y:y+3])
                new.append(self.mapOfGray[x + 2][y:y + 3])
                verticalPixels = self.multiplyMatrices([[-1,-2,-1], [0,0,0], [1,2,1]], new)
                verticalScore = self.sumValues(verticalPixels)/4
                #print(verticalPixels)
                horizontalPixels = self.multiplyMatrices([[-1,0,1], [-2,0,2], [-1,0,1]], new)
                #print(horizontalPixels)
                horizontalScore = self.sumValues(horizontalPixels)/4
                edgeScore = (verticalScore**2 + horizontalScore**2)**.5
                edgeScore = int(edgeScore)
                for a in range(x, x + 3):
                    for b in range(y, y + 3):
                        #self.image3.putpixel((a, b), edgeScore)
                        if edgeScore >= 30:
                            self.image3.putpixel((a, b), 255)
                        elif edgeScore < 30:
                            self.image3.putpixel((a, b), 0)
                # grayscale = ((0.3 * r) + (0.59 * g) + (0.11 * b))
                # grayscale = int(grayscale)
                # self.image2.putpixel((x, y), grayscale)
                # self.image2.putpixel((x, y), 255)       

        for y in range(self.image3.height):
            for x in range(self.image3.width):
                if self.image3.getpixel((x, y)) == 0:
                    self.image1.putpixel((x, y), (255, 255, 255))
                if self.image3.getpixel((x, y)) != 0:
                    break
        for y in range(self.image3.height-1, -1, -1):
            for x in range(self.image3.width-1, -1, -1):
                if self.image3.getpixel((x, y)) == 0:
                    self.image1.putpixel((x, y), (255, 255, 255))
                if self.image3.getpixel((x, y)) != 0:
                    break
        for x in range(self.image3.width - 1, -1, -1):
            for y in range(self.image3.height - 1, -1, -1):
                if self.image3.getpixel((x, y)) == 0:
                    self.image1.putpixel((x, y), (255, 255, 255))
                if self.image3.getpixel((x, y)) != 0:
                    break
        for x in range(self.image3.width):
            for y in range(self.image3.height):
                if self.image3.getpixel((x, y)) == 0:
                    self.image1.putpixel((x, y), (255, 255, 255))
                if self.image3.getpixel((x, y)) != 0:
                    break

    def redrawAll(self, canvas):
        canvas.create_image(200, 300, image=ImageTk.PhotoImage(self.image1))
        canvas.create_image(700, 300, image=ImageTk.PhotoImage(self.image3))

MyApp(width=1000, height=600)
