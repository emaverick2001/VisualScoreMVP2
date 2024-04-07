from neoscore.core import neoscore
from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm
from neoscore.core.path import Path
from neoscore.core.brush import Brush
from neoscore.core.pen import Pen
from neoscore.core.pen import PenPattern
from neoscore.core.units import ZERO
from neoscore.core.text import Text

neoscore.setup() # This is required to initialize the NeoScore environment

# Brushes
# parameters: color, pattern

brush = Brush("#ffff0099")
path1 = Path.rect(ORIGIN, None, Mm(20), Mm(20), brush)

# Pens
# parameters: color, thickness, line pattern, join style, cap style

pens = [
    Pen(thickness=Mm(0.5), pattern=PenPattern.SOLID),
    Pen(thickness=Mm(0.5), pattern=PenPattern.DASH),
    Pen(thickness=Mm(0.5), pattern=PenPattern.DOT),
    Pen(thickness=Mm(0.5), pattern=PenPattern.DASHDOT),
    Pen(thickness=Mm(0.5), pattern=PenPattern.DASHDOTDOT),
]

for i, pen in enumerate(pens):
    Path.straight_line((Mm(25), Mm(10 * i)), None, (Mm(40), ZERO), pen=pen)

# more
Path.rect((Mm(0),Mm(30)), None, Mm(20), Mm(10), Brush.no_brush())
Text((Mm(0), Mm(45)), None, "Outline", brush=Brush.no_brush(), pen="#000000")



# Colors
Path.rect((Mm(0),Mm(55)), None, Mm(20), Mm(10), "#ffff0099", "ff00ff")


neoscore.show()