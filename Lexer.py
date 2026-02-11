"""
Lizbeth Andrea Herrera Ortega - 1246024
Marcela Nicole Letran Lee - 1102124

Laboratorio_1 Compiladores
"""

import sys

class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}', Ln:{self.linea}, Col:{self.columna})"

class error_lexico:
    def __init__(self, char, linea, columna):
        self.char = char
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"wrror: caracter desconocido '{self.char}' en la linea {self.linea}, columna {self.columna}"

"""Tipos de tokens"""
TK_PR_HEX='hex' #varhex
TK_PR_OCT='oct' #varoct
TK_PR_BIN='bin' #varbin
TK_OP='operadores'#+ - / * ( )
TH_EB='espacios en blanco' #/n /f ''
TK_ID='ID' #(_ | D | L)^+
TK_VARHEX='varhex' #(D | M)^+
TK_VAROCT='varoct' #N^+
TK_VARBIN='varbin' #(0 | 1)^+
TK_C='comentario' # # (D | L | C)* /n
# tk extra
TK_NUM='var'# agrupa var-bin,oct,hex
TK_I='igual' #=
TK_E='error'


class Scanner:
    def __init__(self, texto_linea, num_linea):
        self.inicial = texto_linea
        self.pos = 0
        self.linea = num_linea
        self.columna = 1

    def generar_tokens(self):
        tokens = []
        while self.pos < len(self.inicial):
            char = self.inicial[self.pos]

            if char.isspace():
                self.pos += 1
                self.columna += 1
                continue

            if char == '#':
                break

            if char in "+-*/()":
                tokens.append(Token(TK_OP, char, self.linea, self.columna))
                self.pos += 1
                self.columna += 1
                continue

            if char == '=':
                tokens.append(Token(TK_I, '=', self.linea, self.columna))
                self.pos += 1
                self.columna += 1
                continue

            #identificadores y Palabras Reservadas
            if char.isalpha() or char == '_':
                inicio_col = self.columna
                lexema = ""
                while self.pos < len(self.inicial) and (self.inicial[self.pos].isalnum() or self.inicial[self.pos] == '_'):
                    lexema += self.inicial[self.pos]
                    self.pos += 1
                    self.columna += 1
                
                if lexema == "hex": tokens.append(Token(TK_PR_HEX, lexema, self.linea, inicio_col))
                elif lexema == "oct": tokens.append(Token(TK_PR_OCT, lexema, self.linea, inicio_col))
                elif lexema == "bin": tokens.append(Token(TK_PR_BIN, lexema, self.linea, inicio_col))
                else: tokens.append(Token(TK_ID, lexema, self.linea, inicio_col))
                continue

            #numeros - digitos
            if char.isdigit():
                inicio_col = self.columna
                lexema = ""
                while self.pos < len(self.inicial) and self.inicial[self.pos].isalnum():
                    lexema += self.inicial[self.pos]
                    self.pos += 1
                    self.columna += 1
                tokens.append(Token(TK_NUM, lexema, self.linea, inicio_col))
                continue

            #error
            tokens.append(Token(TK_E, char, self.linea, self.columna))
            self.pos += 1
            self.columna += 1
        return tokens

#Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.error_token = None

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        self.pos += 1

    #valoidar base
    def es_binario(self, texto): return all(c in "01" for c in texto)
    def es_octal(self, texto): return all(c in "01234567" for c in texto)
    def es_hex(self, texto): return all(c in "0123456789ABCDEFabcdef" for c in texto)

    def parse(self):
        if not self.tokens:
            return True
        
        #errores léxicos
        for t in self.tokens:
            if t.tipo == TK_E:
                self.error_token = t
                return False

        if self.S() and self.pos == len(self.tokens):
            return True
        
        #errores sintácticos
        if self.error_token is None:
            self.error_token = self.current()
        return False

    def S(self):
        """ S -> tipo ID = Expresion """
        t = self.current()
        if t and t.tipo in [TK_PR_HEX, TK_PR_OCT, TK_PR_BIN]:
            tipo_base = t.tipo
            self.consume()
            if self.current() and self.current().tipo == TK_ID:
                self.consume()
                if self.current() and self.current().tipo == TK_I:
                    self.consume()
                    return self.O(tipo_base) # Pasa a la expresión matemática
        return False

    def O(self, base):
        """ O -> T ( (+|-) T )* """
        if not self.T(base): return False
        while self.current() and self.current().valor in ('+', '-'):
            self.consume()
            if not self.T(base): return False
        return True

    def T(self, base):
        """ T -> F ( (*|/) F )* """
        if not self.F(base): return False
        while self.current() and self.current().valor in ('*', '/'):
            self.consume()
            if not self.F(base): return False
        return True

    def F(self, base):
        """ F -> ( O ) | NUM | ID """
        t = self.current()
        if not t: return False

        if t.valor == '(':
            self.consume()
            if not self.O(base): return False
            if self.current() and self.current().valor == ')':
                self.consume()
                return True
            return False

        if t.tipo == TK_NUM:
            valido = False
            if base == TK_PR_BIN: valido = self.es_binario(t.valor)
            elif base == TK_PR_OCT: valido = self.es_octal(t.valor)
            elif base == TK_PR_HEX: valido = self.es_hex(t.valor)
            
            if valido:
                self.consume()
                return True
            return False

        if t.tipo == TK_ID:
            self.consume()
            return True

        return False

#manejo de archivos
def ejecutar(nombre_entrada, nombre_salida):
    try:
        with open(nombre_entrada, 'r') as f:
            lineas = f.readlines()
        
        resultados = []
        for i, texto in enumerate(lineas, 1):
            linea_contenido = texto.strip()
            if not linea_contenido: continue
            
            sc = Scanner(linea_contenido, i)
            tks = sc.generar_tokens()
            ps = Parser(tks)
            
            if ps.parse():
                #ACEPTADA
                resultados.append(f"linea {i}= ACEPTADA: {linea_contenido}")
            else:
                t = ps.error_token
                fila = t.linea if t else i
                col = t.columna if t else len(linea_contenido) + 1
                char = t.valor if t else ''
                
                #RECHAZADA
                mensaje = f"linea {i}= RECHAZADA: {linea_contenido}\n   fila: {fila}, columna: {col}, caracter: {char}"
                resultados.append(mensaje)
        
        with open(nombre_salida, 'w') as f:
            f.write("\n".join(resultados))
        print(f"Resultados en: {nombre_salida}")

    except FileNotFoundError:
        print(f"no se encontro el archivo '{nombre_entrada}'")

ejecutar('entrada.txt', 'resultado.txt')
