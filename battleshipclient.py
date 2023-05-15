#tcp client
from fltk import *
import socket

class ShipBut(Fl_Button):
    def __init__(self, r, c, x, y, w, h, label=None):
        super().__init__(x, y, w, h, label)
        self.row = r
        self.col = c

class board(Fl_Window):
   def __init__(self, x, y, w, h, label):
       Fl_Window.__init__(self, x, y, w, h, label)
       self.ss = 1  # ship size
       self.siz = 10  # board size
       self.placed = 0  # placed ships
       self.hit = 0  # hit ship squares
       self.but = []  # 2dlist for left buts
       self.ships = []  # ships
       self.mybuts = []  # all of my (left) buttons
       self.yourbuts = []  # your (right) buttons
       self.but2 = []  # 2d list for right buts
       self.begin()
       self.conbut = Fl_Light_Button(100, 550, 270, 40, "Connect")  # light widget to indicate connection
       self.changebut = Fl_Button(500, 550, 270, 40, "Change host and port")
       self.changebut.callback(self.changebut_cb)
       self.conbut.callback(self.conbut_cb)  # calback for connection button
       for r in range(self.siz):
           row = []
           for c in range(self.siz):
               row.append(ShipBut(r, c, c * 40, r * 40, 40, 40, f'{r},{c}'))  # creates ship grid
               row[-1].callback(self.putship)
               self.mybuts.append(row[-1])  # creates a 2d list with 10 instances of row
           self.but.append(row)
       for row in range(self.siz):
           opponent = []
           for col in range(self.siz):
               opponent.append(
                   ShipBut(row, col, 500 + (col * 40), row * 40, 40, 40, f'{row},{col}'))  # creates shooting grid
               opponent[-1].callback(self.shots)
               opponent[-1].deactivate()
               self.yourbuts.append(opponent[-1])  # creates a 2d list with 10 instances of opponent
           self.but2.append(opponent)
       self.end()
       self.callback(self.close)

   def changebut_cb(self, wid):
       '''callback to change host and port'''
       self.host = fl_input("Enter an IP:")  # input for IP/hostname
       self.port = fl_input("Enter a port:")  # input for port

   def putship(self, wid):
       '''places ships, makes sure ships don't overlap'''
       r = wid.row
       c = wid.col
       if wid.color() == FL_BLUE:  # checks if ship is already on square/button
           pass
       else:
           if self.ss <= 4:  # checks number of ships + ship size
               if Fl.event_button() == FL_LEFT_MOUSE:  # places ships horizontally
                   if c + self.ss <= self.siz:
                       for x in range(self.ss):
                           if self.but[r][c + x].color() == FL_BLUE:
                               break
                           else:
                               self.but[r][c + x].color(FL_BLUE)
                               self.but[r][c + x].redraw()
                               self.ships.append(self.but[r][c + x])  # adds to list of ship squares
                       self.ss += 1
                       self.placed += 1

               if Fl.event_button() == FL_RIGHT_MOUSE:  # places ships vertically
                   if r + self.ss <= self.siz:
                       for x in range(self.ss):
                           if self.but[r + x][c].color() == FL_BLUE:
                               break
                           else:
                               self.but[r + x][c].color(FL_BLUE)
                               self.but[r + x][c].redraw()
                               self.ships.append(self.but[r + x][c])
                       self.ss += 1
                       self.placed += 1
           else:  # checks if 4 ships already placed
               self.ready()
       if self.placed == 4:
           self.ready()
           for buttons in self.mybuts:
               buttons.deactivate()

   def ready(self):
       '''tells other side that you are ready'''
       self.s.sendall('ready'.encode())
       # send data that each is ready

   def shots(self, wid):
       '''function for shots'''
       r = wid.row
       c = wid.col
       cords = str(r) + " " + str(c)
       self.s.sendall(cords.encode())
       fl_message("Server's turn")
       for button in self.yourbuts:
           button.deactivate()


   def shotat(self,data):
       for button in self.yourbuts:
           if button.color() != FL_RED and button.color() != FL_WHITE:
               button.activate()
       cords = data.split()
       row = int(cords[0])
       col = int(cords[1])
       but = self.but[row][col]
       if but in self.ships:  # sets hit square to red
           but.color(FL_RED)
           but.deactivate()
           but.redraw()
           self.hit += 1
           cords = (str(row) + " " + str(col))
           self.s.sendall(('hit' + cords).encode())
       else:
           but.color(FL_WHITE)  # sets miss square to white
           but.deactivate()
           but.redraw()
           cords = (str(row) + " " + str(col))
           self.s.sendall(('miss' + cords).encode())
       self.sunk(data)
       self.lose()

   def sunk(self, data):
       '''function to track sunk ships'''
       if self.ships[0].color() == FL_RED:
           self.ships[0].color(FL_BLACK)
           self.ships[0].redraw()
       if self.ships[1].color() == FL_RED and self.ships[2].color() == FL_RED:
           self.ships[1].color(FL_BLACK)
           self.ships[2].color(FL_BLACK)
           self.ships[1].redraw()
           self.ships[2].redraw()
       if self.ships[3].color() == FL_RED and self.ships[4].color() == FL_RED and self.ships[5].color() == FL_RED:
           self.ships[3].color(FL_BLACK)
           self.ships[4].color(FL_BLACK)
           self.ships[5].color(FL_BLACK)
           self.ships[3].redraw()
           self.ships[4].redraw()
           self.ships[5].redraw()
       if self.ships[6].color() == FL_RED and self.ships[7].color() == FL_RED and self.ships[8].color() == FL_RED and self.ships[9].color() == FL_RED:
           self.ships[6].color(FL_BLACK)
           self.ships[7].color(FL_BLACK)
           self.ships[8].color(FL_BLACK)
           self.ships[9].color(FL_BLACK)
           self.ships[6].redraw()
           self.ships[7].redraw()
           self.ships[8].redraw()
           self.ships[9].redraw()
       else:
           pass


   def lose(self):
       '''lose function, checks if all ship squares are hit, sends win message to client'''
       if self.hit == 10:
           fl_message('You lose!')
           self.s.sendall('You win!'.encode())
           for buttons in self.mybuts():
               buttons.deactivate()
           for buttons in self.yourbuts():
               buttons.deactivate()
       else:
           pass

   def conbut_cb(self, wid):
       self.host = 'localhost'
       self.port = 12345
       self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #fd=3

       self.s.connect((self.host,self.port))
       self.fd=self.s.fileno() #3
       Fl.add_fd(self.fd, self.receive_data)

   def close(self,wid):
       try:
           self.s.close()
       except:
           print('closing without a connection')
       finally:
           self.hide()

   def receive_data(self, fd):
       data=self.s.recv(1024)
       data.decode()
       if data == b'ready':
           fl_message('wait for server to shoot!')
           for button in self.yourbuts:
               button.deactivate()
       elif data==b'':
           self.s.close()
           Fl.remove_fd(self.fd)

       elif data[:3] == b'hit':
           cords = data[3:].split()
           row = int(cords[0])
           col = int(cords[-1])
           but = self.but2[row][col]
           but.color(FL_RED)
           but.redraw()
       elif data[:4] == b'miss':
           cords = data[4:].split()
           row = int(cords[0])
           col = int(cords[-1])
           but = self.but2[row][col]
           but.color(FL_WHITE)
           but.redraw()
       elif data == b'You win!':
           fl_message("You win!")

       else:
           self.shotat(data)


app = board(55, 55, 900, 600, "Client")
app.show()
Fl.run()
