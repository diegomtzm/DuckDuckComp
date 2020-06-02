# Diego Martínez A01176489
# Luis Gerardo Bravo A01282014
# Proyecto DuckDuckComp
# Apply the semantic actions to the parsed Tree

from lark import Transformer, Tree
from pprint import pprint
from quadruples import *
from maquinaVirtual import *

dirFunc = {}
currFunc = 'global'
currType = ''
currFuncCall = ''
currVar = ''
pilaVarDim = Stack()
currDim = 0

# @param: var, name of the variable
# return: variable type in function directory
def getTipo(var):
    if var in dirFunc[currFunc]['vars']:
        return dirFunc[currFunc]['vars'][var][1]
    elif var in dirFunc['global']['vars']:
        return dirFunc['global']['vars'][var][1]
    else:
        raise NameError(f'Variable {var} is not declared')

# @param: operand, name of the variable
# @param: operandType, operand type in function
# return: operand virtual memory address
def getDirV(operand, operandType):
    if operandType == 'variable':
        if operand in dirFunc[currFunc]['vars']:
            return dirFunc[currFunc]['vars'][operand][0]
        elif operand in dirFunc['global']['vars']:
            return dirFunc['global']['vars'][operand][0]
        else:
            raise NameError(f'Variable {operand} is not declared')
    elif operandType == 'cte':
        return tablaCtes[operand]

# @param: var, name of the variable
# @param: query, attribute in function directory
# return: attribute in function directory of the specified variable
def getFromVar(var, query):
    if var in dirFunc[currFunc]['vars']:
        return dirFunc[currFunc]['vars'][var][query]
    elif var in dirFunc['global']['vars']:
        return dirFunc['global']['vars'][var][query]
    else:
        raise NameError(f'Variable {var} is not declared')

# @param: vars, scope
# return: the count of all variables in the scope
def getVarsCount(vars):
    iCount, fCount, cCount, bCount = 0, 0, 0, 0
    for _, val in vars.items():
        if val[1] == 'int':
            iCount += val['size']
        elif val[1] == 'float':
            fCount += val['size']
        elif val[1] == 'char':
            cCount += val['size']
        elif val[1] == 'bool':
            bCount += val['size']
    varsCount = [iCount, fCount, cCount, bCount]
    return varsCount

