# Diego Martínez A01176489
# Luis Gerardo Bravo A01282014
# Proyecto DuckDuckComp

from lark import Lark

ld_grammar = r"""
	programa: start dec_var? func* PRINCIPAL "(" ")" bloque
  start: PROGRAMA ID ";"
  dec_var: VAR dec_var2+
  dec_var2: tipo lista_ids ";"
  lista_ids: ID dim? dim? "," lista_ids
      | ID dim? dim?
  dim: "[" INT "]"
  tipo: "int"
      | "float"
      | "char"
  func: FUNCION t dec_func dec_var* bloque
  dec_func: ID "(" params ")" ":"
  params: tipo ID "," params
      | tipo ID
  t: tipo
      | "void"
  bloque: "{" estatuto* "}"
  estatuto: asignacion
      | llamada ";"
      | retorno
      | lectura
      | escritura
      | decision
      | rep_cond
      | rep_no_cond
  asignacion: variable "=" expresion ";"
  variable : ID dimn? dimn?
  dimn: "[" expresion "]"
  llamada: ID "(" params2 ")"
  params2: expresion "," params2
      | expresion
  retorno: REGRESA "(" expresion ")" ";"
  lectura: LEE "(" lista_vars ")" ";"
  lista_vars: variable "," lista_vars
      | variable
  escritura: ESCRIBE "(" salida ")" ";"
  salida: STRING salida2?
      | expresion salida2?
  salida2: "," salida
  decision: SI "(" expresion ")" ENTONCES bloque sino?
  sino: SINO bloque
  rep_cond: MIENTRAS "(" expresion ")" HAZ bloque
  rep_no_cond: DESDE variable "=" expresion HASTA expresion HACER bloque
  expresion: termino op1?
  op1: "+" expresion
      | "-" expresion
  termino: factor op2?
  op2: "*" termino
      | "/" termino
  factor: variable op_mat?
      | NUMBER
      | llamada
      | "(" exp_logica_or ")"
  op_mat: "$"
      | "¡"
      | "?"
  exp_logica_or: exp_logica_and op3?
  op3: "||" exp_logica_or
  exp_logica_and: exp_comp op4?
  op4: "&" exp_logica_and
  exp_comp: expresion op5 expresion
      | expresion
  op5: ">"
      | "<"
      | ">="
      | "<="
      | "!="
      | "=="

  PROGRAMA: "Programa"
  PRINCIPAL: "principal"
	VAR: "var"
  FUNCION: "funcion"
  REGRESA: "regresa"
  LEE: "lee"
  ESCRIBE: "escribe"
  SI: "si"
  ENTONCES: "entonces"
  SINO: "sino"
  MIENTRAS: "mientras"
  HAZ: "haz"
  DESDE: "desde"
  HASTA: "hasta"
  HACER: "hacer"
	ID: WORD
  COMMENT: "%%" /(.|\\n|\\r)+/

	%import common.WORD
	%import common.ESCAPED_STRING -> STRING
  %import common.NUMBER
	%import common.INT
	%import common.WS
	%ignore WS
  %ignore COMMENT
"""

little_duck_parser = Lark(ld_grammar, parser="lalr", start="programa")
parse = little_duck_parser.parse

fValid = open("proyecto/program.txt", "r")
validSentence = fValid.read()

validTree = parse(validSentence)

print("\nPROGRAMA\n")
print("---------------------------------------\n")
print(validTree)
print("\n" )
print(validTree.pretty())
