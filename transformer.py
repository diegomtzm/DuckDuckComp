# Diego Martínez A01176489
# Luis Gerardo Bravo A01282014
# Proyecto DuckDuckComp
# Apply the semantic actions to the parsed Tree

from lark import Transformer, Tree
from pprint import pprint

dirFunc = {}
varGlobal = {}
currFunc = 'global'
currType = ''

class Tables(Transformer):
    # def programa(self, args):
    #     pprint(dirFunc)
    #     return Tree('program', args)

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
        idName = args[0]
        if idName in varList:
            print('\nError: multiple declaracion de funciones')
            print(f'\tVariable {args[0]} ya existe en {currFunc}\n')
        else:
            varList[idName] = currType
            if currFunc == 'global':
                varGlobal = varList
            else:
                dirFunc[currFunc]['vars'] = varList

        return Tree('id', args)

    def func_name(self, args):
        global currFunc
        currFunc = args[0]
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
        idName = args[0]
        if idName in varList:
            print('Error: Multiple declaracion de variables')
            print(f'Variable {args[0]} ya existe en {currFunc}')
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
        currType = args[0]
        return Tree('tipo', args)

    def t(self, args):
        global currType
        currType = args[0]
        return Tree('t', args)
