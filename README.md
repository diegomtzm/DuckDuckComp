# DuckDuckComp

Desarrollado como proyecto de la clase de Diseño de Compiladores, DuckDuckComp es un compilador para el lenguaje Patito++.

## Manual de Referencia Rápida
### Inicio del programa
Se escribe la palabra reservada Programa y el nombre de programa.
Ej: Programa demo;

Declaración de funciones
Se escribe la palabra reservada funcion seguido del tipo (int, float, char, bool o void), el nombre de la función, los parámetros (o paréntesis vacíos en caso de no tener) y termina con dos puntos (‘:’). En la siguiente línea va la declaración de variables y se abren llaves.
Ej: funcion void llenaMatrizB():
     var int i, j;
     { estatutos de función }

### Declaración de variables
Justo después del inicio del programa o de la declaración de la función se escribe la palabra reservada var seguido del tipo y una lista de ids separados por coma.
Ej: Programa demo;
     var int a, b, c;
          float d, e;

### Variables dimensionadas
Para declarar una variable dimensionada se agregan las casillas con la dimensión en la declaración de variables. Estas pueden ser de 1 o 2 dimensiones.
Ej: var int A[2][2], B[2][3], C[5];

### Función principal
Después de terminar las funciones, se escribe la palabra reservada principal( ) con paréntesis vacíos y se abren llaves.
Ej: principal( ) { estatutos de función principal }

### Comentarios
Se escribe ‘%%’ y lo que queda de esa línea es un comentario.
Ej: var int j; %% variable para llevar como contador

### Asignación
Se tiene una variable ya declarada, el signo de igual ‘=’ y una expresión, terminando con punto y coma ‘;’. Se puede asignar a una variable el valor de una constante, una expresión, el retorno de la llamada a una función e incluso se puede asignar una matriz a otra.
Ej: a = 5; 
     b = a + 2 * 5;
     c = funcion1(a);
     A = B;   %% A y B son variables dimensionadas

### Retorno de una función
Para indicar el valor de retorno en una función, se escribe la palabra reservada regresa seguida del valor que se va a regresar y terminando con punto y coma ‘;’.
Ej: regresa(a);

### Lectura
Se escribe la palabra reservada lee seguida de paréntesis con una lista de variables separadas por coma. Se toma una entrada del usuario para cada una de estas variables.
Ej: lee(a,b,c);

### Escritura
Se escribe la palabra reservada escribe seguida de paréntesis con una lista de expresiones ó strings separados por coma para imprimir en pantalla.
Ej: escribe(“hola mundo”, a, A[0][1]);

### Llamada a función
Se escribe el nombre de la función seguida de los parámetros.
Ej: funcion2(a, b*2);

### Decisión
Para ejecutar algunos estatutos si se cumple una condición se escribe la palabra reservada si seguida de una expresión booleana, la palabra reservada entonces y se abren llaves. Puede llevar un segundo bloque en el que se escribe la palabra reservada sino y se abren llaves nuevamente, para ejecutar ese bloque si la expresión no se cumple.
Ej: si ((x > 5)) entonces {
	estatutos del bloque
      } sino {  estatutos del segundo bloque  }

### Ciclo condicional
Para repetir estatutos mientras se cumpla una condición se escribe la palabra reservada mientras seguido de una expresión booleana, la palabra reservada haz y se abren llaves.
Ej: mientras ((x > 5)) haz { estatutos del bloque }

### Ciclo no condicional
Para repetir estatutos n veces se escribe la palabra reservada desde seguido de una asignación, la palabra reservada hasta, una expresión, la palabra reservada hacer y se abren llaves. El bloque se repite desde el límite inferior hasta el límite superior, inclusivo.
Ej: desde i = 0 hasta n hacer { estatutos del bloque }

### Expresiones
Son las expresiones tradicionales y se pueden utilizar en asignación,como parámetro que se envía a una función, dentro de una casilla de variable dimensionada, en las decisiones y ciclos, en el retorno de una función y en el estatuto escribe.

Operadores aritméticos: +, -, *, /
Operadores de comparación: >, <, >=, <=, ==, !=
Operadores lógicos: &, ||

Operaciones especiales
Se pueden realizar operaciones especiales sobre las matrices. Las operaciones disponibles son la transpuesta (¡), la inversa(?) y el determinante($). Además se pueden realizar sumas, restas y multiplicaciones de matrices, siempre y cuando las dimensiones sean las adecuadas.
Ej: A = B * C + D¡;      %% A, B, C, y D son matrices

### Video Demo 
https://youtu.be/JvdgFl25jXI