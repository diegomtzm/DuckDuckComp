from memoryMap import *
from structs import *

arithmeticOps = {
  1: (lambda x,y: x+y), 
  2: (lambda x,y: x-y),
  3: (lambda x,y: x*y),
  4: (lambda x,y: x/y)
}

compOps = {
  6: (lambda x,y: x <= y),
  7: (lambda x,y: x >= y),
  8: (lambda x,y: x > y),
  9: (lambda x,y: x < y),
  10: (lambda x,y: x != y),
  11: (lambda x,y: x == y),
  12: (lambda x,y: x and y),
  13: (lambda x,y: x or y)
}

class MaquinaVirtual:
  def __init__(self, quadruples, ctes, dirFunc):
    self.quadruples = quadruples
    self.ctes = ctes
    self.dirFunc = dirFunc
    self.IP = dirFunc['global']['start']
    self.memGlobal = MemoryMap(dirFunc['global']['varsCount'])
    self.memGlobalTemp = MemoryMap(dirFunc['global']['tempCount'])
    self.memLocal = MemoryMap('0000')
    self.memLocalTemp = MemoryMap('0000')
    self.currFunc = 'global'
    self.pilaFunciones = Stack()
    self.IPatCall = -1
    self.paramsCount = [0,0,0,0]

#  tablaOperadores = {
#   "+": 1, "-": 2, "*": 3, "/": 4, "=": 5, "<=": 6, ">=": 7, ">": 8, "<": 9, 
#   "!=": 10, "==": 11, "&": 12, "||": 13, "lee": 14, "escribe": 15, "regresa": 16,
#   "goTo": 17, "goToF": 18, "endFunc": 19, "end": 20, "era": 21, "param": 22, "goSub": 23
#  }
  def getMemory(self, dirVir):
    # GLOBAL
    if dirVir >= 1000 and dirVir < 4000:
      return self.memGlobal.ints, dirVir - 1000, int
    elif dirVir >= 4000 and dirVir < 7000:
      return self.memGlobal.floats, dirVir - 4000, float
    elif dirVir >= 7000 and dirVir < 9000:
      return self.memGlobal.chars, dirVir - 7000, str
    elif dirVir >= 9000 and dirVir < 10000:
      return self.memGlobal.bools, dirVir - 9000, bool
    # LOCAL
    elif dirVir >= 10000 and dirVir < 13000:
      return self.memLocal.ints, dirVir - 10000, int
    elif dirVir >= 13000 and dirVir < 16000:
      return self.memLocal.floats, dirVir - 13000, float
    elif dirVir >= 16000 and dirVir < 18000:
      return self.memLocal.chars, dirVir - 16000, str
    elif dirVir >= 18000 and dirVir < 19000:
      return self.memLocal.bools, dirVir - 18000, bool
    # GLOBALTEMP
    elif dirVir >= 50000 and dirVir < 52000:
      return self.memGlobalTemp.ints, dirVir - 50000, int
    elif dirVir >= 52000 and dirVir < 54000:
      return self.memGlobalTemp.floats, dirVir - 52000, float
    elif dirVir >= 54000 and dirVir < 56000:
      return self.memGlobalTemp.chars, dirVir - 54000, str
    elif dirVir >= 56000 and dirVir < 58000:
      return self.memGlobalTemp.bools, dirVir - 56000, bool
    # LOCALTEMP
    elif dirVir >= 58000 and dirVir < 60000:
      return self.memLocalTemp.ints, dirVir - 58000, int
    elif dirVir >= 60000 and dirVir < 62000:
      return self.memLocalTemp.floats, dirVir - 60000, float
    elif dirVir >= 62000 and dirVir < 64000:
      return self.memLocalTemp.chars, dirVir - 62000, str
    elif dirVir >= 64000 and dirVir < 66000:
      return self.memLocalTemp.bools, dirVir - 64000, bool
    # CTES
    elif dirVir >= 66000 and dirVir < 68000:
      if '.' in self.ctes[dirVir]:
        tipo = float
      else:
        tipo = int
      return self.ctes, dirVir, tipo
    else:
      raise IndexError(f'Index {dirVir} out of range')

  def switch(self, codigoOp):
    # case '='
    if codigoOp == 5: 
      leftOp = self.quadruples[self.IP].leftOp
      memoria, dirOffset, _ = self.getMemory(leftOp)
      valor = memoria[dirOffset]

      res = self.quadruples[self.IP].res
      memoria, dirOffset, _ = self.getMemory(res)
      print(f'memoria: {memoria}')
      print(f'dirOffset: {dirOffset}')
      memoria[dirOffset] = valor
      print(f'res: {memoria}')
    # case '<=', '>=', '>', '<', '!=', '==', '&', '||'
    elif codigoOp == 6 or codigoOp == 7 or codigoOp == 8 or codigoOp == 9 \
      or codigoOp == 10 or codigoOp == 11 or codigoOp == 12 or codigoOp == 13:
      leftOp = self.quadruples[self.IP].leftOp
      memoria, dirOffset, tipoL = self.getMemory(leftOp)
      valorLeft = memoria[dirOffset]
      
      rightOp = self.quadruples[self.IP].rightOp
      memoria, dirOffset, tipoR = self.getMemory(rightOp)
      valorRight = memoria[dirOffset]

      compRes = compOps[codigoOp](tipoL(valorLeft), tipoR(valorRight))
      res = self.quadruples[self.IP].res
      memoria, dirOffset, _ = self.getMemory(res)

      memoria[dirOffset] = compRes
    # case '+', '-', '*', '/'
    elif codigoOp == 1 or codigoOp == 2 or codigoOp == 3 or codigoOp == 4:
      leftOp = self.quadruples[self.IP].leftOp
      memoria, dirOffset, tipoL = self.getMemory(leftOp)
      valorLeft = memoria[dirOffset]
      
      rightOp = self.quadruples[self.IP].rightOp
      memoria, dirOffset, tipoR = self.getMemory(rightOp)
      valorRight = memoria[dirOffset]
      print(self.pilaFunciones.get())
      arithmeticRes = arithmeticOps[codigoOp](tipoL(valorLeft), tipoR(valorRight))
      res = self.quadruples[self.IP].res
      memoria, dirOffset, _ = self.getMemory(res)

      memoria[dirOffset] = arithmeticRes
    # case 'lee'
    elif codigoOp == 14:
      res = self.quadruples[self.IP].res
      memoria, dirOffset, tipo = self.getMemory(res)
      valor = input()
      memoria[dirOffset] = tipo(valor)
      print(f'res: {memoria}')
    # case 'escribe'
    elif codigoOp == 15:
      res = self.quadruples[self.IP].res
      if type(res) == str:
        print(res)
      else:
        memoria, dirOffset, _ = self.getMemory(res)
        print(memoria[dirOffset])
    # case 'gotoF'
    elif codigoOp == 18:
      dirV = self.quadruples[self.IP].leftOp
      memoria, dirOffset, tipoL = self.getMemory(dirV)
      valor = memoria[dirOffset]
      dirGoTo = self.quadruples[self.IP].res
      if valor == False:
        self.IP = dirGoTo - 1
    # case 'goTo'
    elif codigoOp == 17:
      dirGoTo = self.quadruples[self.IP].res
      self.IP = dirGoTo - 1
    # case 'era'
    elif codigoOp == 21:
      self.currFunc = self.quadruples[self.IP].leftOp
      memLocal = self.memLocal
      memLocalTemp = self.memLocalTemp
      self.pilaFunciones.push((memLocal, memLocalTemp))
      self.memLocal = MemoryMap(self.dirFunc[self.currFunc]['varsCount'])
      self.memLocalTemp = MemoryMap(self.dirFunc[self.currFunc]['tempCount'])
    # case 'endFunc'
    elif codigoOp == 19:
      self.IP = self.IPatCall
      memLocal = self.memLocal
      memLocalTemp = self.memLocalTemp
      del memLocal
      del memLocalTemp
      self.pilaFunciones.pop()
      self.memLocal = self.pilaFunciones.top()[0]
      self.memLocalTemp = self.pilaFunciones.top()[1]
      self.paramsCount = '0000'
      print(self.memLocal.get())
      print(self.memLocalTemp.get())
    # case 'param'
    elif codigoOp == 22:
      params = self.dirFunc[self.currFunc]['params']
      paramNum = self.quadruples[self.IP].rightOp
      paramType = params[paramNum]
      dirV = -1
      if paramType == 'i':
        dirV = 10000 + int(self.paramsCount[0])
        self.paramsCount[0] += 1
      elif paramType == 'f':
        dirV = 13000 + int(self.paramsCount[1])
        self.paramsCount[1] += 1
      elif paramType == 'c':
        dirV = 16000 + int(self.paramsCount[2])
        self.paramsCount[2] += 1
      elif paramType == 'b':
        dirV = 18000 + int(self.paramsCount[3])
        self.paramsCount[3] += 1
      
      leftOp = self.quadruples[self.IP].leftOp
      memoria, dirOffset, _ = self.getMemory(leftOp)
      valor = memoria[dirOffset]
      memoria, dirOffset, _ = self.getMemory(dirV)
      memoria[dirOffset] = valor
    # case 'goSub'
    elif codigoOp == 23:
      self.IPatCall = self.IP
      dirGoSub = self.quadruples[self.IP].res
      self.IP = dirGoSub - 1
    # case 'regresa'
    elif codigoOp == 16:
      retDir = self.quadruples[self.IP].res
      memoria, dirOffset, tipoRet = self.getMemory(retDir)
      retVal = memoria[dirOffset]

      res = self.dirFunc['global']['vars'][self.currFunc][0]
      memoria, dirOffset, tipoFunc = self.getMemory(res)
      if tipoRet == tipoFunc:
        memoria[dirOffset] = retVal
      else:
        raise TypeError(f'Func {self.currFunc} is returning {tipoRet} instead of {tipoFunc}')

  def execute(self):
    self.pilaFunciones.push(([[],[],[],[]], [[],[],[],[]]))
    while self.IP < len(self.quadruples):
      self.switch(self.quadruples[self.IP].op)
      self.IP += 1
