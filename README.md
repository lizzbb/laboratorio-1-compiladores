# Análisis Léxico y GLC
*Laboratorio 1 - Compiladores* \n
Lizbeth Andrea Herrera Ortega - 1246024
Marcela Nicole Letran Lee - 1102124

# Diseño de Grámatica
Estado Inicial: { S } 
Terminales: {hex, oct, bin, varhex, varbin, varoct, id, operadores} 
No Terminales: {S, T, F, O, D} 
Producciones: {
  S → DO 
  D → hex id = varhex | oct id = varoct | bin id = varbin 
  O → O+T | O-T | T 
  T → T*F | T/F | F 
  F → ( O ) | varhex | varoct | varbin
}

# Diseño de Tokens (Expresiones Regulares)
   *D = digitos del 0-9
   L = letras de A-Z, mayusculas y minusculas 
   M = letras A-F, mayusculas
   N = digitos del 0-7
   C = caracteres especiales*
- - - - - - - - - - - - - - - - - - - - - - - 
Palabras Reservadas
  hex -> "varhex"
  oct -> "varoct"
  bin -> "varbin"
  
operadores -> '+', '-', '/', '*', '(', ')' 
espacios en blanco -> "/n", "/f", ' '
comentario -> (D | L | C)*"/n"

id -> ( _ | D | L )⁺
varhex -> (D | M)⁺
varoct -> N⁺
varbin -> (0 | 1)⁺ 
igual -> '='
error 

# Manejo de errores
Por medio de un token designado 'error', se guarda todo aquello que no es aceptado por las expresiones regulares y la gramática libre de contexto. Se almacena el caracter no soportado, número de línera y número de columna donde se encontró sin interrumpir la ejecución del programa. Al finalizar, se muestran los errores con la información almacenada, y se determina si la cadena fue aceptada o no. 
