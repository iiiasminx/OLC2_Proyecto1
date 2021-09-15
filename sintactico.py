# ----------------------------------------------------------------------------------------------------- 
#---------------------------------------- INICIO SINTÁCTICO -------------------------------------------
# -----------------------------------------------------------------------------------------------------


import ply.yacc as yacc
import os
import codecs
import re 
from gramatica import fighting, tokens
from sys import stdin

#precedencia
precedence = (
    ('left','mas','menos'),
    ('left','asterisco','dividido'),
    ('left', 'elevado'),
    #('right','umenos'), #sujeto a cambios
    ('left', 'parentesisa', 'parentesisc'),    
    )

#expresiones

# INICIO --------------------------------------------------------------------------------------------
def p_inicio(t):
    '''inicio : instrucciones'''
    print("Se super acetpó",  t)

def p_instrucciones(t):
    '''instrucciones : instruccion instrucciones
                     | instruccion '''

def p_instruccion(t):
    '''instruccion  : soperacion
                    | sprint
                    | sasignacion
                    | sfuncion
                    | snativa
                    | sllamada_func
                    | scondicionales
                    | sloops
                    | sstruct'''

def p_scondicionales(t):
    pass

def p_slooops(t):
    pass

def p_sstruct(t):
    pass

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)

def fighting2(texto):
    parser = yacc.yacc()
    result = parser.parse(texto)
    print(result)



#parser = yacc.yacc()
#result = parser.parse('cosas + quepasan')
#print(result)
