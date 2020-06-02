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

# Generates a general quadruple with the specified current function
# size and whether it's a pointer or not.
# @param: currFunc, the current function
# @param: pointer, if it's a pointer or not
# @param: size, dimension of the variable 
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
        # Count of temporal variable types
        if result_type == 'int':
            iTempCount += size
        elif result_type == 'float':
            fTempCount += size
        elif result_type == 'char':
            cTempCount += size
        elif result_type == 'bool':
            bTempCount += size
        quadCount += 1
    else:
        raise TypeError(f'Can`t apply {oper} to {leftType} and {rightType}')

# Generates quadruple for matrix multiplication
# @param: currFunc, the current function
# @param: leftDims, dimensions of left matrix
# @param: rightDims, dimensions of right matrix
def generateMatMulQuad(currFunc, leftDims, rightDims):
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

        dirVTemp = getNewDirV(result_type, scope)
        codigoOper = tablaOperadores[oper]

        leftArg = (leftOp, leftDims)
        rightArg = (rightOp, rightDims)

        quad = Quadruple(codigoOper, leftArg, rightArg, dirVTemp)
        cuadruplos.append(quad)
        quadCount += 1
        pilaVariables.push(dirVTemp)
        pilaTipos.push(result_type)

        size = leftDims[0] * rightDims[1]
        dirOffset(result_type, scope, size)
        if result_type == 'int':
            iTempCount += size
        elif result_type == 'float':
            fTempCount += size
    else:
        raise TypeError(f'Can`t apply {oper} to {leftType} and {rightType}')

# Generates quadruple for matrix operations
# @param: dims, dimensions of the resulting matrix
# @param: currFunc, the current function
def generateOpMatQuad(dims, currFunc):
    global quadCount
    global cuadruplos
    global iTempCount
    global fTempCount
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    oper = pilaOperadores.pop()
    result_type = Semantics().get_type(varType, 'mat', oper)
    if result_type != 'ERROR':
        codigoOper = tablaOperadores[oper]
        if currFunc == "global":
            scope = 'globalTemp'
        else:
            scope = 'localTemp'
        dirVTemp = getNewDirV(result_type, scope)
        quad = Quadruple(codigoOper, var, dims, dirVTemp)
        cuadruplos.append(quad)
        quadCount += 1
        pilaVariables.push(dirVTemp)
        pilaTipos.push(result_type)
        if oper == '$':
            size = 1
        else:
            size = dims[0] * dims[1]
            dirOffset(result_type, scope, size)
        if result_type == 'int':
            iTempCount += size
        elif result_type == 'float':
            fTempCount += size
    else:
        raise TypeError(f'Can`t apply {oper} to {varType}')

# Generates ASSIGNMENT quadruple
# @param: size, size of the resul
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
        raise TypeError(f'Can`t apply {oper} to {varType} and {resType}')

# Generates GOTO quadruple
def generateDecisionQuad():
    global quadCount
    res = pilaVariables.pop()
    tipo = pilaTipos.pop()
    codigoOp = tablaOperadores['goToF']
    quad = Quadruple(codigoOp, res, None, "")
    cuadruplos.append(quad)
    quadCount += 1
    pilaSaltos.push(quadCount - 1)

# Generates GOTO quadruple for 'if else' statement
def generateSinoQuad():
    global quadCount
    codigoOp = tablaOperadores['goTo']
    quad = Quadruple(codigoOp, None, None, "")
    cuadruplos.append(quad)
    quadCount += 1
    numQuad = pilaSaltos.pop()
    pilaSaltos.push(quadCount - 1)
    rellenarQuad(numQuad)

# Generates GOTO quadruple
# @param: returnJump, the quadruple number to which the quadruple
# will jump to when called.
def generateGoToQuad(returnJump):
    global quadCount
    codigoOp = tablaOperadores['goTo']
    quad = Quadruple(codigoOp, None, None, returnJump)
    cuadruplos.append(quad)
    quadCount += 1

# Sets the res of GOTO quadruples to the current quadruple number
# @param: numQuad, the quadruple number to be modified
def rellenarQuad(numQuad):
    global quadCount
    cuad = cuadruplos[numQuad]
    cuad.res = quadCount
    cuadruplos[numQuad] = cuad

