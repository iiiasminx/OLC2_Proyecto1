# -------------------------------------
#       GRAMÁTICA - FIGHTING!
# --------------------------------------

import ply.lex as lex
import re
import codecs
import os
import sys

reservadas = {
    # reservadas
    'nothing': 'NOTHING',
    'true': 'TRUE',
    'false': 'FALSE',

    'struct': 'STRUCT',
    'mutable': 'MUTABLE',

    'parse': 'PARSE',
    'trunc': 'TRUNC',
    'typeof': 'TYPEOF',

    'push': 'PUSH',
    'pop': 'POP',
    'length': 'LENGTH',

    'uppercase': 'UPPERCASE',
    'lowercase': 'LOWERCASE',
    'println': 'PRINTLN',
    'print': 'PRINT',

    'log10': 'LOG10',
    'log': 'LOG',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'sqrt': 'SQRT',

    'int64': 'iNT64',
    'float64': 'fLOAT64',
    'bool': 'bOOL',
    'char': 'cHAR',
    'string': 'sTRING',

    'global': 'GLOBAL',
    'local': 'LOCAL',

    'function': 'FUNCTION',
    'end': 'END',

    'if': 'IF',
    'elseif': 'ELSEIF',
    'else': 'ELSE',

    'while': 'WHILE',

    'for': 'FOR',
    'in': 'IN',

    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN'
}


tokens = [
    # generales
    'id',
    'int',
    'float',
    'char',
    'string',
    'array',

    'comment1',
    'comment2',

    # operadores
    'puntocoma',

    'corchetea',
    'corchetec',

    'parentesisa',

    'parentesisc',
    'coma',
    'mas',
    'menos',
    'asterisco',  # este sirve para mas cosas, awas
    'dividido',
    'porcentaje',  # se llama modulo pero eso no se me va a quedar
    'igual',
    'elevado',

    'mayorque',
    'menorque',
    'mayoriwal',
    'menoriwal',
    'iwaliwal',
    'distintoque',

    'or',
    'and',
    'not',

    'comillasdobles',
    'comillassimples',

    'dolar',

    'dos_dospuntos'
] + list(reservadas.values())


t_ignore = r'\t| '
# operadores
t_puntocoma = r';'

t_corchetea = r'\['
t_corchetec = r'\]'

t_parentesisa = r'\('
t_parentesisc = r'\)'

t_mayorque = r'>'
t_menorque = r'<'
t_mayoriwal = r'>='
t_menoriwal = r'<='
t_iwaliwal = r'=='
t_distintoque = r'!='


t_coma = r'\,'
t_mas = r'\+'
t_menos = r'-'
t_asterisco = r'\*'  # este sirve para mas cosas, awas
t_dividido = r'/'
t_porcentaje = r'%'  # se llama modulo pero eso no se me va a quedar
t_igual = r'='
t_elevado = r'\^'

t_or = r'\|\|'
t_and = r'\&\&'
t_not = r'!'

t_dolar = r'\$'

t_dos_dospuntos = r'::'

def t_id(t):
    r'[a-zA-Z_ñÑ][a-zA-Z0-9_ñÑ]*'
    if t.value.lower() in reservadas:
        t.value = t.value.upper()
        t.type = t.value
        t.value = t.value.lower()
    return t
    

def t_comment1(t):
    r'(\#=).*\n*.*(=\#)'
    pass

def t_comment2(t):
    r'(\#)(.)*(\n)'
    pass

def t_float(t):
    r'([0-9]+\.[0-9]+)'
    t.value = float(t.value)
    return t

def t_int(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_char(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_string(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#creando el analizador léxico 
#EXPORTANDO
def fighting(texto):
    print('Importado con éxito!')
    lexer = lex.lex()
    lexer.input(texto)
    while True:
        tok = lexer.token()
        if not tok : break
        print(tok)
    return 'c\'est finit ' + texto + ':D'


#EXTRAS
# t_array = r'' para sintáctico
