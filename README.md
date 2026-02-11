# Análisis Léxico y GLC
*Laboratorio 1 - Compiladores*  
Lizbeth Andrea Herrera Ortega - 1246024  
Marcela Nicole Letran Lee - 1102124  

# Diseño de Grámatica
Estado Inicial: { S }  
Terminales: {hex, oct, bin, varhex, varbin, varoct, id, operadores}  
No Terminales: {S, T, F, O, D}  
Producciones: {  
&nbsp; &nbsp; S → DO   
&nbsp; &nbsp; D → hex id = varhex | oct id = varoct | bin id = varbin   
&nbsp; &nbsp; O → O+T | O-T | T   
&nbsp; &nbsp; T → T*F | T/F | F  
&nbsp; &nbsp; F → ( O ) | varhex | varoct | varbin  
}  

# Diseño de Tokens (Expresiones Regulares)
   *D = digitos del 0-9  
   L = letras de A-Z, mayusculas y minusculas  
   M = letras A-F, mayusculas  
   N = digitos del 0-7  
   C = caracteres especiales*  
- - - - - - - - - - - - - - - - - - - - - - - 
Palabras Reservadas  
&nbsp; &nbsp; hex -> "varhex"  
&nbsp; &nbsp; oct -> "varoct"  
&nbsp; &nbsp; bin -> "varbin"  
    
operadores -> '+', '-', '/', '*', '(', ')'   
espacios en blanco -> "/n", "/f", ' '  
comentario -> (D | L | C)* *"/n"  
  
id -> ( _ | D | L )⁺  
varhex -> (D | M)⁺  
varoct -> N⁺  
varbin -> (0 | 1)⁺  
igual -> '='  
error  

# Manejo de errores
Los errores se manejan bajo dos escenarios, durante el análisis léxico y el análisis sintáctico; primero validando que los símbolos pertenezcan al lenguaje, y después que estén organizados correctamente.
1. Manejo de Error Léxico (Tokenización)
El primer filtro se da en el Scanner, validando el alfabeto del lenguaje 
•	En lugar de detener la ejecución al encontrar un carácter desconocido, si el caracter leído no coincide con ninguna expresión regular, se tokeniza como TK_E (token de error)
•	Al crear el token de error en el momento de la lectura, se guardan las coordenadas (fila, columna); indicando dónde se dejó de reconocer el alfabeto antes de intentar cualquier análisis gramatical.
2. Manejo de Error Sintáctico (GR)
Una vez generada la lista de tokens, el Parser valida la estructura lógica utilizando reglas de producción 
•	Validación del cumplimiento de la gramática. Se intenta construir el árbol de derivación, si en algún punto el token actual no cumple la regla de producción esperada se retorna False
•	Se captura el token del error cuando la derivación gramatical se rompe, se almacena el token actual rechazando la cadena no porque sea caracteres inválidos, sino porque la secuencia de tokens no pertenece al lenguaje generado por la gramática.
•	Si un token numérico no cumple con la base declarada (hex, oct, bin), se trata como un error de sintaxis, rechazando la producción, validando que se reconozca el formato

