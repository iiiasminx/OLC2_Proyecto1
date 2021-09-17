# ----------------------------------------------------------------------------------------------------- 
#---------------------------------------- INICIO SINTÁCTICO -------------------------------------------
# -----------------------------------------------------------------------------------------------------


import ply.yacc as yacc
import os
import codecs
import re 
from gramatica import fighting, tokens
from cst import NodoSimbolo, NodoError, Exporte, GrafoCST #Falta el AST cuando entienda que pex xdxd
from sys import stdin
import math

global impresion
impresion = ""
global listaErrores
listaErrores = []
global listaSimbolos
listaSimbolos = []
global contaerrores
contaerrores = 0

grafo = GrafoCST()

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
    #print("Se super acetpó",  t)

def p_instrucciones(t):
    '''INSTRUCCIONES : INSTRUCCION INSTRUCCIONES
                     | INSTRUCCION'''

def p_instruccion(t):
    '''INSTRUCCION  :  IMPRIMIR
                    | FUNCIONES
                    | SCOPE
                    | DECLFUNC
                    | LLAMADAFUNC
                    | TRANSF
                    | TYPESTRUCT
                    | LLAMADARR
                    | STRUCTINI
                    | SOPERACIONES'''  #este ultimo es temporal
    grafo.generarPadre(1)

def p_soperaciones(t):
    '''SOPERACIONES : SOPSTRING
                    | SOPNATIV
                    | SOPERACION
                    | SOPLOG
                    | DECLNATIV'''
    t[0] = t[1]
    

#  ----------------------------------------TIPOS------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_tipos(t):
    '''TIPOS : int64
            | float64
            | bool
            | char
            | string'''
    t[0] = t[1]

def p_algo(t):
    '''ALGO : SOPERACIONES
            | STRUCTASIGN
            | id
            | ARREGLO
            | LLAMADARR
            | STRUCTINI'''
    t[0] = t[1]
    #print('creeeo que la respuesta es: ', t[0])

#  -------------------------------------- STRUCT------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_typestruct(t):
    '''TYPESTRUCT : mutable STRUCT
                    | STRUCT'''
    #print('Esto termina un struct')

def p_struct(t):
    '''STRUCT : struct id ATRIBUTOS end puntocoma'''

def p_atributos(t):
    '''ATRIBUTOS : ATRIBUTO ATRIBUTOS
                | ATRIBUTO '''

def p_atributo(t):
    '''ATRIBUTO : id dos_dospuntos TIPOS puntocoma
                | id puntocoma'''
    #print('atributo: ', t[1])

def p_creacionstruct(t):
    '''STRUCTINI : id parentesisa PARAMSFUNC parentesisc'''
    #print('ESTOY INICIANDO UN STRUCT')

def p_structasign(t):
    '''STRUCTASIGN : id punto id'''
    t[0] = t[1] + t[2] + t[3]
#  ------------------------------------ ARREGLOS------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_arreglo(t):
    '''ARREGLO : corchetea ARRCONT corchetec'''
    #print('ESTO TERMINA UN ARREGLO')

def p_arrcont(t):
    '''ARRCONT : ARRCONT coma ALGO
            | ALGO
            | '''

def p_llamadaarr(t):
    '''LLAMADARR : id INDARS'''
    #print('ESTO ES LA LLAMADA A ', t[1] ,' EN ÍNDICE', t[2])

def p_indicearr(t):
    '''INDARS :  INDARS INDAR'''
    t[0] = []
    t[0].append(t[1])
    t[0].append(t[2])  
    
def p_indicearr2(t):
    '''INDARS : INDAR'''
    t[0] = t[1] 

def p_indar(t):
    '''INDAR : corchetea id corchetec
            | corchetea SOPERACION corchetec'''
    t[0] = t[2]

#  ------------------------------------FUNCIONES------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_declfunc(t):
    '''DECLFUNC : function id parentesisa PARAMS parentesisc INSTRUCCIONES end puntocoma'''
    #print('LO DE ARRIBA ERA UNA FUNCION')

def p_params(t):
    '''PARAMS : PARAMS coma id
            | id 
            | '''

def p_llamadafunc(t):
    '''LLAMADAFUNC : id parentesisa PARAMSFUNC parentesisc puntocoma'''
    #print('LLAMANDO A: ', t[1])

