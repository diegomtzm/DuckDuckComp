# Espacios de memoria virtual para variables globales
dvig = 1000
dvfg = 4000
dvcg = 7000
dvbg = 9000

# Espacios de memoria virtual para temporales globales
dvigt = 50000
dvfgt = 52000
dvcgt = 54000
dvbgt = 56000

# Espacios de memoria virtual para variables locales
dvil = 10000
dvfl = 13000
dvcl = 16000
dvbl = 18000

# Espacios de memoria virtual para temporales locales
dvilt = 58000
dvflt = 60000
dvclt = 62000
dvblt = 64000

# Espacios de memoria virtual para constantes
dvcte = 66000

dirVirtual = {}
dirVirtual['global'] = {
  'int': dvig,
  'float': dvfg,
  'char': dvcg,
  'bool': dvbg
}
dirVirtual['globalTemp'] = {
  'int': dvigt,
  'float': dvfgt,
  'char': dvcgt,
  'bool': dvbgt
}
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

tablaCtes = {}

tablaOperadores = {
  "+": 1, "-": 2, "*": 3, "/": 4, "=": 5, "<=": 6, ">=": 7, ">": 8, "<": 9, 
  "!=": 10, "==": 11, "&": 12, "||": 13, "lee": 14, "escribe": 15, "regresa": 16,
  "goTo": 17, "goToF": 18, "endFunc": 19, "end": 20, "era": 21, "param": 22, "goSub": 23
}

def getNewDirV(varType, scope):
  dirV = dirVirtual[scope][varType]
  dirVirtual[scope][varType] += 1
  return dirV