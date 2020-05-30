class MemoryMap:
  def __init__(self, varsCount):
    self.ints = [None] * int(varsCount[0])
    self.floats = [None] * int(varsCount[1])
    self.chars = [None] * int(varsCount[2])
    self.bools = [None] * int(varsCount[3])
    if len(varsCount) > 4:
      self.pointers = [None] * int(varsCount[4])
    else:
      self.pointers = [None] * 0

  def get(self):
    mem = [self.ints, self.floats, self.chars, self.bools, self.pointers]
    return mem
