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

# Return the variable type
def getTipo(var):
    if var in dirFunc[currFunc]['vars']:
        return dirFunc[currFunc]['vars'][var][1]
    elif var in dirFunc['global']['vars']:
        return dirFunc['global']['vars'][var][1]
    else:
        raise NameError(f'Variable {var} no esta declarada')

# Return the operand virtual memory address
def getDirV(operand, operandType):
    if operandType == 'variable':
        if operand in dirFunc[currFunc]['vars']:
            return dirFunc[currFunc]['vars'][operand][0]
        elif operand in dirFunc['global']['vars']:
            return dirFunc['global']['vars'][operand][0]
        else:
            raise NameError(f'Variable {operand} no esta declarada')
    elif operandType == 'cte':
        return tablaCtes[operand]

def getVarsCount(vars):
    iCount, fCount, cCount, bCount = 0, 0, 0, 0
    for _, val in vars.items():
        if val[1] == 'int':
            iCount += 1
        elif val[1] == 'float':
            fCount += 1
        elif val[1] == 'char':
            cCount += 1
        elif val[1] == 'bool':
            bCount += 1
    varsCount = str(iCount) + str(fCount) + str(cCount) + str(bCount)
    return varsCount

class Tables(Transformer):
    # Imprime el directorio de funciones para hacer pruebas
    def programa(self, args):
        generateEndQuad()
        tempCount = getTempCount()
        dirFunc[currFunc]['tempCount'] = tempCount
        # No se borran aun para poder probar, 
        # descomentar siguiente linea para borrar la tabla de variables
        # del dirFunc[currFunc]['vars']
        resetTempCount()

        print("\nDirectorio de funciones:\n")
        pprint(dirFunc)
        print("\nTabla de constantes:\n")
        print(tablaCtes)
        print("\nTabla de dir de constantes:\n")
        print(tablaCtesDir)
        print("\nTabla de operadores:\n")
        print(tablaOperadores)
        print("\nPila Variables:\n")
        print(pilaVariables.get())
        print("\nPila Tipos:\n")
        print(pilaTipos.get())
        print("\nPila Operadores:\n")
        print(pilaOperadores.get())
        print("\nCuadruplos:\n")
        for c in cuadruplos:
            print(c.get(), end='')
        print("\n")
        MV = MaquinaVirtual(cuadruplos, tablaCtesDir, dirFunc)
        MV.execute()
        return Tree('program', args)

    def start(self, args):
        global dirFunc
        if 'global' in dirFunc:
            raise NameError('doble declaración de programa')
        else:
            dirFunc['global'] = {'type': 'program', 'vars': {}}

        return Tree('start', args)

    def id(self, args):
        global dirFunc
        global currFunc
        global currType
        varList = dirFunc[currFunc]['vars']
        idName = args[0].value
        if idName in varList:
            raise NameError(f'Variable {idName} ya existe en {currFunc}')
        else:
            if currFunc == "global":
                scope = 'global'
            else:
                scope = 'local'

            dirV = getNewDirV(currType, scope)
            varList[idName] = [dirV, currType]
            dirFunc[currFunc]['vars'] = varList

        return Tree('id', args)

    def func_name(self, args):
        global currFunc
        currFunc = args[0].value
        if currFunc in dirFunc:
            raise NameError(f'Funcion {currFunc} ya existe')
        else:
            dirFunc[currFunc] = {'type': currType, 'vars': {}, 'params': ''}
            if currType != 'void':
                dirV = getNewDirV(currType, 'global')
                dirFunc['global']['vars'][currFunc] = [dirV, currType]

        return Tree('func_name', args)
    
    def llamada_name(self, args):
        global currFuncCall
        currFuncCall = args[0].value
        if currFuncCall not in dirFunc:
            raise NameError(f'La funcion: {currFuncCall} no existe\n')

        return Tree('llamada_name', args)

    def inicio_llamada(self, args):
        params = dirFunc[currFuncCall]['params']
        generateERAQuad(currFuncCall, params)
        return ('inicio_llamada', args)

    def params_exp(self, args):
        generateParamQuad()
        return ('params_exp', args)

    def fin_llamada(self, args):
        initAddress = dirFunc[currFuncCall]['start']
        generateGoSubQuad(initAddress)
        if currFuncCall in dirFunc['global']['vars']:
            dirV = dirFunc['global']['vars'][currFuncCall][0]
            result_type = dirFunc['global']['vars'][currFuncCall][1]
            generateFuncAssignmentQuad(dirV, result_type)
        return ('fin_llamada', args)

    # Clean up the function by restarting all virtual memory addresses
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
        # No se borran aun para poder probar, 
        # descomentar siguiente linea para borrar la tabla de variables
        # del dirFunc[currFunc]['vars']
        resetTempCount()

        return Tree('func', args)

    def param_name(self, args):
        global dirFunc
        global currFunc
        global currType
        varList = dirFunc[currFunc]['vars']
        idName = args[0].value
        if idName in varList:
            raise NameError(f'Variable {args[0].value} ya existe en {currFunc}')
        else:
            dirV = getNewDirV(currType, 'local')
            varList[idName] = [dirV, currType]
            dirFunc[currFunc]['vars'] = varList
            dirFunc[currFunc]['params'] += currType[0]

        return Tree('param_name', args)

    def dec_var(self, args):
        if currFunc != 'global':
            dirFunc[currFunc]['varsCount'] = getVarsCount(dirFunc[currFunc]['vars'])
            quadCount = getCurrentQuadCount()
            dirFunc[currFunc]['start'] = quadCount
        
        return Tree('dec_var', args)

    def principal(self, args):
        global currFunc
        currFunc = 'global'
        quadCount = getCurrentQuadCount()
        dirFunc[currFunc]['start'] = quadCount
        dirFunc[currFunc]['varsCount'] = getVarsCount(dirFunc[currFunc]['vars'])
        return Tree('principal', args)

    def tipo(self, args):
        global currType
        currType = args[0].value
        return Tree('tipo', args)

    def t(self, args):
        global currType
        currType = args[0].value
        return Tree('t', args)

    def variable(self, args):
        var = args[0].value
        tipo = getTipo(var)
        dirV = getDirV(var, 'variable')
        pilaVariables.push(dirV)
        pilaTipos.push(tipo)
        return Tree('variable', args)

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

    def producto(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('producto', args)

    def adicion(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('adicion', args)

    def igual(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('igual', args)

    def op_comp(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('op_comp', args)

    def termino(self, args):
        if pilaOperadores.size() > 0:    
            top = pilaOperadores.top()
            if top == "+" or top == "-":
                generateQuad(currFunc)

        return Tree('termino', args)

    def factor(self, args):
        if pilaOperadores.size() > 0: 
            top = pilaOperadores.top()
            if top == "*" or top == "/":
                generateQuad(currFunc)
        return Tree('factor', args)

    def full_exp_comp(self, args):
        if pilaOperadores.size() > 0:
            top = pilaOperadores.top()
            if top in [">", "<", "<=", ">=", "!=", "=="]:
                generateQuad(currFunc)
        return Tree('full_exp_comp', args)

    def fin_asignacion(self, args):
        if pilaOperadores.size() > 0:
            top = pilaOperadores.top()
            if top == "=":
                generateAssigmentQuad()
                pilaVariables.pop()
                pilaTipos.pop()
        return Tree('fin_asignacion', args)

    def open_par(self, args):
        oper = args[0].value
        pilaOperadores.push(oper)
        return Tree('open_par', args)

    def close_par(self, args):
        pilaOperadores.pop()
        return Tree('close_par', args)
    
    def lee_variable(self, args):
        global quadCount
        var = args[0].value
        varDir = dirFunc[currFunc]['vars'][var][0]
        generateLeeVariableQuad(varDir)
        return Tree('lee_variable', args)

    def string_salida(self, args):
        var = args[0].value
        pilaVariables.push(var)
        pilaTipos.push('char')
        generateSalidaQuad()
        return Tree('string_salida', args)

    def expresion_salida(self, args):
        generateSalidaQuad()
        return Tree('expresion_salida', args)

    def retorno_expresion(self, args):
        generateRetornoExp()
        # Falta hacer return al resultado
        return Tree('retorno_expresion', args)

    def decision_exp(self, args):
        if pilaTipos.top() == "bool":
            generateDecisionQuad()
        else:
            raise TypeError("Expected bool result")

        return Tree('decision_exp', args)

    def sino(self, args):
        generateSinoQuad()
        return Tree('sino', args)

    def decision(self, args):
        end = pilaSaltos.pop()
        rellenarQuad(end)
        return Tree('decision', args)

    def mientras(self, args):
        pushJump()

    def haz(self, args):
        if pilaTipos.top() == "bool":
            generateDecisionQuad()
        else:
            raise TypeError("Expected bool result")
        return Tree('haz', args)

    def mientras_bloque(self, args):
        end = pilaSaltos.pop()
        returnJump = pilaSaltos.pop()
        generateGoToQuad(returnJump)
        rellenarQuad(end)
        return Tree('mientras_bloque', args)

    def variable_desde(self, args):
        global dirFunc
        global currFunc
        varList = dirFunc[currFunc]['vars']
        idName = args[0].value
        if idName not in varList:
            raise NameError(f'Variable {args[0].value} no existe en {currFunc}')
        else:
            var = dirFunc[currFunc]['vars'][idName][0]
            varType = dirFunc[currFunc]['vars'][idName][1]
            pilaVariables.push(var)
            pilaTipos.push(varType)

        return Tree('variable_desde', args)

    def asignacion_desde_fin(self, args):
        if pilaOperadores.size() > 0:
            top = pilaOperadores.top()
            if top == "=":
                generateAssigmentQuad()
        return Tree('asignacion_desde_fin', args)

    def hacer(self, args):
        pushJump(-1)
        generateDesdeQuad(currFunc)
        if pilaTipos.top() == "bool":
            generateDecisionQuad()
        else:
            raise TypeError("Expected bool result")
        return Tree('hacer', args)

    def desde_bloque(self, args):
        end = pilaSaltos.pop()
        returnJump = pilaSaltos.pop()
        # cuadruplo k = k + 1;
        if '1' not in tablaCtes:
            global dvcte
            tablaCtes['1'] = dvcte
            tablaCtesDir[dvcte] = '1'
            dvcte += 1

        dirV = getDirV('1', 'cte')
        generateDesdeFinQuad(currFunc, dirV, 'int')
        generateGoToQuad(returnJump)
        rellenarQuad(end)
        return Tree('desde_bloque', args)