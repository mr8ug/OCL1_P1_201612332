#gramatica
import re
from parser.Excepcion import Excepcion

from parser.Tipo import OperadorAritmetico, OperadorLogico, OperadorRelacional, TIPO

from abstract.Instruccion import Instruccion

from expresiones.Aritmetica import Aritmetica
from expresiones.Relacional import Relacional
from expresiones.Logica import Logica
from expresiones.Identificador import Identificador
from expresiones.Primitivos import Primitivos

from instrucciones.Imprimir import Imprimir
from instrucciones.Declaracion import Declaracion
from instrucciones.Asignacion import Asignacion





#errores
errores=[]

#palabras reservadas
reservadas={
    'int'   : 'RINT',
    'double' : 'RDOUBLE',
    'string': 'RSTRING',
    'boolean': 'RBOOLEAN',
    'char':'RCHAR',
    'null':'RNULL',
    'print':'RPRINT',
    'var':'RVAR' ,
    'func':'RFUNC'
    
}

#definicion de tokens
tokens  = [
    'PUNTOCOMA',
    'PARA',
    'PARC',
    'MAS',
    'MENOS',
    'MENORQUE',
    'MAYORQUE',
    'IGUALIGUAL',
    'AND',
    'OR',
    'NOT',

    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID'
] + list(reservadas.values())

# cadenas de los tokens
t_PUNTOCOMA     = r';'
t_PARA          = r'\('
t_PARC          = r'\)'


t_MAS           = r'\+'
t_MENOS         = r'-'
t_POR           = r'\*'
t_DIV           = r'\/'
t_MOD           = r'%'
t_POT           = r'^'


t_MENORQUE      = r'<'
t_MAYORQUE      = r'>'
t_IGUALIGUAL    = r'=='
t_MENORIGUAL    = r'<='
t_MATORIGUAL    = r'>='
t_DIFERENTE     = r'!='


t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'(not)|(NOT)'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d",t.value)
        t.value=0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value=int(t.value)
    except ValueError:
        print("Integer value too large %d",t.value)
        t.value=0
    return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

    # Caracteres ignorados
t_ignore = " \t"

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

def t_COMENTARIO_MULTI(t):
    r'\#[\s\S]*?\*\#'

def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico." + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)


#encontrar columna
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

import ply.lex as lex
lexer = lex.lex(reflags= re.IGNORECASE, debug=False)

# Asociación de operadores y precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('right','UNOT'),
    ('left','MENORQUE','MAYORQUE', 'IGUALIGUAL'),
    ('left','MAS','MENOS'),
    ('right','UMENOS'),
    )


def p_init(t):
    'init : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t):
    'instrucciones : instrucciones instruccion'
    if t[1] == "":
        t[0]=[]
    else:
        t[0]=[t[1]]

def p_instruccion(t):
    '''instruccion : imprimir_instr finins
                    | declaracion_instr finins
                    | asignacion_instr finins
                    | if_instr'''

    t[0]=t[1]

def p_finins(t):
    '''finins   :   PUNTOCOMA
                | '''
    t[0]=""

def p_imprimir(t) :
    'imprimir_instr     : RPRINT PARA expresion PARC'
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))


def p_declaracion(t):
    'declaracion_instr      : RVAR ID IGUAL expresion'
    t[0] = Declaracion(t[1],t[2], t.lineno(2), find_column(input,t.slice[2]),t[4])

def p_asignacion(t):
    'asignacion_instr       : ID IGUAL expresion'
    t[0] = Asignacion(t[1],t[3], t.lineno(1), find_column(input,t.slice[1]))

