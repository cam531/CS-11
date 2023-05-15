from fltk import *
import subprocess as sp
import signal
import os


def backb_cb(wid):  # callback for back button
    global playing
    stopb_cb(wid)  # stops current song
    line = brow.value()
    brow.value(((brow.value() - 1 - 1) % len(playlist)) + 1)  # goes back 1 in browser
    song = brow.text(brow.value())  # sets selector to new song
    current.value(song)  # changes current song
    playb_cb(wid)  # calls play func


def playb_cb(wid):  # callback for play button
    global playing
    if len(playlist) > 0:
        line = brow.value()     #goes to song selected in browser
        s = playlist[line - 1]
        current.value(songs[line - 1])
        if playing != 0:
            playing.send_signal(signal.SIGTERM)     #stops any music
        playing = sp.Popen(["vlc", "--intf", "dummy", str(s)]) #plays song


def skipb_cb(wid):  # callback for skip button
    global playing
    stopb_cb(wid)  # stops current song
    line = brow.value()
    brow.value(
        ((brow.value() + 1 - 1) % len(playlist)) + 1)  # goes forward 1 in browser
    song = brow.text(brow.value())  # sets selector to new song
    current.value(song)  # changes current song
    playb_cb(wid)  # calls play func


def stopb_cb(wid):  # callback for stop button
    global playing
    if playing != 0:
        playing.send_signal(signal.SIGTERM)  #stops song
    playing = 0
    current.value(None)

def removeb_cb(wid):
    if len(playlist) > 0:
        line = brow.value()
        stopb_cb(wid)  # calls stop function to stop music
        playlist.remove(D.pop(songs.pop(line-1)))  # removes song from everything, accounting for diff in indices
        brow.remove(line)
        brow.value(line)


def close_win(wid):
    if playing != 0:
        playing.send_signal(signal.SIGTERM)  # stops music
    wid.hide()  # hides window


def add_cb(wid):  # menubar callbacks
    global name
    global songs
    d = fl_dir_chooser("Pick a directory to find mp3s", "")  # chooses directory
    dlist = os.listdir(d)
    if d == None:
        return
    for song in dlist:
        if song.endswith(".mp3"):  # checks if file is an mp3
            playlist.append(os.path.join(d, song))  # adds mp3 file to dict
    for song in playlist:  # iterates through list of songs
        songname = song[song.rindex("/") + 1 :]
        songname = songname.replace(".mp3", "")
        D[songname] = song
        songs.append(songname)
    for s in D.keys():
        brow.add(s)  # adds song name to browser, omits path
        brow.take_focus()
        brow.value(1)  # takes focus on line 1 of browser

#key:songname, val:full path of song

def clear_cb(wid):
    global playlist
    brow.clear()  # clears browser
    playlist = []  # clears list of songs


def goplaying_cb(wid):
    brow.value(1)  # goes to first song in browser


def gofirst_cb(wid):
    global playing
    brow.value(playing)  # goes to current song in browser


def golast_cb(wid):
    brow.value(brow.size())  # goes to last song in browser


playing = 0
playlist = []  # list for songs in browser
D = {}  # dict for songs + file path
songname = []  # variable for dict key
songs = []  #list of songs
win = Fl_Window(300, 300, 600, 300, "MP3 Player")
win.begin()

current = Fl_Output(0, 25, win.w(), 25)  # output bar to show current song
current.color(FL_YELLOW)
brow = Fl_Hold_Browser(0, 50, win.w(), 210)

menu = Fl_Menu_Bar(0, 0, win.w(), 25)  # menubar with shortcuts
menu.add("Add/Directory", ord("d"), add_cb)
menu.add("Clear/All", FL_ALT | ord("a"), clear_cb)
menu.add("Go/Playing", ord("p"), goplaying_cb)
menu.add("Go/First", ord("f"), gofirst_cb)
menu.add("Go/Last", ord("l"), golast_cb)

pack = Fl_Pack(0, 260, win.w(), 40)
pack.begin()
backb = Fl_Button(0, 0, 120, 40, "@|<")  # back button
backb.tooltip("Click to go back!")
backb.shortcut(FL_ALT | FL_Left)
playb = Fl_Button(0, 0, 120, 40, "@>")  # play button
playb.tooltip("Click to play!")
playb.shortcut(FL_Enter)
skipb = Fl_Button(0, 0, 120, 40, "@>|")  # skip button
skipb.tooltip("Click to skip!")
skipb.shortcut(FL_ALT | FL_Right)
stopb = Fl_Button(0, 0, 120, 40, "@square")  # stop button
stopb.tooltip("Stop (Space)")
stopb.shortcut(FL_ALT | FL_Enter)
removeb = Fl_Button(0, 0, 120, 40, "@undo")  # remove button
removeb.tooltip("Remove (Del)!")
removeb.shortcut(FL_BackSpace)
pack.end()
pack.type(FL_HORIZONTAL)

win.end()

backb.callback(backb_cb)
playb.callback(playb_cb)  # callback for buttons
skipb.callback(skipb_cb)
stopb.callback(stopb_cb)
removeb.callback(removeb_cb)
win.callback(close_win)

win.resizable(brow)  # allows window and browser to be resized
win.show()
Fl.run()
