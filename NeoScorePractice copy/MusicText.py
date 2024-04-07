from neoscore.common import *

neoscore.setup() # This is required to initialize the NeoScore environment

font = MusicFont("Bravura", Mm(2))

# display a gClef from the SMuFL font library
mt = MusicText(ORIGIN, None, "gClef", font)


# display other musical symbols from the SMuFL font library
# MusicText((Mm(10),Mm(3)), None, "ornamentTurn", MusicFont("Bravura", Mm))
# MusicText((Mm(10),Mm(6)), None, "ornamentTurn", MusicFont("Bravura", Mm(1)))
# MusicText((Mm(10), Mm(9)), None, "ornamentTurn", MusicFont("Bravura", Mm(2)))
# MusicText((Mm(10), Mm(12)), None, "noteheadBlack", MusicFont("Bravura", Mm(2)))

# display a fClef, cClef, and a whole note from the SMuFL font library
# Path.straight_line(ORIGIN, None, (Mm(30), ZERO))
# MusicText(ORIGIN, None, "gClef", font)
# MusicText((Mm(8), ZERO), None, "fClef", font)
# MusicText((Mm(16), ZERO), None, "cClef", font)
# MusicText((Mm(24), ZERO), None, "noteheadWhole", font)

# displaying list of all available SMuFL symbols
# font = MusicFont("Bravura", Mm(2))
# MusicText(ORIGIN, None,
#     ["noteheadBlack", "noteheadHalf", "noteheadWhole"], font)

# displaying tuple list of all available SMuFL symbols
# font = MusicFont("Bravura", Mm(2))
# MusicText(ORIGIN, None, "flag16thUp", font)
# # straight-flagged alternate, aka "flag16thUpStraight"
# MusicText((Mm(4), ZERO), None, ("flag16thUp", 1), font)
# # short-flagged alternate, also accessible with the "flag16thUpShort" glyph name
# MusicText((Mm(8), ZERO), None, ("flag16thUp", 2), font)



neoscore.show()