# Pushes current quadruple number to the jump pile
# @param: n, the offset to the quadruple number
def pushJump(n=0):
    global quadCount
    pilaSaltos.push(quadCount+n)

# Handles 'for loop' statement, compares the current variable
# with the defined limit in a 'smaller or equal than' way (<=)
# @param: currFunc, the current function
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

# Handles the 'for loop' statement, adds 1 to the current variable and
# assigns it.
# @param: currFunc, the current function
# @param: right, the constant's virtual memory address
# @param: rightType, the type of the constant variable
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

# Generates LEE quadruple
# @param: varDir, the virtual memory address of the variable to read
def generateLeeVariableQuad(varDir):
    global quadCount
    codigoOp = tablaOperadores['lee']
    quad = Quadruple(codigoOp, None, None, varDir)
    cuadruplos.append(quad)
    quadCount += 1

# Generates ESCRIBE quadruple, prints the variable's value in console
def generateSalidaQuad():
    global quadCount
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    codigoOp = tablaOperadores['escribe']
    quad = Quadruple(codigoOp, None, None, var)
    cuadruplos.append(quad)
    quadCount += 1

# Generates new line quadruple for ESCRIBE, gives the instruction to
# print a new line in console
def generateNewLineQuad():
    global quadCount
    codigoOp = tablaOperadores['escribe']
    quad = Quadruple(codigoOp, None, "nl", None)
    cuadruplos.append(quad)
    quadCount += 1

# Generates RETURN quadruple, gives the instruction to return and assign
# the value of the specified virtual memory address
# @param: currFuncVar, the current function variables
def generateRetornoExp(currFuncVar):
    global quadCount
    var = pilaVariables.pop()
    varType = pilaTipos.pop()
    codigoOp = tablaOperadores['regresa']
    quad = Quadruple(codigoOp, currFuncVar, None, var)
    cuadruplos.append(quad)
    quadCount += 1

# Generates END FUNC quadruple, specifies the end of the function
def generateEndFuncQuad():
    global quadCount
    codigoOp = tablaOperadores['endFunc']
    quad = Quadruple(codigoOp, None, None, None)
    cuadruplos.append(quad)
    quadCount += 1

# Generates END quadruple, specifies the end of the program
def generateEndQuad():
    global quadCount
    codigoOp = tablaOperadores['end']
    quad = Quadruple(codigoOp, None, None, None)
    cuadruplos.append(quad)
    quadCount += 1

# Generates ERA quadruple, calls for required virtual memory 
# for the specfied function to call
# @param: funcName, function name to call for memory
# @param: params, amount of parameters for the function 
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

# Generates PARAM quadruple, sends variable for parameter to 
# the specified function called and number of current parameter
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

# Generates GO SUB quadruple, sends current function called and the initial
# virtual memory address of the called function
# @param: initAddress, initial virtual memory address of the called function
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

# Generates FUNC ASSIGNMENT quadruple, assigns the called function return 
# value to a temporal variable
# @param: dirV, the virtual memory address from the called function
# @param: result_type, the type of the result
# @param: currFunc, the current function
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

# Generates VER quadruple, checks if the index from the dimensional 
# variable is within the limits of its dimensions
# @param: lim, limit of the dimensional variable
def generateVerQuad(lim):
    global quadCount
    global cuadruplos
    dirDim = pilaVariables.top()
    codigoOp = tablaOperadores['ver']
    quad = Quadruple(codigoOp, dirDim, None, lim)
    cuadruplos.append(quad)
    quadCount += 1

# Auxiliary function to get the current quadruple count
def getCurrentQuadCount():
    global quadCount
    return quadCount

# Auxiliary function to get the current temporal variables count
def getTempCount():
    global iTempCount
    global fTempCount
    global cTempCount
    global bTempCount
    global pTempCount
    tempCount = [iTempCount, fTempCount, cTempCount, bTempCount, pTempCount]
    return tempCount

# Auxiliary function to reset the temporal variables count
def resetTempCount():
    global iTempCount
    global fTempCount
    global cTempCount
    global bTempCount
    global pTempCount
    iTempCount, fTempCount, cTempCount, bTempCount, pTempCount = 0, 0, 0, 0, 0
