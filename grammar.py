# Diego Martínez A01176489
# Luis Gerardo Bravo A01282014
# Proyecto DuckDuckComp

ld_grammar = r"""
  programa: start dec_var? func* principal "(" ")" bloque
	principal: PRINCIPAL
  start: PROGRAMA ID ";"
  dec_var: VAR dec_var2+
  dec_var2: tipo lista_ids ";"
  lista_ids: id "," lista_ids?
      | id
	id: ID dim? dim?
  dim: "[" NUMBER "]"
  tipo: INT
      | FLOAT
      | CHAR
  func: FUNCION t dec_func dec_var* bloque
  t: INT
   | FLOAT
   | CHAR
   | VOID
  dec_func: func_name "(" params ")" ":"
	func_name: ID
  params: tipo param_name "," params
      | tipo param_name
	param_name: ID
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
  INT: "int"
  FLOAT: "float"
  CHAR: "char"
  VOID: "void"
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
  %import common.WS
  %ignore WS
  %ignore COMMENT
"""