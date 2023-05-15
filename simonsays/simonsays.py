from fltk import *
import subprocess as sp
import signal
import random


class mybut(Fl_Button):
    def __init(self, x, y, w, h, label=""):
        '''initializer for button class'''
        super().__init__(x, y, w, h, label)

    def handle(self, event):
        '''method to handle events'''
        retval = super().handle(event)
        if event == FL_PUSH:
            if self.color() == FL_GRAY: #self refers to button class in this method
                return retval
            Fl.remove_timeout(app.pushed) #removes 5 sec timeout for when button held
            Fl.remove_timeout(app.nopush)   #removes 5 sec timeout for when nothing is pressed
            index = app.colors.index(self.color())
            self.pid = sp.Popen(["vlc", "--intf", "dummy", app.sounds[index]])  #plays sound that matches with button color
            Fl.add_timeout(5.0, app.pushed, self) #5 sec timer
            return 1
        if event == FL_RELEASE:
            if self.pid != 0:   #checks if sound is playing
                self.pid.send_signal(signal.SIGTERM) #stops sound
                Fl.remove_timeout(app.pushed)
                return 1
        return retval


class interface(Fl_Window):
    def __init__(self, w, h, label):
        Fl_Window.__init__(self, w, h, label)   #call base class init

        self.colors = [FL_GREEN, FL_RED, FL_YELLOW, FL_BLUE] #list of colors
        self.sounds = ["green.wav", "red.wav", "yellow.wav", "blue.wav"]
        self.shortsounds = ["greens.wav", "reds.wav", "yellows.wav", "blues.wav"]   #list of sounds
        self.sequence = []  #tracks given sequence
        self.clicked = []   #tracks input sequence
        self.buttons = []   #keeps track of buttons
        self.score = 0  #score counter
        self.begin()
        self.greenbut = mybut(100, 100, 200, 200)
        self.greenbut.color(FL_GREEN)
        self.greenbut.callback(self.clicked_cb)
        self.buttons.append(self.greenbut)
        self.redbut = mybut(400, 100, 200, 200)
        self.redbut.color(FL_RED)
        self.redbut.callback(self.clicked_cb)
        self.buttons.append(self.redbut)
        self.yellowbut = mybut(100, 400, 200, 200)
        self.yellowbut.color(FL_YELLOW)
        self.yellowbut.callback(self.clicked_cb)
        self.buttons.append(self.yellowbut)
        self.bluebut = mybut(400, 400, 200, 200)
        self.bluebut.color(FL_BLUE)
        self.bluebut.callback(self.clicked_cb)
        self.buttons.append(self.bluebut)
        self.startbut = Fl_Button(300, 300, 100, 100, "Start")
        self.startbut.callback(self.startbut_cb)
        self.end()

    def activate_all(self):
        '''function for activating buttons '''
        for button in self.buttons:
            button.activate()

    def deactivate_all(self):
        '''function for deactivating buttons'''
        for button in self.buttons:
            button.deactivate()

    def startbut_cb(self, wid):
        """callback function for start button"""
        self.sequence.clear()   #clears lists
        self.clicked.clear()
        for button in self.buttons: #sets all button values to original color
            button.value(0)
        self.redraw()
        self.pattern()  #start showing sequence


    def pattern(self):
        """method to create sequence"""
        self.sequence.append(random.choice(self.colors))    #adds random color to sequence
        self.deactivate_all()
        for x in range(len(self.sequence)):
            index = self.colors.index(self.sequence[x]) #finds index of color in list of colros
            Fl.add_timeout(1 * (x + 1), self.flash, index)  #pushes timeouts farther into the future,creates delay between each flash
        Fl.add_timeout((len(self.sequence) + 1), self.activate_all) #5 sec timer for when sequence is done showing
        Fl.add_timeout(5.0 + (len(self.sequence) + 1), self.nopush)

    def flash(self, index):
        """method to flash button"""
        self.buttons[index].color(FL_GRAY)  #changes color of button to gray
        self.buttons[index].redraw()
        Fl.add_timeout(0.5, self.flashback, index) #timeout for length of flash
        sp.Popen(["vlc", "--intf", "dummy", self.shortsounds[index]])

    def flashback(self, index):
        """method to finish button flash"""
        self.buttons[index].color(self.colors[index])   #changes color of button back to original color
        self.buttons[index].redraw()

    def clicked_cb(self, wid):
        """method to check for correct sequence"""
        color = wid.color()
        self.clicked.append(color)  #tracks clicked buttons
        if self.clicked[len(self.clicked) - 1] != self.sequence[len(self.clicked) - 1]: #checks each part of sequence to see if its wrong
            self.lose() #call lose method
        elif len(self.clicked) == len(self.sequence):
            self.score += 1
            self.pattern()
            self.clicked = []   #checks last color, continues game, play sequence
        else:   #correct but not finished, keeps checking
            return

    def pushed(self, wid):
        """method to manage timouts and 5 sec rule"""
        Fl.remove_timeout(self.pushed)
        self.lose()

    def nopush(self):
        """tracks 5 sec rule"""
        Fl.remove_timeout(self.nopush)
        self.lose()

    def lose(self):
        """method for losing protocol"""
        pid = sp.Popen(["vlc", "--intf", "dummy", "wrong.wav"]) #plays incorrect sound
        fl_message("Incorrect! Your score was " + str(self.score) + " turns")
        highscore = open("highscore.txt", "r+") #opens highscore file and allows reading and writing
        prevscore = int(highscore.readline())   #checks previous high score
        if int(self.score) > int(prevscore):
            highscore.seek(0)   #starts reading file from start
            highscore.truncate()    #clears previous highscore
            self.score = str(self.score)    #changes int score value to string for writing
            highscore.write(self.score) #writes score to highscore file
        highscore.close()


app = interface(700, 700, "Simon Says")
app.resizable(app)
app.show()
Fl.run()











