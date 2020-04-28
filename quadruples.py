from structs import *

pilaOperadores = Stack()
pilaSaltos = Stack()
pilaVariables = Stack()
pilaTipos = Stack()

cuadruplos = []
quadCount = 0

ops = {
  "+": (lambda x,y: x+y), 
  "-": (lambda x,y: x-y),
  "*": (lambda x,y: x*y),
  "/": (lambda x,y: x/y)
}

class Quadruple:
  def __init__(self, operator, leftOp, rightOp, res):
    self.op = operator
    self.leftOp = leftOp
    self.rightOp = rightOp
    self.res = res

  def get(self):
    quad = [self.op, self.leftOp, self.rightOp, self.res]
    return quad

  