def p_tipo(t):
    '''tipo     : RINT
                | RDOUBLE
                | RSTRING
                | RBOOLEAN
                | RCHAR '''
    if t[1] == 'int':
        t[0]= TIPO.ENTERO
    elif t[1] == 'float':
        t[0] = TIPO.DECIMAL
    elif t[1] == 'string':
        t[0] = TIPO.CADENA
    elif t[1] == 'boolean':
        t[0] = TIPO.BOOLEANO

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion DIV expresion
            | expresion MOD expresion

            | expresion MENORQUE expresion
            | expresion MAYORQUE expresion
            | expresion IGUALQUE expresion
            | expresion MENORQUE expresion
            | expresion MENORQUE expresion

            | expresion AND expresion
            | expresion OR expresion
            | expresion NOT expresion
    '''
    #expresiones aritmeticas suma, resta, mult, div, modulo
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS,t[1], t[3], t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] =='-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1],t[3], t.lineno(2), find_column(input,t.slice[2]))
    
    elif t[2] == '/':
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1],t[3], t.lineno(2), find_column(input,t.slice[2]))
    
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.MOD, t[1],t[3], t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '^':
        t[0] = Aritmetica(OperadorAritmetico.POT, t[1],t[3], t.lineno(2), find_column(input,t.slice[2]))

    #expresiones relacionales mayor, menor, mayor que, menor que, igual, diferente   
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!=':
        t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))

    #expresiones logicas and, or
    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == 'not' or t[2] == 'NOT':
        t[0] = Logica(OperadorLogico.NOT, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    
    

    def p_expresion_unaria(t):
        '''
        expresion : MENOS expresion %prec UMENOS
                | NOT expresion %pre UNOT
        '''

        if t[1] == '-':
            t[0]= Aritmetica(OperadorAritmetico.UMENOS, t[2], None, t.lineno(1), find_column(input, t.slice[1]))
        elif t[1] =='!':
            t[0] = Logica (OperadorLogico.NOT, t[2], None, t.lineno(1), find_column(input, t.slice[1]))

    def p_expresion_agrupacion(t):
        '''
        expresion : MENOS expresion %prec UMENOS
                | NOT expresion %prec UNOT
        '''
        t[0] = t[2]

    def p_expresion_identificador(t):
        '''expresion : ID'''
        t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

    def p_expresion_entero(t):
        '''expresion : ENTERO'''
        t[0] = Primitivos(TIPO.ENTERO,t[1], t.lineno(1), find_column(input, t.slice[1]))

    def p_primitivo_decimal(t):
        '''expresion : DECIMAL'''
        t[0] = Primitivos(TIPO.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))

    def p_primitivo_cadena(t):
        '''expresion : CADENA'''
        t[0] = Primitivos(TIPO.CADENA,str(t[1]).replace('\\n', '\n'), t.lineno(1), find_column(input, t.slice[1]))

    def p_primitivo_true(t):
        '''expresion : RTRUE'''
        t[0] = Primitivos(TIPO.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))

    def p_primitivo_false(t):
        '''expresion : RFALSE'''
        t[0] = Primitivos(TIPO.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))

    ###aplicar YACC

    import ply.yacc as yacc
    parser = yacc.yacc()

    input = ''

    def getErrores():
        return errores

    def parse(i):
        global errores
        global lexer
        global parser

        errores=[]
        lexer = lex.lex(reflags=re.IGNORECASE)
        parser = yacc.yacc()
        global input
        input = i
        return parser.parse(i)

    
    #interfaz

    f = open("./entrada.txt", "r")
    entrada = f.read()

    from parser.Arbol import Arbol
    from parser.TablaSimbolos import TablaSimbolos

    instrucciones = parse(entrada.lower())

    ast = Arbol(instrucciones)
    tablaSimboloGlobal=TablaSimbolos()
    ast.setTSglobal(tablaSimboloGlobal)

    for error in errores:
        ast.getExcepciones().append(error)
        ast.updateConsola(error.toString())

    for instruccion in ast.getInstrucciones():
        value = instrucciones.interpreter(ast,tablaSimboloGlobal)
        if isinstance(value,Excepcion):
            ast.getExcepciones().append(value)
            ast.updateConsola(value.toString())

    print(ast.getConsola())
    

                
