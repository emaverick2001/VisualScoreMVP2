from neoscore.core import neoscore
from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm
from neoscore.core.path import Path
from neoscore.core.text import Text
from neoscore.core.units import ZERO

neoscore.setup() # This is required to initialize the NeoScore environment

# Paths
# parameters: position, parent, color

path = Path(ORIGIN, None, "#ff00ff55")
# draws a line from the current point to the specified point which then becomes part of the path
path.line_to(Mm(10), Mm(-10))
path.line_to(Mm(20), Mm(0))
path.line_to(Mm(30), Mm(-10))
# draws a cubic bezier curve from the current point to the specified point which then becomes part of the path
path.cubic_to(Mm(40), Mm(-10), Mm(40), Mm(10), Mm(30), Mm(10))
path.close_subpath()

text = Text((Mm(50), Mm(0)), None, "Path 1")
path2 = Path((Mm(40), Mm(10)), path , "#0000ff55")
# draws a line from the current point (start of path2) to the specified point which then becomes part of the path
path2.line_to(Mm(10), Mm(1),text)
path2.line_to(Mm(10), Mm(10),text)
path2.close_subpath()

neoscore.show()