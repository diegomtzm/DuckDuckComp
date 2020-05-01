from structs import *
from semantics import *
from memoriaVirtual import *

pilaOperadores = Stack()
pilaSaltos = Stack()
pilaVariables = Stack()
pilaTipos = Stack()

cuadruplos = []
quadCount = 0

class Quadruple:
  def __init__(self, operator, leftOp, rightOp, res):
    self.op = operator
    self.leftOp = leftOp
    self.rightOp = rightOp
    self.res = res

  def get(self):
    quad = [self.op, self.leftOp, self.rightOp, self.res]
    return quad

def generateQuad(currFunc):
    rightOp = pilaVariables.pop()
    rightType = pilaTipos.pop()
    leftOp = pilaVariables.pop()
    leftType = pilaTipos.pop()
    oper = pilaOperadores.pop()
    result_type = Semantics().get_type(leftType, rightType, oper)
    if(result_type != 'ERROR'):
        global quadCount
        global cuadruplos

        if currFunc == "global":
            scope = 'globalTemp'
        else:
            scope = 'localTemp'

        dirVTemp = getNewDirV(result_type, scope)
        codigoOper = tablaOperadores[oper]

        quad = Quadruple(codigoOper, leftOp, rightOp, dirVTemp)
        cuadruplos.append(quad.get())
        pilaVariables.push(dirVTemp)
        pilaTipos.push(result_type)
        quadCount += 1
    else:
        print("Error: Type mismatch")

def generateAssigmentQuad():
  res = pilaVariables.pop()
  resType = pilaTipos.pop()
  var = pilaVariables.pop()
  varType = pilaTipos.pop()
  oper = pilaOperadores.pop()
  result_type = Semantics().get_type(resType, varType, oper)
  if(result_type != 'ERROR'):
      global quadCount
      codigoOper = tablaOperadores[oper]
      quad = Quadruple(codigoOper, res, None, var)
      cuadruplos.append(quad.get())
      quadCount += 1
  else:
      print("Error: Type mismatch")

  


