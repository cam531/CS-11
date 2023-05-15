from fltk import *
import time
import random

class app(Fl_Window):
    def __init__(self,w,h,label):
        '''init method, creates UI and defines variables and lists'''
        super().__init__(w,h,label)
        self.LB = []  # list for buttons
        self.i = [] #list for index of buttons
        self.all = []  # labels on buttons i.e. 1,2,3
        self.checked = []  # list for buttons already checked
        self.flags = []  # list of flagged square
        self.bombs = []
        self.grid = 10 #grid dimensions
        self.gen = True  # used to find first button clicked
        self.minenum = 10  # number of mines
        for x in range(100):    #fills index list
            self.i.append(x)
        for row in range(10):
            for col in range(10):
                self.LB.append(Fl_Button(col * 75, row * 75, 75, 75))
                self.LB[-1].callback(self.but_cb)

    def around(self, pos):
        '''finds coordinates around clicked button, finds instances of buttons on edges and corners'''
        around = [pos + 1, pos - 1, pos - self.grid, pos + self.grid, pos - self.grid + 1, pos - self.grid - 1,
                       pos + self.grid + 1, pos + self.grid - 1]    #
        realaround = [] #squares around not including cords out of range
        for location in around:  # clears coordinates out of grid
            if location < 0 or location > (self.grid * self.grid - 1):  #checks if button is on top right/bot left corner
                continue
            if pos % self.grid == 0 and location % self.grid == (self.grid - 1):  #checks if button is on top left/bot right corner
                continue
            if pos % self.grid == (self.grid - 1) and location % self.grid == 0: #checks if button is on edges
                continue
            realaround.append(location)
        return realaround

    def assign(self):
        '''counts mines around square and assigns value to each button'''
        for x in range(100):
            count = 0
            if self.all[x] == "NUM":
                a = self.around(x) #calls around function
                for y in a:
                    if self.all[y] == "M":  #checks if mine is around
                        count += 1  #increases count label
                if count != 0:  #changes value of number label i.e. 1,2,3 bombs around
                    self.all[x] = count
                else:
                    self.all[x] = ""

    def generate(self,start):
        '''generates bombs'''
        around = [start, start + 1, start - 1, start - self.grid, start + self.grid, start - self.grid + 1,
                  start - self.grid - 1,start + self.grid + 1, start + self.grid - 1]  # cords around first button clicked
        for x in range(self.grid * self.grid):
            self.all.append("NUM")  # by default every button has a num
        temp = []  #creates list that doesnt have cords of start position plus 8 around, so no mines at start
        for x in range(self.grid * self.grid):
            if x not in around:
                temp.append(x)
        for x in random.sample(temp, self.minenum): #randomly creates mines
            self.bombs.append(x)    #appends cords to list of bombs
            self.all[x] = "M"   #labels bomb with M indicator
        for x in self.bombs:
            self.LB[x].image(Fl_JPEG_Image('bomb.jpg').copy(75,75)) #assigns bomb pic to each button
        self.assign()

    def begin(self,pos):
        '''recursive function to show clear squares'''
        around = [pos, pos + 1, pos - 1, pos - self.grid, pos + self.grid, pos - self.grid + 1,
                       pos - self.grid - 1,pos + self.grid + 1, pos + self.grid - 1]  # cords around first button clicked
        self.LB[pos].label(str(self.all[pos]))  # shows button's value
        self.checked.append(pos)  # stores every revealed square
        self.LB[pos].deactivate()  # deactivates checked button
        if self.all[pos] == "":  # checks if button doesnt have a label
            a = self.around(pos)
            for x in a:  # for each not revealed button
                if x not in self.checked:  # if the button isnt revealed
                    self.begin(x)  # run function again

    def but_cb(self, wid):
        '''callback function for buttons'''
        cords = self.LB.index(wid)
        if cords in self.checked:   #checks if button is already checked
            return 0
        elif self.gen == True:
            self.generate(cords)    #starts game if self is 1st button clicked
            self.begin(cords)
            self.start = time.time()
            self.gen = False
        elif Fl.event_button() == FL_RIGHT_MOUSE:  # conditional for flagging
            if cords in self.flags: #checks if button is already flagged
                self.label(None)
                self.flags.remove(cords)    #removes cords from list of flags
                self.LB[cords].image(None)  #removes flag image from button
                self.LB[cords].deimage()
                return 0
            else:
                img = Fl_JPEG_Image('flag.jpg').copy(75,75)  # draws flag image on button
                self.LB[cords].image(img)
                self.LB[cords].deimage()
                self.flags.append(cords)    #adds cords to list of flags
                self.LB[cords].activate()
                if len(self.flags) == 10:
                    self.check() #calls win function
                return 1
        elif cords in self.flags:
            return 0
        elif self.all[cords] == "M":    #checks if bomb is clicked
            self.LB[cords].label("BOOM")  #indicates clicked bomb
            self.checked.append(cords)
            self.showall()  #calls lose func
            fl_message("You lost!")
        else:
            if self.all[cords] == "": #checks if button is unlabelled/clear of bombs
                self.begin(cords)
            self.label(str(self.all[cords]))
            self.checked.append(cords)
            self.begin(cords)
            self.LB[cords].deactivate() #deactivates cleared bombs
            self.begin(cords)
            if len(self.checked) == 90 and len(self.flags) == 10:   #checks win condition
                self.check()    #calls win func


    def showall(self):
        '''func for win or lose'''
        for x in range(90):
            if x not in self.checked:  # checks if button hasnt been checked
                if x in self.flags and x in self.bombs:  # shows flagged mines
                    self.LB[x].label("X")
                if x in self.flags and x not in self.bombs: #shows incorrect flags
                    self.LB[x].color(FL_RED)
                elif x in self.bombs:  # mines that arent revealed
                    self.LB[x].label(str(self.all[x]))
                    self.LB[x].image(Fl_JPEG_Image('bomb.jpg').copy(75,75))
                elif x not in self.flags:  # any other non revealed squares
                    self.LB[x].label(str(self.all[x]))
                    self.LB[x].deactivate()
        end = time.time()
        self.duration = end - self.start


    def check(self):
        '''win function'''
        #for x in range(self.grid * self.grid):  #
        if len(self.checked) == 100 and len(self.flags) == 10:
            return 0
        self.showall()
        fl_message("You won in " + str(round(self.duration)) + " seconds!")
        name = fl_input("Enter your name")
        highscore = open("highscore.txt", "r+") #opens highscore file and allows reading and writing
        prevscore = (highscore.readline())   #checks previous high score
        if int(round(self.duration)) < int(prevscore):
            highscore.seek(0)   #starts reading file from start
            highscore.truncate()    #clears previous highscore
            highscore.write(str(round(self.duration))) #writes score to highscore file
            highscore.write(str("\n" + name)) #writes name underneath
        highscore.close()

game = app(800,800,"Minesweeper")
game.resizable(game)
game.show()
Fl.run()


