class Tables(Transformer):
    # Prints the function directory for testing purposes
    # Main program and execute of virtual machine
    def programa(self, args):
        generateEndQuad()
        tempCount = getTempCount()
        dirFunc[currFunc]['tempCount'] = tempCount
        del dirFunc[currFunc]['vars']
        resetTempCount()
        # print("\nDirectorio de funciones:\n")
        # pprint(dirFunc)
        # print("\nTabla de constantes:\n")
        # print(tablaCtes)
        # print("\nTabla de dir de constantes:\n")
        # print(tablaCtesDir)
        # print("\nTabla de operadores:\n")
        # print(tablaOperadores)
        # print("\nPila Variables:\n")
        # print(pilaVariables.get())
        # print("\nPila Tipos:\n")
        # print(pilaTipos.get())
        # print("\nPila Operadores:\n")
        # print(pilaOperadores.get())
        print("\nCuadruplos:\n")
        i = 1
        for c in cuadruplos:
            print(f'{i}. ', end='')
            print(c.get())
            i += 1
        print("\n")
        MV = MaquinaVirtual(cuadruplos, tablaCtesDir, dirFunc)
        MV.execute()
        return Tree('program', args)

    # Declares the start quadruple
    def start(self, args):
        global dirFunc
        if 'global' in dirFunc:
            raise NameError('Double program declaration')
        else:
            dirFunc['global'] = {'type': 'program', 'vars': {}}
            global dvcte
            tablaCtes['1'] = dvcte
            tablaCtesDir[dvcte] = '1'
            dvcte += 1
        return Tree('start', args)

    # Declares a new variable
    def id_name(self, args):
        global currVar
        global dirFunc
        global currFunc
        global currType
        currVar = args[0].value
        varList = dirFunc[currFunc]['vars']
        idName = currVar
        if idName in varList:
            raise NameError(f'Variable {idName} already exists in {currFunc}')
        else:
            if currFunc == "global":
                scope = 'global'
            else:
                scope = 'local'

            dirV = getNewDirV(currType, scope)
            varList[idName] = {0: dirV, 1: currType, 'size': 1, 'dim1': None}
            dirFunc[currFunc]['vars'] = varList
        return Tree('id_name', args)

    # Used for dimensional variables (vector/matrix)
    def dim(self, args):
        global currVar
        global currFunc
        global dvcte
        dim = args[0].value
        if dim > '0':
            if dim not in tablaCtes:
                tablaCtes[dim] = dvcte
                tablaCtesDir[dvcte] = dim
                dvcte += 1
            # One dimensional
            if dirFunc[currFunc]['vars'][currVar]['dim1'] == None:
                dirFunc[currFunc]['vars'][currVar]['dim1'] = dim
                dirFunc[currFunc]['vars'][currVar]['dim2'] = '1'
            # Two dimensional
            else:
                dirFunc[currFunc]['vars'][currVar]['dim2'] = dim
        else:
            raise Exception('Can`t define arrays of size 0')
        return Tree('dim', args)

    # Determines size of variable
    def id(self, args):
        if dirFunc[currFunc]['vars'][currVar]['dim1'] != None:
            if currFunc == "global":
                scope = 'global'
            else:
                scope = 'local'

            # Check if temporal variable
            varDir = getDirV(currVar, 'variable')
            if varDir >= 50000:
                scope += 'Temp'

            varType = getTipo(currVar)
            n = int(dirFunc[currFunc]['vars'][currVar]['dim1']) * int(dirFunc[currFunc]['vars'][currVar]['dim2'])
            dirOffset(varType, scope, n-1)
            dirFunc[currFunc]['vars'][currVar]['size'] = n
        return Tree('id', args)

    # Declares a new function
    def func_name(self, args):
        global currFunc
        currFunc = args[0].value
        if currFunc in dirFunc:
            raise NameError(f'Function {currFunc} already exists')
        else:
            dirFunc[currFunc] = {'type': currType, 'vars': {}, 'params': ''}
            if currType != 'void':
                dirV = getNewDirV(currType, 'global')
                dirFunc['global']['vars'][currFunc] = {0: dirV, 1: currType, 'size': 1, 'dim1': None}
        return Tree('func_name', args)
    
    # Sets current function call to global
    def llamada_name(self, args):
        global currFuncCall
        currFuncCall = args[0].value
        if currFuncCall not in dirFunc:
            raise NameError(f'Function {currFuncCall} is not declared')
        return Tree('llamada_name', args)

    # Generates ERA Quadruple
    def inicio_llamada(self, args):
        params = dirFunc[currFuncCall]['params']
        generateERAQuad(currFuncCall, params)
        pilaOperadores.push("[")
        return ('inicio_llamada', args)

    # Generates PARAM Quadruple
    def params_exp(self, args):
        if pilaDimensions.size() > 0:
            raise RuntimeError('Can`t send arrays as parameters to function')
        else:
            generateParamQuad()
        return ('params_exp', args)

    # Generates GOSUB Quadruple and FUNCTION ASSIGNMENT Quadruple
    def fin_llamada(self, args):
        pilaOperadores.pop()
        initAddress = dirFunc[currFuncCall]['start']
        generateGoSubQuad(initAddress)
        if currFuncCall in dirFunc['global']['vars']:
            dirV = dirFunc['global']['vars'][currFuncCall][0]
            result_type = dirFunc['global']['vars'][currFuncCall][1]
            generateFuncAssignmentQuad(dirV, result_type, currFunc)
        return ('fin_llamada', args)

    # Clean up the function by restarting all virtual memory addresses
    # Generates END FUNCTION Quadruple
    def func(self, args):
        global dvil, dvfl, dvcl, dvbl, dvilt, dvflt, dvclt, dvblt
        dvil = 10000
        dvfl = 13000
        dvcl = 16000
        dvbl = 18000

        dvilt = 58000
        dvflt = 60000
        dvclt = 62000
        dvblt = 64000

        dirVirtual['local'] = {
            'int': dvil,
            'float': dvfl,
            'char': dvcl,
            'bool': dvbl
        }
        dirVirtual['localTemp'] = {
            'int': dvilt,
            'float': dvflt,
            'char': dvclt,
            'bool': dvblt
        }

        generateEndFuncQuad()
        tempCount = getTempCount()
        dirFunc[currFunc]['tempCount'] = tempCount
        del dirFunc[currFunc]['vars']
        resetTempCount()
        return Tree('func', args)

    # Declares parameter variable in local functions directory
    def param_name(self, args):
        global dirFunc
        global currFunc
        global currType
        varList = dirFunc[currFunc]['vars']
        idName = args[0].value
        if idName in varList:
            raise NameError(f'Variable {args[0].value} already exists in {currFunc}')
        else:
            dirV = getNewDirV(currType, 'local')
            varList[idName] = {0: dirV, 1: currType, 'size': 1, 'dim1': None}
            dirFunc[currFunc]['vars'] = varList
            dirFunc[currFunc]['params'] += currType[0]
        return Tree('param_name', args)

    # Adds variable to variable count in function directory
    def dec_var(self, args):
        if currFunc != 'global':
            dirFunc[currFunc]['varsCount'] = getVarsCount(dirFunc[currFunc]['vars'])
        return Tree('dec_var', args)

    # Adds function to variable count in function directory
    # Adds start Quadruple to current function
    def dec_func(self, args):
        if currFunc != 'global':
            dirFunc[currFunc]['varsCount'] = getVarsCount(dirFunc[currFunc]['vars'])
            quadCount = getCurrentQuadCount()
            dirFunc[currFunc]['start'] = quadCount
        return Tree('dec_func', args)

    # Adds start Quadruple and variable count to main function
    def principal(self, args):
        global currFunc
        currFunc = 'global'
        quadCount = getCurrentQuadCount()
        dirFunc[currFunc]['start'] = quadCount
        dirFunc[currFunc]['varsCount'] = getVarsCount(dirFunc[currFunc]['vars'])
        return Tree('principal', args)

    # Sets current type to global
    def tipo(self, args):
        global currType
        currType = args[0].value
        return Tree('tipo', args)

    # Sets current type to global
    def t(self, args):
        global currType
        currType = args[0].value
        return Tree('t', args)

    # Pushes type, address, size and dimensions to piles
    def var_id(self, args):
        var = args[0].value
        tipo = getTipo(var)
        dirV = getDirV(var, 'variable')
        size = getFromVar(var, 'size')
        pilaVariables.push(dirV)
        pilaTipos.push(tipo)
        if size > 1:
            dim1 = int(getFromVar(var,'dim1'))
            dim2 = int(getFromVar(var, 'dim2'))
            pilaDimensions.push((dim1, dim2))
        return Tree('var_id', args)

    # Pops Operators and VarDims piles
    def var_dim(self, args):
        pilaOperadores.pop()
        pilaVarDim.pop()
        return Tree('var_dim', args)
    
    # Sets current variable to global and pushes current variable dimensions to pile
    def var_dim_id(self, args):
        global currVar
        global pilaVarDim
        currVar = args[0].value
        pilaVarDim.push(currVar)
        pilaOperadores.push("[")
        return Tree('var_dim_id', args)

    # Handles expresions in dimensional variable indexing
    def dimn(self, args):
        global currDim
        global currFunc
        global dvcte
        var = pilaVarDim.top()
        if currDim == 0:
            lim = getFromVar(var, 'dim1')
            dirLim = tablaCtes[lim]
            generateVerQuad(dirLim)
            if getFromVar(var, 'dim2') != '1':
                currDim = 1
                dim2 = getFromVar(var, 'dim2')
                dirDim2 = tablaCtes[dim2]
                pilaVariables.push(dirDim2)
                pilaTipos.push('int')
                pilaOperadores.push('*')
                generateQuad(currFunc)
            else:
                dirBase = str(getDirV(var, 'variable'))
                tipoBase = getTipo(var)
                if dirBase not in tablaCtes:
                    tablaCtes[dirBase] = dvcte
                    tablaCtesDir[dvcte] = dirBase
                    dvcte += 1
                pilaVariables.push(tablaCtes[dirBase])
                pilaTipos.push(tipoBase)
                pilaOperadores.push('+')
                generateQuad(currFunc, True)
        else:
            currDim = 0
            lim = getFromVar(var, 'dim2')
            dirLim = tablaCtes[lim]
            generateVerQuad(dirLim)
            pilaOperadores.push('+')
            generateQuad(currFunc)
            dirBase = str(getDirV(var, 'variable'))
            tipoBase = getTipo(var)
            if dirBase not in tablaCtes:
                tablaCtes[dirBase] = dvcte
                tablaCtesDir[dvcte] = dirBase
                dvcte += 1
            pilaVariables.push(tablaCtes[dirBase])
            pilaTipos.push(tipoBase)
            pilaOperadores.push('+')
            generateQuad(currFunc, True)
        return Tree('dimn', args)

    # Handles constant variables
    def number(self, args):
        global dvcte

        var = args[0].value
        if '.' in var:
            tipo = 'float'
        else:
            tipo = 'int'

        if var not in tablaCtes:
            tablaCtes[var] = dvcte
            tablaCtesDir[dvcte] = var
            dvcte += 1

        dirV = getDirV(var, 'cte')
        pilaVariables.push(dirV)
        pilaTipos.push(tipo)
        return Tree('number', args)

    # Handles boolean variables
    def boolean(self, args):
        global dvtrue
        global dvfalse

        var = args[0].value
        if var == "True":
            dirV = dvtrue
        else:
            dirV = dvfalse

        pilaVariables.push(dirV)
        pilaTipos.push('bool')
        return Tree('boolean', args)

    # Handles '*'. Pushes operator to operators pile
    def producto(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('producto', args)

    # Handles '+'. Pushes operator to operators pile
    def adicion(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('adicion', args)

    # Handles '='. Pushes operator to operators pile
    def igual(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('igual', args)

    # Handles '>=', '<=', '!=', '==', '>', '<'. Pushes operator to operators pile
    def op_comp(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('op_comp', args)

    # Generates general Quadruple for '+', '-', '&', '||' operations
    def termino(self, args):
        if pilaOperadores.size() > 0:    
            top = pilaOperadores.top()
            if top in ["+", "-", "&", "||"]:
                if pilaDimensions.size() > 1:
                    rightDims = pilaDimensions.pop()
                    leftDims = pilaDimensions.pop()
                    if rightDims == leftDims:
                        size = rightDims[0] * rightDims[1]
                        generateQuad(currFunc, size=size)
                        pilaDimensions.push(leftDims)
                    else:
                        raise RuntimeError(f'Can`t apply {top} between vars of size {leftDims} and {rightDims}')
                elif pilaDimensions.size() > 0:
                    dims = pilaDimensions.pop()
                    raise RuntimeError(f'Uncompatible sizes {dims} vs 1')
                else:
                    generateQuad(currFunc)
        return Tree('termino', args)

    # Generates general Quadruple for '*', '/' operations
    # Generates Matrix Operations Quadruple for '¡', '?', '$' matrix operations
    def factor(self, args):
        if pilaOperadores.size() > 0: 
            top = pilaOperadores.top()
            if top == "*" or top == "/":
                if pilaDimensions.size() > 1:
                    rightDims = pilaDimensions.pop()
                    leftDims = pilaDimensions.pop()
                    if leftDims[1] == rightDims[0]:
                        generateMatMulQuad(currFunc, leftDims, rightDims)
                        pilaDimensions.push((leftDims[0], rightDims[1]))
                    else:
                        raise RuntimeError(f'Can`t apply {top} between vars of size {leftDims} and {rightDims}')
                elif pilaDimensions.size() > 0:
                    dims = pilaDimensions.pop()
                    raise RuntimeError(f'Uncompatible sizes {dims} vs 1')
                else:
                    generateQuad(currFunc)
            # Inverse and Transpose
            elif top == "¡" or top == "?":
                if pilaDimensions.size() > 0:
                    rightDims = pilaDimensions.pop()
                    generateOpMatQuad(rightDims, currFunc)
                    if top == "¡":
                        pilaDimensions.push((rightDims[1], rightDims[0]))
                    elif top == "?":
                        pilaDimensions.push(rightDims)
                else:
                    raise RuntimeError(f'Can`t apply {top} if it`s not a matrix')
            # Determinant
            elif top == "$":
                if pilaDimensions.size() > 0:
                    rightDims = pilaDimensions.pop()
                    if rightDims[0] == rightDims[1]:
                        generateOpMatQuad(rightDims, currFunc)
                    else:
                        raise RuntimeError(f'Can`t apply {top} to a non-square matrix of size {rightDims[0]}x{rightDims[1]}')
                else:
                    raise RuntimeError(f'Can`t apply {top} if it`s not a matrix')
        return Tree('factor', args)

    # Generates general Quadruple for '>=', '<=', '!=', '==', '>', '<' operations
    def full_exp_comp(self, args):
        if pilaOperadores.size() > 0:
            top = pilaOperadores.top()
            if top in [">", "<", "<=", ">=", "!=", "==", "&", "||"]:
                if pilaDimensions.size() > 0:
                    raise RuntimeError(f'Can`t apply {top} to arrays')
                else:
                    generateQuad(currFunc)
        return Tree('full_exp_comp', args)

    # Generates ASSIGNMENT Quadruple
    def fin_asignacion(self, args):
        if pilaOperadores.size() > 0:
            top = pilaOperadores.top()
            if top == "=":
                if pilaDimensions.size() > 1:
                    rightDims = pilaDimensions.pop()
                    leftDims = pilaDimensions.pop()
                    if rightDims == leftDims:
                        size = rightDims[0] * rightDims[1]
                        generateAssigmentQuad(size)
                        pilaVariables.pop()
                        pilaTipos.pop()
                    else:
                        raise RuntimeError(f'Can`t assign array of size {rightDims} to an array of size {leftDims}')
                elif pilaDimensions.size() > 0:
                    dims = pilaDimensions.pop()
                    raise RuntimeError(f'Uncompatible sizes {dims} vs 1')
                else:
                    generateAssigmentQuad()
                    pilaVariables.pop()
                    pilaTipos.pop()
        return Tree('fin_asignacion', args)

    # Pushes open parentesis to operator pile
    def open_par(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('open_par', args)

    # Pushes closed parentesis to operator pile
    def close_par(self, args):
        pilaOperadores.pop()
        return Tree('close_par', args)
    
    # Generates LEE VARIABLE Quadruple
    def lee_variable(self, args):
        global quadCount
        var = args[0].value
        varDir = getDirV(var, 'variable')
        size = getFromVar(var, 'size')
        if size > 1:
            raise RuntimeError('Can`t apply "lee" to whole arrays')
        else:
            generateLeeVariableQuad(varDir)
        return Tree('lee_variable', args)

    # Generate SALIDA Quadruple
    def string_salida(self, args):
        var = args[0].value
        pilaVariables.push(var.replace('"', ''))
        pilaTipos.push('char')
        generateSalidaQuad()
        return Tree('string_salida', args)

    # Generate SALIDA Quadruple
    def expresion_salida(self, args):
        if pilaDimensions.size() > 0:
            raise RuntimeError('Can`t apply "escribe" to whole arrays')
        else:
            generateSalidaQuad()
        return Tree('expresion_salida', args)

    # Generate NEW LINE Quadruple for ESCRIBE
    def escritura(self, args):
        generateNewLineQuad()
        return Tree('escritura', args)

    # Generate RETORNO Quadruple
    def retorno_expresion(self, args):
        global currFunc
        currFuncVar = dirFunc['global']['vars'][currFunc][0]
        if pilaDimensions.size() > 0:
            raise RuntimeError('Can`t apply "regresa" to whole arrays')
        else:
            generateRetornoExp(currFuncVar)
        return Tree('retorno_expresion', args)

    # Generate DECISION Quadruple
    def decision_exp(self, args):
        if pilaTipos.top() == "bool":
            generateDecisionQuad()
        else:
            raise TypeError("Expected bool result")

        return Tree('decision_exp', args)

    # Generate SINO Quadruple
    def sino(self, args):
        generateSinoQuad()
        return Tree('sino', args)

    # Sets the quadruple number for goTo
    def decision(self, args):
        end = pilaSaltos.pop()
        rellenarQuad(end)
        return Tree('decision', args)

    # Pushes to jump pile
    def mientras(self, args):
        pushJump()

    # Generates DECISION Quadruple
    def haz(self, args):
        if pilaTipos.top() == "bool":
            generateDecisionQuad()
        else:
            raise TypeError("Expected bool result")
        return Tree('haz', args)

    # Generates GOTO Quadruple
    def mientras_bloque(self, args):
        end = pilaSaltos.pop()
        returnJump = pilaSaltos.pop()
        generateGoToQuad(returnJump)
        rellenarQuad(end)
        return Tree('mientras_bloque', args)

    # Pushes variable of FOR to variable and type piles
    def variable_desde(self, args):
        global dirFunc
        global currFunc
        varList = dirFunc[currFunc]['vars']
        idName = args[0].value
        var = getDirV(idName, 'variable')
        varType = getTipo(idName)
        pilaVariables.push(var)
        pilaTipos.push(varType)
        return Tree('variable_desde', args)

    # Generates ASSIGNMENT Quadruple of FOR (i = 0)
    def asignacion_desde_fin(self, args):
        if pilaOperadores.size() > 0:
            top = pilaOperadores.top()
            if top == "=":
                generateAssigmentQuad()
        return Tree('asignacion_desde_fin', args)

    # Generates DESDE and DECISION Quadruple of FOR
    def hacer(self, args):
        pushJump(0)
        generateDesdeQuad(currFunc)
        if pilaTipos.top() == "bool":
            generateDecisionQuad()
        else:
            raise TypeError("Expected bool result")
        return Tree('hacer', args)

    # Generates DESDE FIN and GOTO Quadruples of FOR BLOCK
    def desde_bloque(self, args):
        end = pilaSaltos.pop()
        returnJump = pilaSaltos.pop()
        # cuadruplo k = k + 1;
        dirV = getDirV('1', 'cte')
        generateDesdeFinQuad(currFunc, dirV, 'int')
        generateGoToQuad(returnJump)
        rellenarQuad(end)
        return Tree('desde_bloque', args)

    # Pushes logic operators
    def oplogic(self, args):
        global currFunc
        op = args[0].value
        pilaOperadores.push(op)
        return Tree('op3', args)

    # Pushes matrix operators
    def op_mat(self, args):
        op = args[0].value
        pilaOperadores.push(op)
        return Tree('op_mat', args)

    # Handles and pushes chars
    def char(self, args):
        global dvcte
        char = args[0].value
        if char not in tablaCtes:
            tablaCtes[char] = dvcte
            tablaCtesDir[dvcte] = char
            dvcte += 1
        pilaVariables.push(tablaCtes[char])
        pilaTipos.push('char')
        return Tree('char', args)
        