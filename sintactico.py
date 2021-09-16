# ----------------------------------------------------------------------------------------------------- 
#---------------------------------------- INICIO SINTÁCTICO -------------------------------------------
# -----------------------------------------------------------------------------------------------------


import ply.yacc as yacc
import os
import codecs
import re 
from gramatica import fighting, tokens
from cst import NodoSimbolo, NodoError, Exporte #Falta el AST cuando entienda que pex xdxd
from sys import stdin
import math

global impresion
impresion = ""

#precedencia
precedence = (
    ('left','mas','menos'),
    ('left','asterisco','dividido'),
    ('left', 'elevado', 'modulo'),
    ('left','umenos'), #sujeto a cambios
    ('left', 'and', 'or'),
    ('left','not'),
    ('left','mayorque','mayoriwal', 'menorque', 'menoriwal', 'iwaliwal', 'distintoque'),
    ('left', 'parentesisa', 'parentesisc'),    
    )

#expresiones

#  ------------------------------------------INICIO--------------------------------------------------
#----------------------------------------------------------------------------------------------------
def p_inicio(t):
    '''INICIO : INSTRUCCIONES'''
    print("Se super acetpó",  t)

def p_instrucciones(t):
    '''INSTRUCCIONES : INSTRUCCION INSTRUCCIONES
                     | INSTRUCCION 
                     | '''

def p_instruccion(t):
    '''INSTRUCCION  : SOPERACIONES
                    | IMPRIMIR
                    | FUNCIONES'''    

def p_soperaciones(t):
    '''SOPERACIONES : SOPERACION
                    | SOPSTRING
                    | SOPNATIV
                    | SOPLOG'''
    t[0] = t[1]
    print('creeeo que la respuesta es: ', t[0])

def p_subinstrucciones(t):
    '''SUBINSTRUCCIONES : SUBINSTRUCCION SUBINSTRUCCIONES
                     | SUBINSTRUCCION 
                     | '''

def p_subinstruccion(t):
    '''SUBINSTRUCCION  : SOPERACIONES
                        | IMPRIMIR
                        | FUNCIONES'''  
#  ---------------------------------FUNCIONES---------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_funciones(t):
    '''FUNCIONES : FIF'''

def p_fif(t):
    '''FIF : if SOPLOG SUBINSTRUCCIONES FELSEIF
            | if SOPLOG SUBINSTRUCCIONES FELSE
            | if SOPLOG SUBINSTRUCCIONES end puntocoma''' # Podría poner un bool de dentro if ejecute, si no no xd

def p_felseif(t):
    '''FELSEIF : elseif SOPLOG SUBINSTRUCCIONES FELSEIF
            | elseif SOPLOG SUBINSTRUCCIONES FELSE
            | elseif SOPLOG SUBINSTRUCCIONES end puntocoma'''
        
def p_felse(t):
    '''FELSE : else SUBINSTRUCCIONES end puntocoma'''
#  ---------------------------------IMPRIMIR----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sprint(t):
    '''IMPRIMIR : println parentesisa SCONTPRNT parentesisc puntocoma
                | print parentesisa SCONTPRNT parentesisc puntocoma''' 
    if t[1] == 'println'  : t[0] = str(t[3]) + "\n"
    elif t[1] == 'print': t[0] = str(t[3])               
    paraImprimir(t[0])

def p_scontprint(t):
    '''SCONTPRNT : SCONTPRNT coma SCONTPRNT'''
    t[0] = str(t[1]) + str(t[3])

def p_scontprintterm(t):
    '''SCONTPRNT : cadena
                | caracter
                | SOPERACIONES'''
    t[0] = t[1]

#------------------------------OPERACIONES LOGICAS----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_soplog(t):
    '''SOPLOG : SOPLOG and SOPLOG
            | SOPLOG or SOPLOG
            | SOPLOG mayorque SOPLOG
            | SOPLOG menorque SOPLOG
            | SOPLOG mayoriwal SOPLOG
            | SOPLOG menoriwal SOPLOG
            | SOPLOG iwaliwal SOPLOG
            | SOPLOG distintoque SOPLOG'''
    if t[2] == '&&'  : t[0] = t[1] and t[3]
    elif t[2] == '||': t[0] = t[1] or t[3] 
    elif t[2] == '<': t[0] = t[1] < t[3] 
    elif t[2] == '<=': t[0] = t[1] <= t[3] 
    elif t[2] == '>': t[0] = t[1] > t[3] 
    elif t[2] == '>=': t[0] = t[1] >= t[3] 
    elif t[2] == '==': t[0] = t[1] == t[3] 
    elif t[2] == '!=': t[0] = t[1] != t[3]   

