from neoscore.core import neoscore
from neoscore.core.text import Text
from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm
from neoscore.core.units import ZERO
from neoscore.core.units import Unit

from neoscore.core.font import Font

from neoscore.core.units import Inch

from neoscore.core.rich_text import RichText

neoscore.setup()

# Text
# parameters: position (specified by a tuple), parent (can be None), text

# text_1 is given parent None, implicitly the first page,
# and positioned at the page origin (0, 0)
text_1 = Text((Mm(0), Mm(3)), None, "text 1")

# text_2 is given text_1 as its parent, so its position is relative to text_1
text_2 = Text((Mm(0), Mm(10)), None, "text 2")

# text_3 is given text_2 as its parent, so its positition is relative to text_2
# Notice how text_3's position includes a negative Y value, meaning it is
# positioned above its parent.
text_3 = Text((Mm(0), Mm(10)), text_2, "text 3")
Lorem_text = Text((Mm(10),Mm(-10)), text_1, "Lorem ipsum")

# Fonts
# Default font is 12pt Lora

default = neoscore.default_font # Alias just for docs legibility
sample = "The quick brown fox jumps over the lazy dog"
font_text = Text((ZERO, Mm(10)), text_3, sample, default.modified(size=Unit(14), weight=100, italic=True))


# Custom fonts
font = Font("Arial", Unit(18)) # Using default weight and italics values
custom_font_text = Text((ZERO,Mm(10)), font_text , "Text in another font family", font)

# registering custom font
# you can register fonts from TrueType and OpenType files

# neoscore.register_font('path/to/Arial.ttf')

# Rich text
# parameters: position, parent, html (text want to pass), width, font

html = """
<p align=right>
  another paragraph aligned right
  and <span style="color: red">with inline coloring</span>!
</p>
"""

default_font = neoscore.default_font.modified(weight=80, italic=True)

RichText((ZERO, Mm(10)), custom_font_text, html, Inch(4),default_font)

neoscore.show()