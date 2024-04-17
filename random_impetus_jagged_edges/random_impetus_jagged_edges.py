from neoscore.core import neoscore
from neoscore.core.units import Mm, Unit
from neoscore.core.point import ORIGIN, ZERO
from neoscore.core.path import Path
from neoscore.core.brush import Brush, Color, BrushPattern
from neoscore.core.pen import Pen, PenPattern
from neoscore.core.music_text import MusicText, MusicFont
from neoscore.core.path import Path
from neoscore.core.text import Text, Font
from neoscore.core.rich_text import RichText
from neoscore.western.staff import Staff
from typing import Optional
from time import time
import time as tm
import random
import math
import threading
import drawings
import os
import sys

neoscore.setup()

#Create bounding rectangle for rendering purposes
boundingRectColor = "FFFFFF"
boundingRect = Path.rect((Mm(-1000000), Mm(-1000000)), None, Mm(2000000), Mm(2000000),
      boundingRectColor, Pen.no_pen())

#Set viewport initial position
window_center_x = Unit(0)
window_center_y = Unit(0)

#Initial viewport position
neoscore.set_viewport_center_pos((Unit(40), window_center_y-Unit(15)))

#Initial staff length
staffLength = Mm(30)
#Initialize brush and pen
color = "000000"
brush = Brush(color)
pen = Pen(color, Unit(0.35))

#Create staff object in center of viewport
staff = Staff((window_center_x, window_center_y), None, staffLength, pen=pen)
s = staff
font = MusicFont("Bravura", s.unit(1))
#Braxton diamond clef
diamondClef = Path((s.unit(-0.5), s.unit(2)), s, Brush("000000", BrushPattern.INVISIBLE), Pen("000000", Mm(0.4), PenPattern.SOLID))
diamondClef.line_to(s.unit(0.5), s.unit(4), s)
diamondClef.line_to(s.unit(1.5), s.unit(2), s)
diamondClef.line_to(s.unit(0.5), s.unit(0), s)
diamondClef.close_subpath()
#Note on first line of staff
firstNote = MusicText((s.unit(6), s.unit(4)), s, "noteheadBlack", font, brush)

staff2Length = Mm(30)

def newStaff():
    global staff2
    staff2 = Staff((window_center_x, Mm(20)), staff, staff2Length, pen=pen)


def menuScreen():
    global startScreen, instructions, border
    border = Path.rect((window_center_x-Mm(48), window_center_y-Mm(30)), None, Mm(96), Mm(60), Brush("F59400"), Pen("000000", Unit(1)))
    
    startScreen = Path.rect((window_center_x-Mm(37), window_center_y-Mm(26)-Unit(2)), None, Mm(75), Mm(53), Brush("0EE0F4"), Pen("E9FBFF"))
    text = """<p align=center style="color: #000000"><strong>__random_impetus - jagged_edges__</strong><br><br>Press [space] to begin piece. Start playing when the staff begins to move. Press [r] to reset piece.<br><br>Press the +/- keys to zoom in and out. Make sure the top border of the orange box is just barely within the screen before starting.</p>"""
    instructions = RichText((Mm(-34), Mm(-24)-Unit(2)), None, text, Mm(70), Font("Times New Roman", Unit(12)))

    neoscore.set_refresh_func(startPiece, 30)

def startPiece(t: float) -> Optional[neoscore.RefreshFuncResult]:
    neoscore.set_viewport_center_pos((ZERO, window_center_y))
    
pieceStartReady = True

#Set user input controls
def key_handler(event):
    global pieceStartReady, viewScale, startTime
    if event.text == ' ' and pieceStartReady:
        pieceStartReady = False
        #Save time at beginning of program
        startTime = time()
        startScreen.remove()
        instructions.remove()
        border.remove()
        threading.Thread(target=changeRefresh).start()
    if event.text == 'r' and not pieceStartReady:
        os.execv(sys.executable, ['python'] + sys.argv)
    #Set zoom scale
    if event.text == '=':
        viewScale += 0.1
        neoscore.set_viewport_scale(viewScale)
    if event.text == '-':
        viewScale -= 0.1
        neoscore.set_viewport_scale(viewScale)

#Initial zoom value
viewScale = 6 #6 is default
neoscore.set_viewport_scale(viewScale)