def p_soplogPar(t):
    '''SOPLOG : parentesisa SOPLOG parentesisc'''
    t[0] = t[2]


def p_soplogterm(t):
    '''SOPLOG : true
            | false
            | int
            | float
            | cadena
            | caracter
            | SOPERACION'''
    t[0] = t[1]
            

#------------------------------OPERACIONES NATIVAS----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sopnativ(t):
    '''SOPNATIV : uppercase parentesisa SOPN parentesisc
                | lowercase parentesisa SOPN parentesisc'''
    if t[1] == 'uppercase'  : t[0] = str(t[3]).upper()
    elif t[1] == 'lowercase'  : t[0] = str(t[3]).lower()

def p_sopnativterm(t):
    ''' SOPN : cadena
            | caracter'''
    t[0] = t[1]

#------------------------------OPERACIONES STRING ----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sopstring(t):
    '''SOPSTRING : SOPSTRING asterisco SOPSTRING
                | SOPSTRING elevado int'''
    if t[2] == '*'  : t[0] = t[1] + t[3]
    elif t[2] == '^': 
        t[0] = ""
        copia = t[1]
        number = 0
        while  number < t[3]:
            t[0] = t[0] + copia
            number = number +1

def p_sopstringterm(t):
    '''SOPSTRING : cadena
                | caracter'''
    t[0] = t[1]

#  ----------------------------OPERACIONES NUMÉRICAS--------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def p_soperacion(t):
    '''SOPERACION : SOPERACION mas SOPERACION
                    | SOPERACION menos SOPERACION
                    | SOPERACION asterisco SOPERACION
                    | SOPERACION dividido SOPERACION
                    | SOPERACION modulo SOPERACION
                    | SOPERACION elevado SOPERACION'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]
    elif t[2] == '%': t[0] = t[1] % t[3]
    elif t[2] == '^': t[0] = t[1] ** t[3]

def p_soperacionUmenos(t):
    '''SOPERACION : menos SOPERACION %prec umenos'''
    t[0] = -t[2]

def p_soperacionPar(t):
    '''SOPERACION : parentesisa SOPERACION parentesisc'''
    t[0] = t[2]

def p_soperacionMath(t):
    '''SOPERACION : NATMATH parentesisa SOPERACION parentesisc'''
    if t[1] == 'log10': t[0] = math.log10(t[3])
    elif t[1] == 'sin': t[0] = math.sin(t[3])
    elif t[1] == 'cos': t[0] = math.cos(t[3])
    elif t[1] == 'tan': t[0] = math.tan(t[3])
    elif t[1] == 'sqrt': t[0] = math.sqrt(t[3])

def p_soperacionlog(t):
    '''SOPERACION : log parentesisa SOPERACION coma SOPERACION parentesisc'''
    t[0] = math.log(t[3], t[5])
    
def p_soperacionNumeros(t):
    '''SOPERACION : int
                    | float'''
    t[0] = t[1]

def p_nathmath(t):
    '''NATMATH : log10
                | sin
                | cos
                | tan
                | sqrt '''
    t[0] = t[1]








def p_sasignacion(t):
    pass

def p_sfuncion(t):
    pass

def p_snativa(t):
    pass

def p_sllamadafunc(t):
    pass

def p_sstruct(t):
    pass

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)


#  ----------------------------------------- OTROS --------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def fighting2(texto):
    global impresion 
    impresion = ''
    paraImprimir('cosas que se imprimen -------------------------------------------------------\n')

    parser = yacc.yacc()
    result = parser.parse(texto)
    #print(impresion)
    return impresion

def paraImprimir(texto):
    global impresion 
    impresion += texto


#fighting('uppercase()')
#parser = yacc.yacc()
#result = parser.parse('uppercase()')
#print(result)
