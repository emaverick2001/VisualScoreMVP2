from neoscore.common import *
import pathlib

neoscore.setup() # This is required to initialize the NeoScore environment

# Just a black rectangle here, but this can be anything.
# These paths are relative to the docs build dir, if you want to try this out
# yourself you'll need to provide your own images
file_path = pathlib.Path("..") / "tests" / "resources" / "pixmap_image.png"
Image(ORIGIN, None, file_path)

file_path2 = pathlib.Path("..") / "tests" / "resources" / "svg_image.svg"
Image(ORIGIN, None, file_path2, scale=1.2)


neoscore.show()