from neoscore.common import *
from neoscore.core.paper import LETTER

neoscore.setup(LETTER)


length = Mm(800)

flowable = Flowable(ORIGIN, None, length, Mm(30))
staff = Staff(ORIGIN, flowable, length)

clef = Clef(ZERO, staff, 'treble')

note1 = Chordrest(Mm(10), staff, ["f", "b"], (1,4)) #10
note2 = Chordrest(Mm(20), staff, ["c'"], (3,4)) #20
note3 = Chordrest(Mm(80), staff, ["eb'"], (1,8)) #40
note4 = Chordrest(Mm(95), staff, ["f#"], (1,16)) #50
note5 = Chordrest(Mm(105), staff, ["g"], (1,16)) #55
note6 = Chordrest(Mm(175), staff, ["ab'"], (1,8)) #80
note7 = Chordrest(Mm(250), staff, ["db''"], (2,4)) #90
note8 = Chordrest(Mm(280), staff, ["f'", "gb"], (4,4)) #100

#Need to find a way to have both a starting and ending parent to scale length naturally
box_length = Mm(110)
box_height = Mm(20)
box = Path((-Mm(5), -Mm(7)), note3)
box.rect((-Mm(5), -Mm(7)), note3, box_length, box_height, Brush(pattern=BrushPattern.INVISIBLE), Pen(thickness=Unit(2)))
#Probably need to make a version of .rect that uses starting and ending position (and starting and ending parents) rather than width and height

box2 = Path((-Mm(5), -Mm(10)), note7)
box2.rect((-Mm(5), -Mm(10)), note7, Mm(50), Mm(25), Brush(pattern=BrushPattern.INVISIBLE), Pen(thickness=Unit(2)))

#How to make y_pos centered on staff?
arrow = Path((box_length, box_height/2), box)
arrow.arrow((box_length, box_height/2), box, (-Mm(1), Mm(13)), box2, pen=Pen(thickness=Unit(2)), arrow_head_width=Unit(7))


neoscore.show()