#Makes the menu appear at start and allows user input to be detected
menuScreen()
neoscore.set_key_event_handler(key_handler)


#Changes over to animation function once the user begins the piece
def changeRefresh():
    tm.sleep(3.0)
    #Set animation function
    neoscore.set_refresh_func(refresh, 30)


#Checkpoint variables in seconds before event occurs
checkpoint1 = 60.0 #60.0
checkpoint2 = checkpoint1+40.0 #40.0
checkpoint3 = checkpoint2+25.0 #25.0
checkpoint4 = checkpoint3+45.0 #45.0
checkpoint5 = checkpoint4+55.0 #60.0
checkpoint6 = checkpoint5+60.0 #60.0
checkpoint7 = checkpoint6+50.0 #50.0

#Initial note position
newNoteXPos = firstNote.pos.x

#Starting scroll speed
initialScrollVelocity = 1.5
currentScrollVelocity = initialScrollVelocity

#Time after pressing [space] before piece starts moving
startTime = 0.0
startDelay = 3.0

#Other initial variables
checkpointNumber = 0
noteDensity = 0.0
elapsedTime = 0.0
saveTime = 0.0
newTime = 0.0
computerClock = 0.0
scroll_xpos = 0.0
scroll_ypos = window_center_y
generateNotes = True
speedTrigger = True
speedChangeType = 'None'
modifierX = Mm(scroll_xpos)-Mm(52)
modifierY = Mm(25)
modifierPath = Path.ellipse_from_center((modifierX, modifierY), staff, Mm(10), Mm(10), Brush(pattern=BrushPattern.INVISIBLE), Pen.no_pen())
fadeout = 0


#note possibilities
notes = [s.unit(-0.5), s.unit(0), s.unit(0.5), s.unit(1), s.unit(1.5), s.unit(2), s.unit(2.5), s.unit(3), s.unit(3.5), s.unit(4), s.unit(4.5)]

def PickNote(): #Randomly chooses a note (staff position)
    newNote = random.choice(notes)
    return newNote

def prevNotePos(): #Saves position of generated note to use as a condition to avoid collisions
    global lastPrintedNote
    lastPrintedNote = newNoteXPos

#Create empty dictionary for accidentals
accidentalNotes = {}

def randomNote(staffChoice): #Actually creates the note from PickNote()
    global newNoteXPos, accidentalNotes
    x_pos = neoscore.get_viewport_center_pos().x + Mm(20) #Places notes a little ahead of the viewport center
    y_pos = PickNote()
    self = MusicText((x_pos, y_pos), staffChoice, "noteheadBlack", font, brush) #Generate the note

    if accidentalNotes.get(f'{y_pos}') != None: #If the dictionary has items in it, print a sharp or a flat
        if (accidentalNotes.get(f'{y_pos}') == ['accidentalSharp']):
            MusicText((Unit(-5.5), ZERO), self, 'accidentalSharp', font, brush)
        else:
            MusicText((Unit(-5), ZERO), self, 'accidentalFlat', font, brush)

    #Save this note's x position to avoid collisions
    newNoteXPos = self.pos.x
    prevNotePos()

    deleteNoteThread = threading.Thread(target=deleteNote, args=(self,))
    deleteNoteThread.start()

def deleteNote(self):
    tm.sleep(5.0)
    self.remove()

def setAccidental(): #Fill dictionary accidentalNotes to align accidental y position with noteheads
    global accidentalNotes
    accidentalNote = random.choice(notes)
    accidentalType = random.choices(("accidentalSharp", "accidentalFlat"), (50, 50), k=1)
    accidentalNotes[f'{accidentalNote}'] = accidentalType
    if accidentalNote == s.unit(4.5):
        accidentalNotes[f'{s.unit(1)}'] = accidentalType
    if accidentalNote == s.unit(1):
        accidentalNotes[f'{s.unit(4.5)}'] = accidentalType
    if accidentalNote == s.unit(4):
        accidentalNotes[f'{s.unit(0.5)}'] = accidentalType
    if accidentalNote == s.unit(0.5):
        accidentalNotes[f'{s.unit(4)}'] = accidentalType
    if accidentalNote == s.unit(3.5):
        accidentalNotes[f'{s.unit(0)}'] = accidentalType
    if accidentalNote == s.unit(0):
        accidentalNotes[f'{s.unit(3.5)}'] = accidentalType
    if accidentalNote == s.unit(3):
        accidentalNotes[f'{s.unit(-0.5)}'] = accidentalType
    if accidentalNote == s.unit(-0.5):
        accidentalNotes[f'{s.unit(3)}'] = accidentalType


