from neoscore.core.units import Mm, Unit
from neoscore.core.point import ORIGIN
from neoscore.core.color import Color
from neoscore.core.pen import Pen, PenPattern
from neoscore.core.path import Path
from neoscore.core.text import Text, Font
from neoscore.core.brush import Brush
import time as tm
import random
import threading

blueSat = Color(59,136,204)
greenSat = Color(47,224,80)
yellowSat = Color(247,222,40)
orangeSat = Color(230,121,67)
purpleSat = Color(182,38,237)

colorsSat = [blueSat, greenSat, yellowSat, orangeSat, purpleSat]

def compositeShape(start, par, viewScale, duration, graphicsType):
    global shapeNumber, widthList, valueList, startPoint, parent, scale
    shapeNumber = random.randint(1,8)

    startPoint = start
    parent = par
    scale = viewScale/2

    if graphicsType == ['Active']:
        backgroundFrame(duration)
        generateCloud(random.randint(500, 800), duration)
        randomShapes(random.randint(10, 40), duration)
        textPrint(duration)
    else:
        backgroundFrame(duration)
        randomShapes(random.randint(1, 2), duration)
        textPrint(duration)

def backgroundFrame(duration):
    global startPoint, parent
    frame = Path(startPoint, parent, random.choice(colorsSat))
    frame.rect((Mm(-120), Mm(-40)), frame, Mm(200), Mm(150), random.choice(colorsSat))
    threading.Thread(target=deleteSelf, args=(frame, duration)).start()

def deleteSelf(self, duration):
    tm.sleep(duration)
    self.remove()
    

words = "shimmering caution grotesque humanity aspirations gods lustrous time space orb qualities language thoughts inhabitants combinations countless moons enclose virtue sin visible ownership pleasure himself herself being aspirations lacking earth believe belief perfect harmony chaos howling questions recurring life faith faithless vain craving empty years intertwined amid idle wondrous fear fearful laughing poor rich months death whistling cacophony midnight lonesome soul listen clusters sorrow sorrowful eerie rapture rapturous"

def textPrint(duration): #Scramble string and print a random number of words from it
    global words, startPoint, parent
    wordNumber = random.randint(1, 5)
    stringReplace = words.replace(",", "").replace(".", "").replace("?", "").replace("!", "")
    stringLower = stringReplace.lower()
    listSplit = stringLower.split()
    random.shuffle(listSplit)
    scrambledText = listSplit[slice(wordNumber)]
    scrambledText = " ".join(scrambledText)

    font = Font("Times New Roman", Unit(random.randint(16, 72)), random.randint(25, 75))
    if random.choices(['Print', 'noPrint'], [70, 30]) == ['Print']:
        self = Text((startPoint[0]-Mm(random.uniform(20.0, 40.0)), Mm(random.uniform(-10.0, 10.0))), parent, scrambledText, font, random.choice(colorsSat), Pen("000000", Unit(0.5)), rotation=random.randint(0, 360))
        duration -= 1.0
        threading.Thread(target=deleteSelf, args=(self, duration)).start()

def generateCloud(num_elements, duration, otherParent=False):
    global startPoint, parent
    #Pen randomization options
    penThickness = random.uniform(0.25, 1.25)
    penPattern = random.choice([PenPattern.SOLID, PenPattern.DASH, PenPattern.DOT, PenPattern.DASHDOT, PenPattern.DASHDOTDOT])
    
    duration -= 1.0

    if not otherParent:
        for _ in range(num_elements):
            x = Unit(random.uniform(-250, 50))
            y = Unit(random.uniform(0, 200))

            line = Path((startPoint[0]+x, startPoint[1]+y), parent, pen=Pen((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), Unit(penThickness), penPattern))
            line.line_to(Unit(random.uniform(-6,6)), Unit(random.uniform(-6,6)), line)

            threading.Thread(target=deleteSelf, args=(line, duration)).start()
    else:
        for _ in range(num_elements):
            x = Unit(random.uniform(-120, 150))
            y = Unit(random.uniform(-5, 160))

            line = Path((x, y), otherParent, pen=Pen((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), Unit(penThickness), penPattern))
            line.line_to(Unit(random.uniform(-6,6)), Unit(random.uniform(-6,6)), line)

            threading.Thread(target=deleteSelf, args=(line, duration)).start()

def randomShapes(shape_num, duration):
    global startPoint, parent
    for _ in range(shape_num):
        x = Unit(random.uniform(-250, 50))
        y = Unit(random.uniform(0, 200))

        shape = Path((startPoint[0]+x, startPoint[1]+y), parent, rotation=random.randint(0,360))
        shape.rect(ORIGIN, shape, Unit(random.uniform(1, 100)), Unit(random.uniform(1, 100)), brush=Brush((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))))

        threading.Thread(target=deleteSelf, args=(shape, duration)).start()
