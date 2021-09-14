# -------------------------------------
#       GRAMÁTICA - FIGHTING!
#--------------------------------------

import ply.lex as lex
import re
import codecs
import ord
import cys

tokens = [
    #GENERALES
    'ID',
    'COMENTARIO',
    'INT',
    'FLOAT',
    'CHAR',
    'STRING',
    'ARRAY'

    #OPERADORES
    'PUNTO_Y_COMA',

    'CORCHETEA',
    'CORCHETEC',

    'PARENTESISA',

    'PARENTESISC'
    'COMA',
    'MAS',
    'MENOS',
    'ASTERISCO', #ESTE SIRVE PARA MAS COSAS, AWAS
    'DIVIDIDO',
    'PORCENTAJE', #SE LLAMA MODULO PERO ESO NO SE ME VA A QUEDAR
    'IGUAL',
    'ELEVADO',

    'MAYORQUE',
    'MENORQUE',
    'MAYORIWAL',
    'MENORIWAL',
    'IWALIWAL',
    'DISTINTOQUE',

    'PR_OR',
    'PR_AND',
    'PR_NOT',

    'COMILLASDOBLES',
    'COMILLASSIMPLES',

    'DOLAR',

    'DOS_DOSPUNTOS' 
]

reservadas = {
    #RESERVADAS
    'PR_NOTHING' : 'nothing',
    'PR_TRUE' : 'true',
    'PR_FALSE': 'false',

    'PR_STRUCT': 'struct',
    'PR_MUTABLE': 'mutable',

    'PR_PARSE': 'parse',
    'PR_TRUNC': 'trunc',
    'PR_FLOAT_MIN': 'float',
    'PR_STRING_MIN': 'string',
    'PR_TYPEOF': 'typeof',
    
    'PR_PUSH': 'push',
    'PR_POP': 'pop',
    'PR_LENGTH': 'length',

    'PR_UPPERCASE': 'uppercase',
    'PR_LOWERCASE': 'lowercase',
    'PR_PRINTLN': 'println',
    'PR_PRINT': 'print',

    'PR_LOG10': 'log10',
    'PR_LOG': 'log',
    'PR_SIN': 'sin',
    'PR_COS': 'cos',
    'PR_TAN': 'tan',
    'PR_SQRT': 'sqrt',

    'PR_INT64': 'Int64',
    'PR_FLOAT64': 'Float64',
    'PR_BOOL': 'Bool',
    'PR_CHAR': 'Char',
    'PR_STRING': 'String',

    'PR_GLOBAL': 'global',
    'PR_LOCAL': 'local',

    'PR_FUNCTION': 'function',
    'PR_END': 'end',

    'PR_IF': 'if',
    'PR_ELSEIF': 'elseif',
    'PR_ELSE': 'else',  

    'PR_WHILE': 'while' ,
    
    'PR_FOR': 'for',
    'PR_IN': 'in',
    
    'PR_BREAK': 'break',
    'PR_CONTINUE': 'continue',
    'PR_RETURN': 'return'
}

tokens = tokens + list(reservadas.values())

t_ignore = '\t'