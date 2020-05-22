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
      | BOOL
  func: FUNCION t dec_func dec_var* bloque
  t: INT
   | FLOAT
   | CHAR
   | BOOL
   | VOID
  dec_func: func_name "(" params? ")" ":"
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
  asignacion: variable igual expresion fin_asignacion
	fin_asignacion: ";"
	igual: IGUAL
  variable: ID dimn? dimn?
  dimn: "[" expresion "]"
  llamada: llamada_name inicio_llamada params2? fin_llamada
  llamada_name: ID
  inicio_llamada: "("
  fin_llamada: ")"
  params2: params_exp "," params2
      | params_exp
  params_exp: expresion
  retorno: REGRESA "(" retorno_expresion ")" ";"
  retorno_expresion: expresion
  lectura: LEE "(" lista_vars ")" ";"
  lista_vars: lee_variable "," lista_vars
      | lee_variable
  lee_variable: ID dimn? dimn?
  escritura: ESCRIBE "(" salida ")" ";"
  salida: string_salida salida2?
      | expresion_salida salida2?
  salida2: "," salida
  expresion_salida: expresion
  string_salida: STRING
  decision: SI "(" decision_exp ")" ENTONCES bloque sino_bloque?
  decision_exp: expresion
  sino_bloque: sino bloque
  sino: SINO
  rep_cond: mientras "(" expresion ")" haz mientras_bloque
  mientras: MIENTRAS
  haz: HAZ
  mientras_bloque: bloque
  rep_no_cond: DESDE asignacion_desde HASTA expresion hacer desde_bloque
  hacer: HACER
  desde_bloque: bloque
  asignacion_desde: variable_desde igual asignacion_desde_fin
  asignacion_desde_fin: expresion
  variable_desde: ID
  expresion: termino op1?
  op1: adicion expresion
	adicion: ADICION
  termino: factor op2?
  op2: producto termino
	producto: PRODUCTO
  factor: variable op_mat?
      | number
      | llamada
      | open_par exp_logica_or close_par
	open_par: OPENPAR
	close_par: CLOSEPAR
	number: NUMBER
  op_mat: "$"
      | "¡"
      | "?"
  exp_logica_or: exp_logica_and op3?
  op3: "||" exp_logica_or
  exp_logica_and: exp_comp op4?
  op4: "&" exp_logica_and
  exp_comp: full_exp_comp
      | expresion
  full_exp_comp: expresion op_comp expresion
  op_comp: OPCOMP

  PROGRAMA: "Programa"
  PRINCIPAL: "principal"
  VAR: "var"
  INT: "int"
  FLOAT: "float"
  CHAR: "char"
  BOOL: "bool"
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
	ADICION: "+" | "-"
	PRODUCTO: "*" | "/"
  OPCOMP: ">=" | "<=" | "!=" | "==" | ">" | "<"
	IGUAL: "="
	OPENPAR: "("
	CLOSEPAR: ")"
  ID: WORD
  COMMENT: "%%" /(.|\\n|\\r)+/

  %import common.WORD
  %import common.ESCAPED_STRING -> STRING
  %import common.NUMBER
  %import common.WS
  %ignore WS
  %ignore COMMENT
"""