def changeBackgroundColor():
    global boundingRect, boundingRectColor
    choice = random.choices(('orange', 'skyBlue', 'yellow'), (36, 32, 32))
    if choice == ['orange']:
        boundingRectColor = "F59400"
    elif choice == ['skyBlue']:
        boundingRectColor = "0EE0F4"
    elif choice == ['yellow']:
        boundingRectColor = "F5E601"
    '''elif choice == ['red']:
        boundingRectColor = "F76757"'''

    boundingRect.brush = boundingRectColor
    threading.Thread(target=backgroundWhite).start()

def backgroundWhite():
    global boundingRect, boundingRectColor
    tm.sleep(random.uniform(5.0, 15.0))
    boundingRectColor = "FFFFFF"
    boundingRect.brush = boundingRectColor

def changeModifier():
    modifierPath.pen = Pen("000000", Unit(1))

    choice = random.choices(('solo', 'duet', 'quarterSharp', 'quarterFlat', 'unpitched', 'bright', 'dark'), (25, 25, 4, 4, 14, 14, 14))
    if choice == ['solo']:
        #glyph = MusicText((Mm(3.2), Mm(5)), modifierPath, "timeSig1", MusicFont("Bravura", Unit(1)), scale=7)
        glyph = Text((Mm(2.9), Mm(7.9)), modifierPath, "1", Font("Times New Roman", Unit(24), 75))
    elif choice == ['duet']:
        #glyph = MusicText((Mm(2.8), Mm(5)), modifierPath, "timeSig2", MusicFont("Bravura", Unit(1)), scale=7)
        glyph = Text((Mm(3), Mm(7.9)), modifierPath, "2", Font("Times New Roman", Unit(24), 60))
    elif choice == ['quarterSharp']:
        glyph = MusicText((Mm(4.1), Mm(4.8)), modifierPath, "accidentalQuarterToneSharpStein", MusicFont("Bravura", Unit(1)), scale=7)
    elif choice == ['quarterFlat']:
        glyph = MusicText((Mm(3.5), Mm(6.2)), modifierPath, "accidentalQuarterToneFlatStein", MusicFont("Bravura", Unit(1)), scale=7)
    elif choice == ['unpitched']:
        glyph = Text((Mm(2.2), Mm(7.9)), modifierPath, "X", Font("Arial", Unit(24)))
    elif choice == ['bright']:
        glyph = Text(ORIGIN, modifierPath, "")
    elif choice == ['dark']:
        glyph = Text(ORIGIN, modifierPath, "")
        modifierPath.brush = Brush("000000")

    duration = random.uniform(8.0, 15.0)

    #Longer duration for solo and duet sections
    if choice == ['solo'] or choice == ['duet'] and duration <= 10.0:
        duration += random.uniform(6.5, 12.0)

    threading.Thread(target=resetModifier, args=(glyph, duration)).start()
    
def resetModifier(glyph, duration):
    tm.sleep(duration)
    modifierPath.pen = Pen.no_pen()
    modifierPath.brush = Brush.no_brush()
    glyph.remove()


#Function for changing animation scroll speed
def speedUp():
    global currentScrollVelocity
    probability = bool(random.getrandbits(1))
    if probability:
        currentScrollVelocity = 1.2
    else:
        currentScrollVelocity = 1.0

def slowDown():
    global currentScrollVelocity
    currentScrollVelocity = random.uniform(0.3, 0.5)

def resetSpeedFast():
    global currentScrollVelocity, initialScrollVelocity, speedTrigger
    tm.sleep(1.5)
    currentScrollVelocity = initialScrollVelocity
    speedTrigger = True

def resetSpeedRand(sleepTime):
    global currentScrollVelocity, initialScrollVelocity, speedTrigger, generateNotes
    tm.sleep(sleepTime)
    currentScrollVelocity = initialScrollVelocity
    generateNotes = True
    speedTrigger = True

