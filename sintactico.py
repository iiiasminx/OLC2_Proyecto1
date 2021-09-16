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
global listaErrores
listaErrores = []
global listaSimbolos
listaSimbolos = []

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
                     | INSTRUCCION'''

def p_instruccion(t):
    '''INSTRUCCION  :  IMPRIMIR
                    | FUNCIONES
                    | SCOPE
                    | DECLFUNC'''    

def p_soperaciones(t):
    '''SOPERACIONES : SOPERACION
                    | SOPSTRING
                    | SOPNATIV
                    | SOPLOG'''
    t[0] = t[1]
    print('creeeo que la respuesta es: ', t[0])

#  ------------------------------------FUNCIONES------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_declfunc(t):
    '''DECLFUNC : function id parentesisa PARAMS parentesisc INSTRUCCIONES end puntocoma'''
    print('LO DE ARRIBA ERA UNA FUNCION')

def p_params(t):
    '''PARAMS : PARAMS coma id
            | id 
            | '''
#  ---------------------------------ASIGNACIONES------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sope(t):
    '''SCOPE : global ASIGNACION
            | local ASIGNACION
            | ASIGNACION'''
    t[0] = t[1]
    if t[1] == 'global'  : print('SCOPE EN EL ANTERIOR')
    elif t[1] == 'local'  : print('SCOPE EN EL ANTERIOR')
    

#cualquiera

def p_asignaciones(t):
    '''ASIGNACION : id igual SOPLOG puntocoma'''
    print('ASIGNACION CUALQUIERA --', t[3])

def p_asignaciones2(t):
    '''ASIGNACION : id igual SOPLOG dos_dospuntos string puntocoma
                | id igual SOPLOG dos_dospuntos char puntocoma
                | id igual SOPLOG dos_dospuntos bool puntocoma
                | id igual SOPLOG dos_dospuntos float64 puntocoma
                | id igual SOPLOG dos_dospuntos int64 puntocoma''' 
    print('ASIGNACION CUALQUIERA: ', t[5])

#string 

def p_asignaciones3(t):
    '''ASIGNACION : id igual SOPSTRING puntocoma
                | id igual SOPSTRING  dos_dospuntos string puntocoma
                | id igual SOPSTRING  dos_dospuntos char puntocoma'''
    print('ASIGNACION STRING ' + t[3])

#nothing

def p_asignaciones4(t):
    '''ASIGNACION : id igual nothing puntocoma'''
    print('ASIGNACION NOTHING --', t[3])

#  ---------------------------------FUNCIONES---------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_funciones(t):
    '''FUNCIONES : FIF'''

#  -------------------------------------- IF ---------------------------------------------------------

#  -------------------------------------- IF ---------------------------------------------------------

def p_fif(t):
    '''FIF : if SOPLOG INSTRUCCIONES FELSEIF
            | if SOPLOG INSTRUCCIONES FELSE
            | if SOPLOG INSTRUCCIONES end puntocoma''' 
    print('IF 1')

def p_felseif(t):
    '''FELSEIF : elseif SOPLOG INSTRUCCIONES FELSEIF
            | elseif SOPLOG INSTRUCCIONES FELSE
            | elseif SOPLOG INSTRUCCIONES end puntocoma'''
    print('ELSEIF 1')
        
def p_felse(t):
    '''FELSE : else INSTRUCCIONES end puntocoma'''
    print('ELSE 1')



# *********************************************************************************************************
# *********************************************************************************************************
# ****************************  A PARTIR DE ACÁ ESTA EL COSO CON TODO Y PARSER ****************************
# *********************************************************************************************************
# *********************************************************************************************************

#  ---------------------------------IMPRIMIR----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sprint(t):
    '''IMPRIMIR : println parentesisa SCONTPRNT parentesisc puntocoma
                | print parentesisa SCONTPRNT parentesisc puntocoma'''
    print('IMPRIMIR 1')

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
                | caracter
                | SOPNATIV'''
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


#  --------------------------------------- ERRORES --------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def p_error(t):
    try: 
        desc = 'Error sintáctico con ' + t.value
        error1 = NodoError(desc, t.lineno, t.lexpos)
        listaErrores.append(error1)
        print("Error sintáctico en '%s'" % t.value)
    except:
        print('Algo pasó en el error :c')


#  ----------------------------------------- OTROS --------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def fighting2(texto):
    #asignaciones iniciales
    global impresion 
    impresion = ''
    global listaErrores
    listaErrores = []
    paraImprimir('cosas que se imprimen -------------------------------------------------------\n')

    parser = yacc.yacc()
    result = parser.parse(texto)
    
    for i in listaErrores:
        print(i.descripcion, ' ', i.fila, ' ', i.columna, ' ', i.fecha)

    return impresion

def paraImprimir(texto):
    global impresion 
    impresion += texto


#fighting('uppercase()')
#parser = yacc.yacc()
#result = parser.parse('uppercase()')
#print(result)
