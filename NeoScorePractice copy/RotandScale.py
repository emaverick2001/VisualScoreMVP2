from neoscore.common import *
neoscore.setup()

# Transformations
# Text(ORIGIN, None, "Hello, neoscore!", rotation= 45, scale= 2.0)

# more properties
# children objects will inherit the properties of their parent
parent = Text((Mm(0),Mm(100)), None, "parent", rotation=-45, scale=1.2)
Text((Mm(20), Mm(10)), parent, "child")

# within flowables trandform properties are not inherited

# flowables are objects that can contain other objects
# this is useful for creating sheets of music, text, etc.
flowable = Flowable(ORIGIN, None, Mm(200), Mm(15))
parent = Text(ORIGIN, flowable, "parent", rotation=-45, scale=1.2)
Text((Mm(20), Mm(10)), parent, "child", rotation=10)

neoscore.show()