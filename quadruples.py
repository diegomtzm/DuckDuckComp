from structs import *
from semantics import *
from memoriaVirtual import *

pilaOperadores = Stack()
pilaSaltos = Stack()
pilaVariables = Stack()
pilaTipos = Stack()
pilaDimensions = Stack()

cuadruplos = []
quadCount = 0
iTempCount = 0
fTempCount = 0
cTempCount = 0
bTempCount = 0
pTempCount = 0
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

def generateQuad(currFunc, pointer=False, size=1):
    rightOp = pilaVariables.pop()
    rightType = pilaTipos.pop()
    leftOp = pilaVariables.pop()
    leftType = pilaTipos.pop()
    oper = pilaOperadores.pop()
    result_type = Semantics().get_type(leftType, rightType, oper)
    if(result_type != 'ERROR'):
        global quadCount
        global iTempCount
        global fTempCount
        global cTempCount
        global bTempCount
        global pTempCount
        global cuadruplos

        if currFunc == "global":
            scope = 'globalTemp'
        else:
            scope = 'localTemp'

        if pointer:
            dirVTemp = getNewDirV('pointer', scope)
            pTempCount += 1
        else:
            dirVTemp = getNewDirV(result_type, scope)
        codigoOper = tablaOperadores[oper]

        if size > 1:
            dirVTemp = (dirVTemp, size)
            pilaVariables.push(dirVTemp[0])
        else:
            pilaVariables.push(dirVTemp)

        quad = Quadruple(codigoOper, leftOp, rightOp, dirVTemp)
        cuadruplos.append(quad)
        pilaTipos.push(result_type)
        if result_type == 'int':
            iTempCount += 1
        elif result_type == 'float':
            fTempCount += 1
        elif result_type == 'char':
            cTempCount += 1
        elif result_type == 'bool':
            bTempCount += 1
        quadCount += 1
    else:
        raise TypeError(f'Cannot apply {oper} to {leftType} and {rightType}')

def generateAssigmentQuad(size=1):
    res = pilaVariables.pop()
    resType = pilaTipos.pop()
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    oper = pilaOperadores.pop()
    result_type = Semantics().get_type(varType, resType, oper)
    if(result_type != 'ERROR'):
        global quadCount
        codigoOper = tablaOperadores[oper]
        quad = Quadruple(codigoOper, res, size, var)
        cuadruplos.append(quad)
        quadCount += 1
        pilaVariables.push(var)
        pilaTipos.push(varType)
    else:
        raise TypeError(f'Cannot apply {oper} to {varType} and {resType}')

def generateDecisionQuad():
    global quadCount
    res = pilaVariables.pop()
    tipo = pilaTipos.pop()
    codigoOp = tablaOperadores['goToF']
    quad = Quadruple(codigoOp, res, None, "")
    cuadruplos.append(quad)
    quadCount += 1
    pilaSaltos.push(quadCount - 1)
    
def generateSinoQuad():
    global quadCount
    codigoOp = tablaOperadores['goTo']
    quad = Quadruple(codigoOp, None, None, "")
    cuadruplos.append(quad)
    quadCount += 1
    numQuad = pilaSaltos.pop()
    pilaSaltos.push(quadCount - 1)
    rellenarQuad(numQuad)

def generateGoToQuad(returnJump):
    global quadCount
    codigoOp = tablaOperadores['goTo']
    quad = Quadruple(codigoOp, None, None, returnJump)
    cuadruplos.append(quad)
    quadCount += 1

def rellenarQuad(numQuad):
    global quadCount
    cuad = cuadruplos[numQuad]
    cuad.res = quadCount
    cuadruplos[numQuad] = cuad

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
        global iTempCount
        global fTempCount
        global cTempCount
        global bTempCount
        global cuadruplos

        if currFunc == "global":
            scope = 'globalTemp'
        else:
            scope = 'localTemp'

        dirVTemp = getNewDirV(result_type, scope)
        codigoOper = tablaOperadores['<=']
        quad = Quadruple(codigoOper, var, res, dirVTemp)
        cuadruplos.append(quad)
        pilaVariables.push(var)
        pilaTipos.push(varType)
        pilaVariables.push(dirVTemp)
        pilaTipos.push(result_type)
        if result_type == 'int':
            iTempCount += 1
        elif result_type == 'float':
            fTempCount += 1
        elif result_type == 'char':
            cTempCount += 1
        elif result_type == 'bool':
            bTempCount += 1
        quadCount += 1
    else:
        raise TypeError(f'Cannot apply <= to {varType} and {resType}')

