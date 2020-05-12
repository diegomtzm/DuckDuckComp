from structs import *
from semantics import *
from memoriaVirtual import *

pilaOperadores = Stack()
pilaSaltos = Stack()
pilaVariables = Stack()
pilaTipos = Stack()

cuadruplos = []
quadCount = 0
tempCount = 0
paramCount = 0
currParams = []
currFuncCall = ''

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
        global tempCount
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
        tempCount += 1
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
        pilaVariables.push(var)
        pilaTipos.push(varType)
    else:
        print("Error: Type mismatch")

def generateDecisionQuad():
    global quadCount
    res = pilaVariables.pop()
    tipo = pilaTipos.pop()
    codigoOp = tablaOperadores['goToF']
    quad = Quadruple(codigoOp, res, None, "")
    cuadruplos.append(quad.get())
    quadCount += 1
    pilaSaltos.push(quadCount - 1)
    
def generateSinoQuad():
    global quadCount
    codigoOp = tablaOperadores['goTo']
    quad = Quadruple(codigoOp, None, None, "")
    cuadruplos.append(quad.get())
    quadCount += 1
    numQuad = pilaSaltos.pop()
    pilaSaltos.push(quadCount - 1)
    rellenarQuad(numQuad)

def generateGoToQuad(returnJump):
    global quadCount
    codigoOp = tablaOperadores['goTo']
    quad = Quadruple(codigoOp, None, None, returnJump)
    cuadruplos.append(quad.get())
    quadCount += 1

def rellenarQuad(numQuad):
    global quadCount
    cuadruplos[numQuad][3] = quadCount

def pushJump(n=0):
    global quadCount
    pilaSaltos.push(quadCount+n)

def generateDesdeQuad(currFunc):
    res = pilaVariables.pop()
    resType = pilaTipos.pop()
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    result_type = Semantics().get_type(varType, resType, "<=")
    
    if(result_type != 'ERROR'):
        global quadCount
        global tempCount
        global cuadruplos

        if currFunc == "global":
            scope = 'globalTemp'
        else:
            scope = 'localTemp'

        dirVTemp = getNewDirV(result_type, scope)
        codigoOper = tablaOperadores['<=']
        quad = Quadruple(codigoOper, var, res, dirVTemp)
        cuadruplos.append(quad.get())
        pilaVariables.push(var)
        pilaTipos.push(varType)
        pilaVariables.push(dirVTemp)
        pilaTipos.push(result_type)
        tempCount += 1
        quadCount += 1
    else:
        print("Error: Type mismatch")

def generateDesdeFinQuad(currFunc, right, rightType):
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    result_type = Semantics().get_type(varType, rightType, "+")
    if(result_type != 'ERROR'):
        global quadCount
        global tempCount
        global cuadruplos

        if currFunc == "global":
            scope = 'globalTemp'
        else:
            scope = 'localTemp'

        dirVTemp = getNewDirV(result_type, scope)
        codigoOper = tablaOperadores['+']
        
        quad = Quadruple(codigoOper, var, right, dirVTemp)
        cuadruplos.append(quad.get())
        quadCount += 1

        codigoOper = tablaOperadores['=']
        quad2 = Quadruple(codigoOper, dirVTemp, None, var)
        cuadruplos.append(quad2.get())
        tempCount += 1
        quadCount += 1
    else:
        print("Error: Type mismatch")

def generateLeeVariableQuad(varDir):
    global quadCount
    codigoOp = tablaOperadores['lee']
    quad = Quadruple(codigoOp, None, None, varDir)
    cuadruplos.append(quad.get())
    quadCount += 1

def generateSalidaQuad():
    global quadCount
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    codigoOp = tablaOperadores['escribe']
    quad = Quadruple(codigoOp, None, None, var)
    cuadruplos.append(quad.get())
    quadCount += 1

def generateRetornoExp():
    global quadCount
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    codigoOp = tablaOperadores['regresa']
    quad = Quadruple(codigoOp, None, None, var)
    cuadruplos.append(quad.get())
    quadCount += 1

def generateEndFuncQuad():
    global quadCount
    codigoOp = tablaOperadores['endFunc']
    quad = Quadruple(codigoOp, None, None, None)
    cuadruplos.append(quad.get())
    quadCount += 1

def generateEndQuad():
    global quadCount
    codigoOp = tablaOperadores['end']
    quad = Quadruple(codigoOp, None, None, None)
    cuadruplos.append(quad.get())
    quadCount += 1

def generateERAQuad(funcName, params):
    global quadCount
    global paramCount
    global currParams
    global currFuncCall
    codigoOp = tablaOperadores['era']
    quad = Quadruple(codigoOp, funcName, None, None)
    cuadruplos.append(quad.get())
    quadCount += 1
    currParams = params
    paramCount = 0
    currFuncCall = funcName

def generateParamQuad():
    global quadCount
    global paramCount
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    if paramCount < len(currParams):
        if varType[0] == currParams[paramCount]:
            codigoOp = tablaOperadores['param']
            quad = Quadruple(codigoOp, var, paramCount, None)
            cuadruplos.append(quad.get())
            quadCount += 1
            paramCount += 1
        else:
            print('Error: param type mismatch')
    else:
        print('Error: param count mismatch')

def generateGoSubQuad(initAddress):
    global quadCount
    global paramCount
    if paramCount == len(currParams):
        codigoOp = tablaOperadores['goSub']
        quad = Quadruple(codigoOp, currFuncCall, None, initAddress)
        cuadruplos.append(quad.get())
        quadCount += 1
    else:
        print('Error: number of params mismatch')
        

def getCurrentQuadCount():
    global quadCount
    return quadCount

def getTempCount():
    global tempCount
    return tempCount

def resetTempCount():
    global tempCount
    tempCount = 0