def stopScroll():
    global currentScrollVelocity, initialScrollVelocity, speedTrigger, generateNotes
    generateNotes = False
    speedTrigger = False
    currentScrollVelocity = 0.0


#Animation function allowing the piece to move and determining when other functions are triggered
def refresh(t: float) -> Optional[neoscore.RefreshFuncResult]: 
    global checkpointNumber, initialScrollVelocity, currentScrollVelocity, noteDensity, elapsedTime, newTime, computerClock, scroll_xpos, scroll_ypos, speedTrigger, speedChangeType, saveTime, staff2, modifierX, modifierY, fadeout, blackScreen, generateNotes
    computerClock = t
    prevNotePos() #Constant tracking of previous note's x position
    elapsedTime = computerClock - startTime #Number of seconds since start of piece
    scroll_xpos += currentScrollVelocity #Scroll right at rate determined by velocity
    staff._length = Mm(30) + Mm(scroll_xpos) #Grow staff to the right at the same rate as viewport scroll
    minimumNoteDistance = (neoscore.get_viewport_center_pos().x + Mm(20))-lastPrintedNote #Distance to avoid note collisions

    neoscore.set_viewport_center_pos((Mm(scroll_xpos)-Unit(30.0), scroll_ypos)) #Move the viewport right

    #Moves the modifier symbol with the viewport
    modifierX = neoscore.get_viewport_center_pos().x-Mm(5)
    modifierY = scroll_ypos-Mm(28)
    modifierPath.pos = (modifierX, modifierY)

    #Note spawn density calculations
    max = 0.03
    min = 0.005
    sinLFO = math.sin((computerClock/2))
    
    #Calculates note density
    if speedTrigger is False and speedChangeType == 'Fast':
        noteDensity = 100.0
    elif speedTrigger is False and speedChangeType == 'Slow':
        noteDensity = 0.005
    else:
        noteDensity = ((max - min) * sinLFO + max + min) / 2

    #Events to be potentially performed at any moment
    #Probability to spawn a note
    if (minimumNoteDistance) > staff.unit(2) and generateNotes:
        if (elapsedTime % 0.2) <= noteDensity:
            randomNote(staff)
            #Occasionally stack 2 notes
            doubleStop = random.choices(('True', 'False'), (10, 90))
            if doubleStop == ['True']:
                randomNote(staff)
            #Occasionally stack 3 notes
            tripleStop = random.choices(('True', 'False'), (5, 95))
            if tripleStop == ['True']:
                randomNote(staff)
                randomNote(staff)
    
    #Probability to change velocity
    if (elapsedTime % 0.2) <= 0.001 and speedTrigger is True: #Speed up
        speedTrigger = False
        speedChangeType = 'Fast'
        speedUpThread = threading.Thread(target=speedUp)
        resetSpeedFastThread = threading.Thread(target=resetSpeedFast)
        speedUpThread.start(), resetSpeedFastThread.start()
    
    roundedTime = round(elapsedTime, 1)
    #Events to be potentially performed every half second
    if roundedTime % 0.5 == 0 and saveTime != roundedTime:
        saveTime = roundedTime

        #Change the background color
        if random.choices(('True', 'False'), (2, 98)) == ['True']: #2%
            if boundingRectColor == "FFFFFF":
                changeBackgroundColor()

        #Change the modifier type
        if random.choices(('True', 'False'), (2, 98)) == ['True']: #2%
            if modifierPath.pen != Pen("000000", Unit(1)):
                changeModifier()
        
        #Generate graphics screen
        if random.choices(('True', 'False'), (3, 97)) == ['True'] and speedTrigger is True: #2%
            randomDuration = random.uniform(3.5, 6.5)
            graphicsType = random.choices(('Active', 'Minimal'), (50, 50))
            #If the graphics generated are minimal, there is a 50% to increase the time it stays onscreen
            if graphicsType == ['Minimal']:
                if bool(random.getrandbits(1)):
                    randomDuration += random.uniform(3.0, 6.0)

            #Call functions to generate the graphics screen
            drawings.compositeShape((neoscore.get_viewport_center_pos().x+Mm(30), Mm(-30)), staff, viewScale, randomDuration, graphicsType)
            
            #Stops scrolling screen for as long as the graphics are onscreen
            stopScrollThread = threading.Thread(target=stopScroll)
            resetSpeedRandThread = threading.Thread(target=resetSpeedRand, args=(randomDuration,))
            stopScrollThread.start(), resetSpeedRandThread.start()

        #Slow down scroll
        if random.choices(('True', 'False'), (5, 95)) == ['True'] and speedTrigger is True: #5%
            speedTrigger = False
            speedChangeType = 'Slow'
            slowDownThread = threading.Thread(target=slowDown)
            resetSpeedRandThread = threading.Thread(target=resetSpeedRand, args=(random.uniform(2.0, 5.0),))
            slowDownThread.start(), resetSpeedRandThread.start()

    #Performs all the same calculations for events but for staff 2
    if checkpointNumber >= 5:
        scroll_ypos = window_center_y+Mm(12)
        staff2._length = Mm(30) + Mm(scroll_xpos)
        if speedTrigger is False and speedChangeType == 'Fast':
            noteDensity = 100.0
        elif speedTrigger is False and speedChangeType == 'Slow':
            noteDensity = 0.005
        else:
            noteDensity = ((max - min) * sinLFO + max + min) / 2

        #Probability to spawn a note
        if (minimumNoteDistance) > staff2.unit(2) and generateNotes:
            if (elapsedTime % 0.3) <= noteDensity:
                randomNote(staff2)
                doubleStop = random.choices(('True', 'False'), (10, 90)) #Occasionally stack 2 notes
                if doubleStop == ['True']:
                    randomNote(staff2)
                tripleStop = random.choices(('True', 'False'), (5, 95))
                if tripleStop == ['True']:
                    randomNote(staff2)
                    randomNote(staff2)
        
        #Probability to change velocity
        if (elapsedTime % 0.2) <= 0.001 and speedTrigger is True: #Speed up
            speedTrigger = False
            speedChangeType = 'Fast'
            speedUpThread = threading.Thread(target=speedUp)
            resetSpeedFastThread = threading.Thread(target=resetSpeedFast)
            speedUpThread.start(), resetSpeedFastThread.start()
        
        if random.choices(('True', 'False'), (5, 95)) == ['True'] and speedTrigger is True: #Slow down
            speedTrigger = False
            speedChangeType = 'Slow'
            slowDownThread = threading.Thread(target=slowDown)
            resetSpeedRandThread = threading.Thread(target=resetSpeedRand, args=(random.uniform(2.0, 5.0),))
            slowDownThread.start(), resetSpeedRandThread.start()


    #Checkpoint event changes
    if elapsedTime >= checkpoint1 and checkpointNumber == 0:
        setAccidental()
        checkpointNumber = 1
    if elapsedTime >= checkpoint2 and checkpointNumber == 1:
        accidentalNotes.clear()
        setAccidental()
        checkpointNumber = 2
    if elapsedTime >= checkpoint3 and checkpointNumber == 2:
        setAccidental()
        checkpointNumber = 3
    if elapsedTime >= checkpoint4 and checkpointNumber == 3:
        setAccidental()
        setAccidental()
        checkpointNumber = 4
    if elapsedTime >= checkpoint5 and checkpointNumber == 4:
        setAccidental()
        setAccidental()
        newStaff()
        checkpointNumber = 5
    if elapsedTime >= checkpoint6 and checkpointNumber == 5:
        setAccidental()
        setAccidental()
        checkpointNumber = 6
    if elapsedTime >= checkpoint7 and checkpointNumber == 6:
        blackScreen = Path.rect((Mm(scroll_xpos-100), scroll_ypos-Mm(100)), staff, Mm(1000), Mm(1000), Color(0, 0, 0, fadeout))
        checkpointNumber = 7
    if elapsedTime >= checkpoint7:
        ending()


def ending():
    global fadeout
    stopScroll()
    if round(elapsedTime, 2) % 0.01 <= 0.1:
        if fadeout < 252:
            fadeout += 1
        if fadeout >= 252:
            fadeout = 255
    blackScreen.brush = Color(0,0,0,fadeout)

neoscore.show(display_page_geometry=False, fullscreen=True, auto_viewport_interaction_enabled=False)