def generateDesdeFinQuad(currFunc, right, rightType):
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    result_type = Semantics().get_type(varType, rightType, "+")
    if(result_type != 'ERROR'):
        global quadCount
        global iTempCount
        global cuadruplos

        if currFunc == "global":
            scope = 'globalTemp'
        else:
            scope = 'localTemp'

        dirVTemp = getNewDirV(result_type, scope)
        codigoOper = tablaOperadores['+']
        
        quad = Quadruple(codigoOper, var, right, dirVTemp)
        cuadruplos.append(quad)
        quadCount += 1

        codigoOper = tablaOperadores['=']
        quad2 = Quadruple(codigoOper, dirVTemp, 1, var)
        cuadruplos.append(quad2)
        iTempCount += 1
        quadCount += 1
    else:
        raise TypeError(f'Cannot apply + to {varType} and {rightType}')

def generateLeeVariableQuad(varDir):
    global quadCount
    codigoOp = tablaOperadores['lee']
    quad = Quadruple(codigoOp, None, None, varDir)
    cuadruplos.append(quad)
    quadCount += 1

def generateSalidaQuad():
    global quadCount
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    codigoOp = tablaOperadores['escribe']
    quad = Quadruple(codigoOp, None, None, var)
    cuadruplos.append(quad)
    quadCount += 1

def generateRetornoExp():
    global quadCount
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    codigoOp = tablaOperadores['regresa']
    quad = Quadruple(codigoOp, None, None, var)
    cuadruplos.append(quad)
    quadCount += 1

def generateEndFuncQuad():
    global quadCount
    codigoOp = tablaOperadores['endFunc']
    quad = Quadruple(codigoOp, None, None, None)
    cuadruplos.append(quad)
    quadCount += 1

def generateEndQuad():
    global quadCount
    codigoOp = tablaOperadores['end']
    quad = Quadruple(codigoOp, None, None, None)
    cuadruplos.append(quad)
    quadCount += 1

def generateERAQuad(funcName, params):
    global quadCount
    global paramCount
    global currParams
    global currFuncCall
    codigoOp = tablaOperadores['era']
    quad = Quadruple(codigoOp, funcName, None, None)
    cuadruplos.append(quad)
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
            cuadruplos.append(quad)
            quadCount += 1
            paramCount += 1
        else:
            raise TypeError(f'Expected {currParams[paramCount]} and received {varType[0]}')
    else:
        raise Exception(f'Expected {paramCount} params and received {len(currParams)+1}')

def generateGoSubQuad(initAddress):
    global quadCount
    global paramCount
    if paramCount == len(currParams):
        codigoOp = tablaOperadores['goSub']
        quad = Quadruple(codigoOp, currFuncCall, None, initAddress)
        cuadruplos.append(quad)
        quadCount += 1
    else:
        raise Exception(f'Expected {len(currParams)} params and received {paramCount}')

def generateFuncAssignmentQuad(dirV, result_type, currFunc):
    global quadCount
    global cuadruplos
    global iTempCount
    global fTempCount
    global cTempCount
    global bTempCount
    if currFunc == 'global':
        scope = 'globalTemp'
    else:
        scope = 'localTemp'
    dirVTemp = getNewDirV(result_type, scope)
    codigoOp = tablaOperadores['=']
    quad = Quadruple(codigoOp, dirV, 1, dirVTemp)
    cuadruplos.append(quad)
    quadCount += 1
    pilaVariables.push(dirVTemp)
    pilaTipos.push(result_type)
    if result_type == 'int':
        iTempCount += 1
    elif result_type == 'float':
        fTempCount += 1
    elif result_type == 'char':
        cTempCount += 1
    elif result_type == 'bool':
        bTempCount += 1

def generateVerQuad(lim):
    global quadCount
    global cuadruplos
    dirDim = pilaVariables.top()
    codigoOp = tablaOperadores['ver']
    quad = Quadruple(codigoOp, dirDim, None, lim)
    cuadruplos.append(quad)
    quadCount += 1

    
def getCurrentQuadCount():
    global quadCount
    return quadCount

def getTempCount():
    global iTempCount
    global fTempCount
    global cTempCount
    global bTempCount
    global pTempCount
    tempCount = [iTempCount, fTempCount, cTempCount, bTempCount, pTempCount]
    return tempCount

def resetTempCount():
    global iTempCount
    global fTempCount
    global cTempCount
    global bTempCount
    global pTempCount
    iTempCount, fTempCount, cTempCount, bTempCount, pTempCount = 0, 0, 0, 0, 0