def p_paramsfunc(t):
    '''PARAMSFUNC : PARAMSFUNC coma ALGO
                | ALGO
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

def p_nombrealgo(t):
    '''NOMBREALGO : LLAMADARR
                | STRUCTASIGN
                | id'''

#string

def p_asignaciones3(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING puntocoma'''
    #print('ASIGNACION STRING --', t[3])

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING dos_dospuntos TIPOS puntocoma'''
    #print('ASIGNACION STRING: ', t[5])


#cualquiera

def p_asignaciones(t):
    '''ASIGNACION : NOMBREALGO igual ALGO puntocoma'''
    #print('ASIGNACION CUALQUIERA --', t[3])


def p_asignaciones2(t):
    '''ASIGNACION : NOMBREALGO igual ALGO dos_dospuntos TIPOS puntocoma'''
    #print('ASIGNACION CUALQUIERA: ', t[5])



#nothing

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual nothing puntocoma'''
    #print('ASIGNACION NOTHING --', t[3])

#  ---------------------------------FUNCIONES---------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_funciones(t):
    '''FUNCIONES : FIF
                | FWHILE
                | FFOR'''

def p_transferencia(t):
    '''TRANSF : break puntocoma
            | continue puntocoma
            | return puntocoma'''
    #print('SENTENCIA DE TRANSFERENCIA: ', t[1])

#  -------------------------------------- FOR---------------------------------------------------------

def p_ffor(t):
    '''FFOR : for id in RANGO INSTRUCCIONES end puntocoma'''
    #print('Eso fue un for de', t[2], ' en ', t[4])

def p_rangofor(t):
    '''RANGO : int dospuntos int
            | cadena'''
    if str(t[1]).isnumeric():
        t[0] =  t[3] - (t[1] - 1)
    else:
        t[0] = len(str(t[1]))
#  ------------------------------------WHILE ---------------------------------------------------------

def p_fwhile(t):
    '''FWHILE : while SOPLOG INSTRUCCIONES end puntocoma'''
    #print('Eso fue un while si', t[2])

#  -------------------------------------- IF ---------------------------------------------------------

def p_fif(t):
    '''FIF : if SOPLOG INSTRUCCIONES FELSEIF
            | if SOPLOG INSTRUCCIONES FELSE
            | if SOPLOG INSTRUCCIONES end puntocoma''' 
    #print('IF 1')

def p_felseif(t):
    '''FELSEIF : elseif SOPLOG INSTRUCCIONES FELSEIF
            | elseif SOPLOG INSTRUCCIONES FELSE
            | elseif SOPLOG INSTRUCCIONES end puntocoma'''
    #print('ELSEIF 1')
        
def p_felse(t):
    '''FELSE : else INSTRUCCIONES end puntocoma'''
    #print('ELSE 1')

def p_fifunilinea(t):
    ''' FIFUNI : SOPLOG interrogacionc ALGO dospuntos ALGO'''
    #print('FIFUNI', t[1], ' SISI: ', t[3], ' SINO ', t[5])

#  ---------------------------------IMPRIMIR----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sprint(t):
    '''IMPRIMIR : println parentesisa SCONTPRNT parentesisc puntocoma
                | print parentesisa SCONTPRNT parentesisc puntocoma'''
    #print('IMPRIMIR 1')

def p_scontprint(t):
    '''SCONTPRNT : SCONTPRNT coma SCONTPRNT'''
    t[0] = str(t[1]) + str(t[3])

def p_scontprintterm(t):
    '''SCONTPRNT :  ALGO
                | FIFUNI'''
    t[0] = t[1]


# *********************************************************************************************************
# *********************************************************************************************************
# ****************************  A PARTIR DE ACÁ ESTA EL COSO CON TODO Y PARSER ****************************
# *********************************************************************************************************
# *********************************************************************************************************

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
            | flotante
            | cadena
            | caracter
            | SOPERACION'''
    t[0] = t[1]
            

#------------------------------OPERACIONES NATIVAS----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sopnativ(t):
    '''SOPNATIV : uppercase parentesisa SOPN parentesisc
                | lowercase parentesisa SOPN parentesisc
                | length parentesisa SOPN parentesisc'''
    if t[1] == 'uppercase'  : t[0] = str(t[3]).upper()
    elif t[1] == 'lowercase'  : t[0] = str(t[3]).lower()
    elif t[1] == 'length'  : t[0] = len(str(t[3]))

def p_sopnativterm(t):
    ''' SOPN : cadena
            | caracter
            | id
            | SOPSTRING'''
    t[0] = t[1]

def p_declnativ(t):
    '''DECLNATIV : parse parentesisa TIPOS coma ALGO parentesisc'''
    #print('EN DECLNATIV 4.6.2 ->', t[1])
    grafo.generarPadre(5)
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Type', t[4], 'Termino', t[6])

def p_declnativ2(t):
    '''DECLNATIV : trunc parentesisa int64 coma flotante parentesiscc'''
    grafo.generarHijos(t[1], t[2], t[3], t[4], t[5], t[6])

def p_declnativ3(t):
    '''DECLNATIV :  float parentesisa int parentesisc'''
    grafo.generarHijos(t[1], t[2], t[3], t[4])

def p_declnativ4(t):
    '''DECLNATIV :  string parentesisa ALGO parentesisc'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Termino', t[4])


