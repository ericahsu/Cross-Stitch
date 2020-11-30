from cmu_112_graphics import *
import random

class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        font = 'Arial 26 bold'
        canvas.create_text(mode.width/2, 150, text='This demos a ModalApp!', font=font)
        canvas.create_text(mode.width/2, 200, text='This is a modal splash screen!', font=font)
        canvas.create_text(mode.width/2, 250, text='Press any key for the game!', font=font)

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

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
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50

app = MyModalApp(width=500, height=500)