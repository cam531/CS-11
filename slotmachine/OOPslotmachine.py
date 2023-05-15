from fltk import *
import random

class slotmachine(Fl_Window):
    def __init__(self, w, h, label=None): #initializer
        Fl_Window.__init__(self, w, h, label)
        fnames = ['diamond.png', 'iron.png', 'emerald.png', 'redstone.png', 'gold.png'] #call base class initializer
        pbw=50 #pull button width
        imgw= (w-pbw)//3 #width of window - pull button width // each Fl_Box (650-50) // 3, floor div so we get an int
        self.I = [ Fl_PNG_Image(f'pics/{name}').copy(imgw, h) for name in fnames ] #list comprehension

        self.B=[] #list of buttons
        self.begin()
        self.pack = Fl_Pack(0,0,self.w(),self.h())
        self.pack.begin()
        for x in range(3):
            self.B.append(Fl_Box(0, 0, 200,0)) #appends boxes to list
            self.B[-1].box(FL_SHADOW_BOX)
            self.B[-1].color(207)
        self.pull = Fl_Return_Button(0,0,pbw,0,'Pull')
        self.pull.tooltip('Hit enter to play again') #creates tooltip
        self.pull.callback(self.pull_cb) #callback function belongs in class, needs self
        self.pack.end()
        self.pack.type(FL_HORIZONTAL)
        self.end()

    def pull_cb(self,wid): #callback function
        shown=[]
        for x in range(3):
            i=random.randrange(len(self.I)) #random number doesnt need to persist outside the function
            self.B[x].image(self.I[i])
            shown.append(i) #checking indices not images
            self.redraw() #usually B[x].redraw() but images are transparent
        if len(set(shown)) == 1: #remember sets are unique
            fl_message('You win!')

Fl.scheme('plastic')
app = slotmachine(650, 300, 'slotmachine') #app is an instance of subclass slotmachine
app.show()
Fl.run()