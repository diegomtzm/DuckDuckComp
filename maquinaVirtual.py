from memoryMap import *

arithmeticOps = {
  1: (lambda x,y: x+y), 
  2: (lambda x,y: x-y),
  3: (lambda x,y: x*y),
  4: (lambda x,y: x/y)
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
      print('Error: OVERFLOW')

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
    # case '+', '-', '*', '/'
    elif codigoOp == 1 or codigoOp == 2 or codigoOp == 3 or codigoOp == 4:
      leftOp = self.quadruples[self.IP].leftOp
      memoria, dirOffset, tipoL = self.getMemory(leftOp)
      valorLeft = memoria[dirOffset]
      
      rightOp = self.quadruples[self.IP].rightOp
      memoria, dirOffset, tipoR = self.getMemory(rightOp)
      valorRight = memoria[dirOffset]

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

  def execute(self):
    while self.IP < len(self.quadruples):
      self.switch(self.quadruples[self.IP].op)
      self.IP += 1




  