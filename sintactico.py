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
    ('left', 'elevado', 'modulo'),
    ('left','umenos'), #sujeto a cambios
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
    print('instrucciones')

def p_instruccion(t):
    '''instruccion  : soperacion'''
    t[0] = t[1]
    print('creeeo que la respuesta es: ', t[0])

def p_soperacion(t):
    '''soperacion : soperacion mas soperacion
                    | soperacion menos soperacion
                    | soperacion asterisco soperacion
                    | soperacion dividido soperacion
                    | soperacion modulo soperacion
                    | soperacion elevado soperacion'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]
    elif t[2] == '%': t[0] = t[1] % t[3]
    elif t[2] == '^': t[0] = t[1] ** t[3]

def p_soperacionUmenos(t):
    '''soperacion : menos soperacion %prec umenos'''
    t[0] = -t[2]

def p_soperacionPar(t):
    '''soperacion : parentesisa soperacion parentesisc'''
    t[0] = t[2]

def p_soperacionNumeros(t):
    '''soperacion : int
                    | float'''
    t[0] = t[1]

def p_sprint(t):
    pass

def p_sasignacion(t):
    pass

def p_sfuncion(t):
    pass

def p_snativa(t):
    pass

def p_sllamadafunc(t):
    pass

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
