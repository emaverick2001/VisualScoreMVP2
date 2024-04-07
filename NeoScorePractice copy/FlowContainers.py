from neoscore.common import *
from neoscore.core.break_opportunity import BreakOpportunity

neoscore.setup() # This is required to initialize the NeoScore environment

# Flow Containers
# parameters: position, parent, width, height
# flow = Flowable(ORIGIN, None, Mm(500), Mm(5))
# Text(ORIGIN, flow, "text on first line")
# Text((Mm(200), ZERO), flow, "text on second line")
# Text((Mm(300), ZERO), flow, "text spanning line break")

# Break Opportunities
class BreakHintText(Text, BreakOpportunity):
    pass

flow = Flowable(ORIGIN, None, Mm(500), Mm(15), break_threshold=Mm(50))
paper = neoscore.document.pages[0].paper
# Outline the flowable for visualization
Path.rect(ORIGIN, flow, Mm(500), Mm(15), brush=Brush.no_brush())
# And draw a line over the break threshold
Path.straight_line((paper.live_width - Mm(50), ZERO), None, (ZERO, Mm(75)),
    pen=Pen("#ff0000", pattern=PenPattern.DASH))
BreakHintText((Mm(100), Mm(8)), flow, "opp 1")
BreakHintText((Mm(200), Mm(8)), flow, "opp 2")
BreakHintText((Mm(300), Mm(8)), flow, "opp 3")
BreakHintText((Mm(430), Mm(6)), flow, "opp 4")
BreakHintText((Mm(440), Mm(12)), flow, "opp 5")

#Dynamic margins


neoscore.show()