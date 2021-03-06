class Semantics():
  # Semantic Cube
  def __init__(self):
    self.Semantics = {
      # int
      'int' : { 
        # int, mat
        'mat' : {
          '?' : 'float', '$' : 'float', '¡' : 'int'
        },
        # int, int
        'int' : {
        '+' : 'int', '-' : 'int', '*' : 'int', '/' : 'float', '=' : 'int', '&' : 'ERROR', '||': 'ERROR',
        '<' : 'bool', '<=' : 'bool', '>' : 'bool', '>=' : 'bool', '!=' : 'bool', '==' : 'bool'
        },
        # int, float
        'float' : {
          '+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'bool', '<=' : 'bool', '>' : 'bool', '>=' : 'bool', '!=' : 'bool', '==' : 'bool'
        },
        # int, char
        'char' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        },
        # int, bool
        'bool' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        }
      },
      # float
      'float' : {
        # float, mat
        'mat' : {
          '?' : 'float', '$' : 'float', '¡' : 'float'
        },
        # float, int
        'int' : {
        '+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float', '=' : 'float', '&' : 'ERROR', '||': 'ERROR',
        '<' : 'bool', '<=' : 'bool', '>' : 'bool', '>=' : 'bool', '!=' : 'bool', '==' : 'bool'
        },
        # float, float
        'float' : {
          '+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float', '=' : 'float', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'bool', '<=' : 'bool', '>' : 'bool', '>=' : 'bool', '!=' : 'bool', '==' : 'bool'
        },
        # float, char
        'char' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        },
        # float, bool
        'bool' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        }
      },
      # char
      'char' : { 
        # char, mat
        'mat' : {
          '?' : 'ERROR', '$' : 'ERROR', '¡' : 'ERROR'
        },
        # char, int
        'int' : {
        '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
        '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        },
        # char, float
        'float' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        },
        # char, char
        'char' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'char', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'bool', '<=' : 'bool', '>' : 'bool', '>=' : 'bool', '!=' : 'bool', '==' : 'bool'
        },
        # char, bool
        'bool' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        }
      },
      'bool' : { 
        # bool, mat
        'mat' : {
          '?' : 'ERROR', '$' : 'ERROR', '¡' : 'ERROR'
        },
        # bool, int
        'int' : {
        '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
        '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        },
        # bool, float
        'float' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        },
        # bool, char
        'char' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'ERROR', '&' : 'ERROR', '||': 'ERROR',
          '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'ERROR', '==' : 'ERROR'
        },
        # bool, bool
        'bool' : {
          '+' : 'ERROR', '-' : 'ERROR', '*' : 'ERROR', '/' : 'ERROR', '=' : 'bool', '&' : 'bool', '||': 'bool',
          '<' : 'ERROR', '<=' : 'ERROR', '>' : 'ERROR', '>=' : 'ERROR', '!=' : 'bool', '==' : 'bool'
        }
      }
    }

  def get_type(self, leftType, rightType, oper):
    right = rightType
    while type(right) is not str:
      right = rightType[1]
    res = self.Semantics[leftType][right][oper]
    return res

# Testing
# def main():
#   test = Semantics()
#   print(test.get('int', 'char', '+'))

# if __name__=='__main__':
#   main()