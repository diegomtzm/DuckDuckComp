import numpy as np
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
    self.memLocalOld = self.memLocal
    self.memLocalTempOld = self.memLocalTemp
    self.currFunc = 'global'
    self.pilaFunciones = Stack()
    self.IPatCall = Stack()
    self.paramsCount = [0,0,0,0]
    self.inParams = False

  def checkPointer(self, dirV):
    if dirV >= 70000:
      memoria, dirOffset, _ = self.getMemory(dirV)
      dirV = memoria[dirOffset]
    return dirV

#  tablaOperadores = {
#   "+": 1, "-": 2, "*": 3, "/": 4, "=": 5, "<=": 6, ">=": 7, ">": 8, "<": 9, 
#   "!=": 10, "==": 11, "&": 12, "||": 13, "lee": 14, "escribe": 15, "regresa": 16,
#   "goTo": 17, "goToF": 18, "endFunc": 19, "end": 20, "era": 21, "param": 22, "goSub": 23
#  }
  def getMemory(self, dirVir, version='current'):
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
    elif dirVir >= 10000 and dirVir < 13000 and version == 'current': 
      return self.memLocal.ints, dirVir - 10000, int
    elif dirVir >= 13000 and dirVir < 16000 and version == 'current': 
      return self.memLocal.floats, dirVir - 13000, float
    elif dirVir >= 16000 and dirVir < 18000 and version == 'current': 
      return self.memLocal.chars, dirVir - 16000, str
    elif dirVir >= 18000 and dirVir < 19000 and version == 'current': 
      return self.memLocal.bools, dirVir - 18000, bool
    elif dirVir >= 10000 and dirVir < 13000 and version == 'old': 
      return self.memLocalOld.ints, dirVir - 10000, int
    elif dirVir >= 13000 and dirVir < 16000 and version == 'old': 
      return self.memLocalOld.floats, dirVir - 13000, float
    elif dirVir >= 16000 and dirVir < 18000 and version == 'old': 
      return self.memLocalOld.chars, dirVir - 16000, str
    elif dirVir >= 18000 and dirVir < 19000 and version == 'old': 
      return self.memLocalOld.bools, dirVir - 18000, bool
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
    elif dirVir >= 58000 and dirVir < 60000 and version == 'current':
      return self.memLocalTemp.ints, dirVir - 58000, int
    elif dirVir >= 60000 and dirVir < 62000 and version == 'current':
      return self.memLocalTemp.floats, dirVir - 60000, float
    elif dirVir >= 62000 and dirVir < 64000 and version == 'current':
      return self.memLocalTemp.chars, dirVir - 62000, str
    elif dirVir >= 64000 and dirVir < 66000 and version == 'current':
      return self.memLocalTemp.bools, dirVir - 64000, bool
    elif dirVir >= 58000 and dirVir < 60000 and version == 'old':
      return self.memLocalTempOld.ints, dirVir - 58000, int
    elif dirVir >= 60000 and dirVir < 62000 and version == 'old':
      return self.memLocalTempOld.floats, dirVir - 60000, float
    elif dirVir >= 62000 and dirVir < 64000 and version == 'old':
      return self.memLocalTempOld.chars, dirVir - 62000, str
    elif dirVir >= 64000 and dirVir < 66000 and version == 'old':
      return self.memLocalTempOld.bools, dirVir - 64000, bool
    # CTES
    elif dirVir >= 66000 and dirVir < 68000:
      if ord(self.ctes[dirVir][0]) >= 65:
        tipo = str
      elif '.' in self.ctes[dirVir]:
        tipo = float
      else:
        tipo = int
      return self.ctes, dirVir, tipo
    # POINTERS GLOBALTEMP
    elif dirVir >= 70000 and dirVir < 72000:
      return self.memGlobalTemp.pointers, dirVir - 70000, None
    # POINTERS LOCALTEMP
    elif dirVir >= 72000 and dirVir < 74000:
      return self.memLocalTemp.pointers, dirVir - 72000, None
    elif dirVir == 800 or dirVir == 900:
      d = {800: True, 900: False}
      return d, dirVir, bool
    else:
      raise IndexError(f'Address {dirVir} out of range')

  def switch(self, codigoOp):
    # case '='
    if codigoOp == 5: 
      leftOp = self.checkPointer(self.quadruples[self.IP].leftOp)
      memoriaL, dirOffsetL, _ = self.getMemory(leftOp)

      res = self.checkPointer(self.quadruples[self.IP].res)
      memoriaR, dirOffsetR, _ = self.getMemory(res)

      size = self.quadruples[self.IP].rightOp
      for i in range(0,size):
        valor = memoriaL[dirOffsetL+i]
        memoriaR[dirOffsetR+i] = valor

    # case '<=', '>=', '>', '<', '!=', '==', '&', '||'
    elif codigoOp == 6 or codigoOp == 7 or codigoOp == 8 or codigoOp == 9 \
      or codigoOp == 10 or codigoOp == 11 or codigoOp == 12 or codigoOp == 13:
      if self.inParams:
        mem = 'old'
      else:
        mem = 'current'

      leftOp = self.checkPointer(self.quadruples[self.IP].leftOp)
      memoria, dirOffset, tipoL = self.getMemory(leftOp, mem)
      valorLeft = memoria[dirOffset]
      
      rightOp = self.checkPointer(self.quadruples[self.IP].rightOp)
      memoria, dirOffset, tipoR = self.getMemory(rightOp, mem)
      valorRight = memoria[dirOffset]
      compRes = compOps[codigoOp](tipoL(valorLeft), tipoR(valorRight))
      res = self.quadruples[self.IP].res
      memoria, dirOffset, _ = self.getMemory(res, mem)

      memoria[dirOffset] = compRes
    # case '+', '-', '*', '/'
    elif codigoOp == 1 or codigoOp == 2 or codigoOp == 3 or codigoOp == 4:
      if self.inParams:
        mem = 'old'
      else:
        mem = 'current'

      leftOp = self.quadruples[self.IP].leftOp
      rightOp = self.quadruples[self.IP].rightOp
      res = self.quadruples[self.IP].res
      if type(leftOp) == tuple and type(rightOp) == tuple:
        dirVLeft = leftOp[0]
        leftDims = leftOp[1]
        dirVRight = rightOp[0]
        rightDims = rightOp[1]
        dirV = res
        size = leftDims[0] * rightDims[1]
      elif type(res) == tuple:
        dirV = res[0]
        size = res[1]
        dirVLeft = self.checkPointer(leftOp)
        dirVRight = self.checkPointer(rightOp)
      else:
        dirVLeft = self.checkPointer(leftOp)
        dirVRight = self.checkPointer(rightOp)
        dirV = res
        size = 1
      memoriaRes, dirOffsetRes, _ = self.getMemory(dirV, mem)
      memoriaL, dirOffsetL, tipoL = self.getMemory(dirVLeft, mem) 
      memoriaR, dirOffsetR, tipoR = self.getMemory(dirVRight, mem)

      res = [None] * size
      if codigoOp == 3 and type(leftOp) == tuple and type(rightOp) == tuple:
        leftSize = leftDims[0] * leftDims[1]
        leftTemp = [None] * leftSize
        rightSize = rightDims[0] * rightDims[1]
        rightTemp = [None] * rightSize
        for i in range(0, leftSize):
          leftTemp[i] = memoriaL[dirOffsetL+i]
        for i in range(0, rightSize):
          rightTemp[i] = memoriaR[dirOffsetR+i]
        
        leftTempMatrix = np.reshape(leftTemp, leftDims)
        leftMatrix = np.matrix(leftTempMatrix)
        rightTempMatrix = np.reshape(rightTemp, rightDims)
        rightMatrix = np.matrix(rightTempMatrix)

        matrixRes = np.dot(leftMatrix, rightMatrix)
        res = matrixRes.A1

      else:
        for i in range(0, size):
          valorLeft = memoriaL[dirOffsetL+i]
          valorRight = memoriaR[dirOffsetR+i]
          arithmeticRes = arithmeticOps[codigoOp](tipoL(valorLeft), tipoR(valorRight))
          res[i] = arithmeticRes

      for i in range(0, size):
        memoriaRes[dirOffsetRes+i] = res[i]

    # case 'lee'
    elif codigoOp == 14:
      res = self.checkPointer(self.quadruples[self.IP].res)
      memoria, dirOffset, tipo = self.getMemory(res)
      valor = input()
      memoria[dirOffset] = tipo(valor)
    # case 'escribe'
    elif codigoOp == 15:
      res = self.quadruples[self.IP].res
      rightOp = self.quadruples[self.IP].rightOp

      if rightOp == "nl":
        print()
      elif type(res) == str:
        print(res, end=" ")
      else:
        res = self.checkPointer(res)
        memoria, dirOffset, _ = self.getMemory(res)
        print(memoria[dirOffset], end=" ")
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
      self.memLocalOld = self.memLocal
      self.memLocalTempOld = self.memLocalTemp
      self.paramsCount = [0,0,0,0]
      self.memLocal = MemoryMap(self.dirFunc[self.currFunc]['varsCount'])
      self.memLocalTemp = MemoryMap(self.dirFunc[self.currFunc]['tempCount'])
      self.pilaFunciones.push((self.memLocal, self.memLocalTemp))
      self.inParams = True
    # case 'endFunc'
    elif codigoOp == 19:
      ip = self.IPatCall.pop()
      self.IP = ip
      memLocal = self.memLocal
      memLocalTemp = self.memLocalTemp
      del memLocal
      del memLocalTemp
      self.pilaFunciones.pop()
      self.memLocal = self.pilaFunciones.top()[0]
      self.memLocalTemp = self.pilaFunciones.top()[1]
    # case 'param'
    elif codigoOp == 22:
      params = self.dirFunc[self.currFunc]['params']
      paramNum = self.quadruples[self.IP].rightOp
      paramType = params[paramNum]
      dirV = -1
      if paramType == 'i':
        dirV = 10000 + self.paramsCount[0]
        self.paramsCount[0] += 1
      elif paramType == 'f':
        dirV = 13000 + self.paramsCount[1]
        self.paramsCount[1] += 1
      elif paramType == 'c':
        dirV = 16000 + self.paramsCount[2]
        self.paramsCount[2] += 1
      elif paramType == 'b':
        dirV = 18000 + self.paramsCount[3]
        self.paramsCount[3] += 1
      
      leftOp = self.checkPointer(self.quadruples[self.IP].leftOp)
      memoria, dirOffset, _ = self.getMemory(leftOp, 'old')
      valor = memoria[dirOffset]
      memoria, dirOffset, _ = self.getMemory(dirV)
      memoria[dirOffset] = valor
    # case 'goSub'
    elif codigoOp == 23:
      self.IPatCall.push(self.IP)
      dirGoSub = self.quadruples[self.IP].res
      self.IP = dirGoSub - 1
      self.inParams = False
    # case 'regresa'
    elif codigoOp == 16:
      retDir = self.checkPointer(self.quadruples[self.IP].res)
      memoria, dirOffset, tipoRet = self.getMemory(retDir)
      retVal = memoria[dirOffset]

      leftOp = self.quadruples[self.IP].leftOp
      memoria, dirOffset, tipoFunc = self.getMemory(leftOp)
      if tipoRet == tipoFunc:
        memoria[dirOffset] = retVal
        ip = self.IPatCall.pop()
        self.IP = ip
        memLocal = self.memLocal
        memLocalTemp = self.memLocalTemp
        del memLocal
        del memLocalTemp
        self.pilaFunciones.pop()
        self.memLocal = self.pilaFunciones.top()[0]
        self.memLocalTemp = self.pilaFunciones.top()[1]
      else:
        raise TypeError(f'Func {self.currFunc} is returning {tipoRet} instead of {tipoFunc}')
    # case 'ver'
    elif codigoOp == 24:
      leftOp = self.checkPointer(self.quadruples[self.IP].leftOp)
      memoria, dirOffset, _ = self.getMemory(leftOp)
      valor = int(memoria[dirOffset])

      res = self.quadruples[self.IP].res
      memoria, dirOffset, _ = self.getMemory(res)
      lim = int(memoria[dirOffset])

      if valor < 0 or valor >= lim:
        raise IndexError(f'Index {valor} out of range')
    # case '?', '¡', '$'
    elif codigoOp == 25 or codigoOp == 26 or codigoOp == 27:
      var = self.quadruples[self.IP].leftOp
      memoria, dirOffset, _ = self.getMemory(var)

      dims = self.quadruples[self.IP].rightOp

      res = self.quadruples[self.IP].res
      memoriaRes, dirOffsetRes, _ = self.getMemory(res)

      size = dims[0] * dims[1]
      temp = [None] * size
      for i in range(0, size):
        temp[i] = memoria[dirOffset+i]

      
      tempMatrix = np.reshape(temp, dims)
      # case '$'
      if codigoOp == 27:
        matrix = np.matrix(tempMatrix, dtype='float')
        det = np.linalg.det(matrix)
        memoriaRes[dirOffsetRes] = det
      else:
        # case '?'
        if codigoOp == 25:
          try:
            matrix = np.matrix(tempMatrix, dtype='float')
            matrixRes = np.linalg.inv(matrix)
          except:
            raise ValueError(f'There`s no inverse for this matrix')
        # case '¡'
        elif codigoOp == 26:
          matrix = np.matrix(tempMatrix)
          matrixRes = matrix.transpose()
        # Push results to memory
        tempRes = matrixRes.A1
        for i in range(0, size):
          memoriaRes[dirOffsetRes+i] = tempRes[i]
        

  def execute(self):
    self.pilaFunciones.push((self.memLocal, self.memLocalTemp))
    while self.IP < len(self.quadruples):
      self.switch(self.quadruples[self.IP].op)
      self.IP += 1
