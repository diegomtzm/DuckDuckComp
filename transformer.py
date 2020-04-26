# Diego Martínez A01176489
# Luis Gerardo Bravo A01282014
# Proyecto DuckDuckComp
# Apply the semantic actions to the parsed Tree

from lark import Transformer, Tree
from pprint import pprint
from quadruples import *

dirFunc = {}
varGlobal = {}
currFunc = 'global'
currType = ''
temps = [None] * 1000
tempCount = 0
types = {
    'int': int,
    'float': float,
    'char': str,
    'bool': bool
}

def getTipo(var):
    if var in dirFunc[currFunc]['vars']:
        return dirFunc[currFunc]['vars'][var]
    elif var in dirFunc['global']['vars']:
        return dirFunc['global']['vars'][var]
    else:
        print(f'Error: Variable {var} no esta declarada')
        return False

class Tables(Transformer):
    # Imprime el directorio de funciones para hacer pruebas
    def programa(self, args):
        print("\nDirectorio de funciones:\n")
        pprint(dirFunc)
        print("\nPila Variables:\n")
        print(pilaVariables.get())
        print("\nPila Tipos:\n")
        print(pilaTipos.get())
        print("\nPila Operadores:\n")
        print(pilaOperadores.get())
        print("\nCuadruplos:\n")
        print(cuadruplos)
        return Tree('program', args)

    def start(self, args):
        global dirFunc
        global varGlobal
        if args[1] in dirFunc:
            print('Funcion ya existe')
        else:
            dirFunc['global'] = {'type': 'program', 'vars': varGlobal}

        return Tree('start', args)

    def id(self, args):
        global dirFunc
        global currFunc
        global currType
        varList = dirFunc[currFunc]['vars']
        idName = args[0].value
        if idName in varList:
            print('\nError: multiple declaracion de funciones')
            print(f'\tVariable {args[0].value} ya existe en {currFunc}\n')
        else:
            varList[idName] = currType
            if currFunc == 'global':
                varGlobal = varList
            else:
                dirFunc[currFunc]['vars'] = varList

        return Tree('id', args)

    def func_name(self, args):
        global currFunc
        currFunc = args[0].value
        if currFunc in dirFunc:
            print('\nError: multiple declaracion de funciones')
            print(f'\tFuncion {currFunc} ya existe\n')
        else:
            dirFunc[currFunc] = {'type': currType, 'vars': {}}

        return Tree('func_name', args)

    def param_name(self, args):
        global dirFunc
        global currFunc
        global currType
        varList = dirFunc[currFunc]['vars']
        idName = args[0].value
        if idName in varList:
            print('Error: Multiple declaracion de variables')
            print(f'Variable {args[0].value} ya existe en {currFunc}')
        else:
            varList[idName] = currType
            dirFunc[currFunc]['vars'] = varList

        return Tree('param_name', args)

    def principal(self, args):
        global currFunc
        currFunc = 'global'
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
        pilaVariables.push(var)
        pilaTipos.push(tipo)
        return Tree('variable', args)

    def number(self, args):
        var = args[0].value
        pilaVariables.push(var)
        pilaTipos.push('int')
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

    def termino(self, args):
        if pilaOperadores.size() > 0:    
            top = pilaOperadores.top()
            if top == "+" or top == "-":
                rightOp = pilaVariables.pop()
                rightType = pilaTipos.pop()
                leftOp = pilaVariables.pop()
                leftType = pilaTipos.pop()
                oper = pilaOperadores.pop()
                result_type = 'int' # HACER CUBO SEMANTICO!!!
                if(result_type != 'ERROR'):
                    global tempCount
                    global quadCount
                    global cuadruplos
                    # HACER MEMORIA VIRTUAL!!!
                    temps[tempCount] = ops[oper](types[leftType](leftOp), types[rightType](rightOp))
                    quad = Quadruple(oper, leftOp, rightOp, temps[tempCount])
                    cuadruplos.append(quad.get())
                    pilaVariables.push(temps[tempCount])
                    pilaTipos.push(result_type)
                    tempCount += 1
                    quadCount += 1
                else:
                    print("Error: Type mismatch")
        return Tree('termino', args)

    def factor(self, args):
        if pilaOperadores.size() > 0: 
            top = pilaOperadores.top()
            if top == "*" or top == "/":
                rightOp = pilaVariables.pop()
                rightType = pilaTipos.pop()
                leftOp = pilaVariables.pop()
                leftType = pilaTipos.pop()
                oper = pilaOperadores.pop()
                result_type = 'int' # HACER CUBO SEMANTICO!!!
                if(result_type != 'ERROR'):
                    global tempCount
                    global quadCount
                    # HACER MEMORIA VIRTUAL!!!
                    temps[tempCount] = ops[oper](types[leftType](leftOp), types[leftType](rightOp))
                    quad = Quadruple(oper, leftOp, rightOp, temps[tempCount])
                    cuadruplos.append(quad.get())
                    pilaVariables.push(temps[tempCount])
                    pilaTipos.push(result_type)
                    tempCount += 1
                    quadCount += 1
                else:
                    print("Error: Type mismatch")
        return Tree('factor', args)

    def fin_asignacion(self, args):
        if pilaOperadores.size() > 0:
            top = pilaOperadores.top()
            if top == "=":
                res = pilaVariables.pop()
                resType = pilaTipos.pop()
                var = pilaVariables.pop()
                varType = pilaTipos.pop()
                oper = pilaOperadores.pop()
                result_type = 'int' # HACER CUBO SEMANTICO!!!
                if(result_type != 'ERROR'):
                    global quadCount
                    # valor de variable = resultado en memoria virtual
                    quad = Quadruple(oper, res, None, var)
                    cuadruplos.append(quad.get())
                    quadCount += 1
                else:
                    print("Error: Type mismatch")
        return Tree('fin_asignacion', args) 
    