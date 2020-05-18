class MemoryMap:
   def __init__(self, varsCount):
     self.ints = [None] * int(varsCount[0])
     self.floats = [None] * int(varsCount[1])
     self.chars = [None] * int(varsCount[2])
     self.bools = [None] * int(varsCount[3])