def p_declnativ5(t):
    '''DECLNATIV : typeof parentesisa ALGO parentesisc'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Termino', t[4])

#------------------------------OPERACIONES STRING ----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sopstring(t):
    '''SOPSTRING : SOPSTRING asterisco SOPSTRING'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos("OPString", t[2], 'OPString')
    t[0] = t[1] + t[3]


def p_sopstring2(t):
    '''SOPSTRING :  SOPSTRING elevado int'''
    grafo.generarPadre(1)
    grafo.generarHijos('OPString', t[2], t[3])
    t[0] = ""
    copia = t[1]
    number = 0
    while  number < t[3]:
        t[0] = t[0] + copia
        number = number +1

def p_sopstringterm(t):
    '''SOPSTRING : cadena
                | caracter
                | id'''
    t[0] = t[1]
    grafo.generarHijos(t[1])

def p_sopstringterm2(t):
    '''SOPSTRING : SOPNATIV'''
    t[0] = t[1]
    grafo.generarPadre(1)

#  ----------------------------OPERACIONES NUMÉRICAS--------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def p_soperacion(t):
    '''SOPERACION : SOPERACION mas SOPERACION
                    | SOPERACION menos SOPERACION
                    | SOPERACION asterisco SOPERACION
                    | SOPERACION dividido SOPERACION
                    | SOPERACION modulo SOPERACION
                    | SOPERACION elevado SOPERACION'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos("Operacion", t[2], 'Operacion')
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]
    elif t[2] == '%': t[0] = t[1] % t[3]
    elif t[2] == '^': t[0] = t[1] ** t[3]

def p_soperacionUmenos(t):
    '''SOPERACION : menos SOPERACION %prec umenos'''
    t[0] = -t[2]
    grafo.generarPadre(2)
    grafo.generarHijos('-', 'Operacion')

def p_soperacionPar(t):
    '''SOPERACION : parentesisa SOPERACION parentesisc'''
    t[0] = t[2]
    grafo.generarPadre(2)
    grafo.generarHijos("(", "Operacion", ")")

def p_soperacionMath(t):
    '''SOPERACION : NATMATH parentesisa SOPERACION parentesisc'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)    
    grafo.generarHijos('Función Matenática', t[2], "Operacion", t[4])
    
    if t[1] == 'log10': t[0] = math.log10(t[3])        
    elif t[1] == 'sin': t[0] = math.sin(t[3])
    elif t[1] == 'cos': t[0] = math.cos(t[3])
    elif t[1] == 'tan': t[0] = math.tan(t[3])
    elif t[1] == 'sqrt': t[0] = math.sqrt(t[3])

def p_soperacionlog(t):
    '''SOPERACION : log parentesisa SOPERACION coma SOPERACION parentesisc'''
    t[0] = math.log(t[5], t[3])
    print('SOPLOG')
    grafo.generarPadre(3)
    grafo.generarPadre(5)
    grafo.generarHijos(t[1], t[2], "Operacion", t[4], "Operacion", t[6])
    
    
    
def p_soperacionNumeros(t):
    '''SOPERACION : int
                    | flotante'''
    t[0] = t[1]
    grafo.generarHijos(t[1])

def p_nathmath(t):
    '''NATMATH : log10
                | sin
                | cos
                | tan
                | sqrt '''
    t[0] = t[1]
    grafo.generarHijos(t[1])


#  --------------------------------------- ERRORES --------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def p_error(t):
    try: 
        desc = 'Error sintactico con \"' + t.value + '\"'
        global contaerrores
        contaerrores = contaerrores+1
        error1 = NodoError(contaerrores, desc, t.lineno, t.lexpos)
        listaErrores.append(error1)
        #print("Error sintactico en '%s'" % t.value)
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
    global contaerrores
    contaerrores = 0
    paraImprimir('cosas que se imprimen -------------------------------------------------------\n')

    parser = yacc.yacc()
    result = parser.parse(texto)
    
    #for i in listaErrores:
    #    #print(i.descripcion, ' ', i.fila, ' ', i.columna, ' ', i.fecha)
    #print("\n\n\n")
    global grafo
    print(grafo.textoNodo, '\n', grafo.textoEdges)
    exportacion = Exporte(impresion, '', '', listaErrores)

    return exportacion



def paraImprimir(texto):
    global impresion 
    impresion += texto


#fighting('uppercase()')
#parser = yacc.yacc()
#result = parser.parse('uppercase()')
#print(result)
