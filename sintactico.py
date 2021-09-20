# ----------------------------------------------------------------------------------------------------- 
#---------------------------------------- INICIO SINTÁCTICO -------------------------------------------
# -----------------------------------------------------------------------------------------------------


import ply.yacc as yacc
import os
import codecs
import re 
from gramatica import fighting, tokens
from cst import NodoError, Exporte, GrafoCST 
from semantico import *
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
#sintactico = Sintactico()

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
    '''INICIO : INSTRUCCIONES2'''
    grafo.generarPadre(1)
    grafo.generarHijos('INICIO')



def p_instrucciones2(t):
    '''INSTRUCCIONES2 : INSTRUCCION2 puntocoma INSTRUCCIONES2'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Instruccion', t[2], 'Instrucciones')


def p_instrucciones21(t):
    '''INSTRUCCIONES2 :  INSTRUCCION2 puntocoma'''
    grafo.generarPadre(1)
    grafo.generarHijos('Instruccion', t[2])

def p_instruccion2(t):
    '''INSTRUCCION2  :  IMPRIMIR
                    | FUNCIONES
                    | SCOPE
                    | DECLFUNC
                    | LLAMADAFUNC
                    | TRANSF
                    | SOPERACIONES
                    | TYPESTRUCT'''  
    #grafo.generarPadre(1)   

#LO QUE VA ADENTRO DEL TEXTO
def p_instrucciones1(t):
    '''INSTRUCCIONES : INSTRUCCION puntocoma INSTRUCCIONES'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Instruccion', t[2], 'Instrucciones')


def p_instrucciones11(t):
    '''INSTRUCCIONES :  INSTRUCCION puntocoma'''
    grafo.generarPadre(1)
    grafo.generarHijos('Instruccion', t[2])


def p_instruccion(t):
    '''INSTRUCCION  :  IMPRIMIR
                    | FUNCIONES
                    | SCOPE
                    | DECLFUNC
                    | LLAMADAFUNC
                    | TRANSF
                    | SOPERACIONES
                    | TYPESTRUCT'''  #este ultimo es temporal


def p_soperaciones(t):
    '''SOPERACIONES : SOPSTRING
                    | SOPNATIV
                    | SOPERACION
                    | SOPLOG
                    | DECLNATIV
                    | OPIDLOG'''
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
    grafo.generarHijos(t[1])

def p_algo(t):
    '''ALGO : SOPERACIONES
            | ARREGLO
            | LLAMADARR
            | STRUCTINI'''
    t[0] = t[1]
    #grafo.generarPadre(1)
    #grafo.generarHijos('Data')

def p_algo2(t):
    '''ALGO : id'''
    t[0] = t[1]
    grafo.generarHijos(t[1])
    
#  -------------------------------------- STRUCT------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_typestruct(t):
    '''TYPESTRUCT : STRUCT'''
    grafo.generarPadre(1)
    grafo.generarHijos('Struct')
    
def p_typestruct2(t):
    '''TYPESTRUCT : mutable STRUCT'''
    grafo.generarPadre(1)
    grafo.generarHijos(t[1], 'Struct')
    

def p_struct(t):
    '''STRUCT : struct id ATRIBUTOS end'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Atributos', t[4])

def p_atributos(t):
    '''ATRIBUTOS : ATRIBUTO  puntocoma ATRIBUTOS'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Atributo', t[2], 'Atributo')

def p_atributos2(t):
    '''ATRIBUTOS :  ATRIBUTO  puntocoma'''
    grafo.generarPadre(1)
    grafo.generarHijos('Atributo', t[2])

def p_atributo(t):
    '''ATRIBUTO : id dos_dospuntos TIPOS ''' 
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Type')

def p_atributo2(t):
    '''ATRIBUTO :  id ''' #quite el ; de acá
    grafo.generarHijos(t[1])

def p_creacionstruct(t):
    '''STRUCTINI : id parentesisa PARAMSFUNC parentesisc'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Params', t[4])


def p_structasign(t):
    '''STRUCTASIGN : id punto id'''
    t[0] = t[1] + t[2] + t[3]
    grafo.generarHijos(t[1], t[2], t[3])

#  ------------------------------------ ARREGLOS------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_arreglo(t):
    '''ARREGLO : corchetea ARRCONT corchetec'''
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Contenido', t[3])

def p_arrcont(t):
    '''ARRCONT : ARRCONT coma ARRCONT '''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Valor', t[2], 'Contenido')

def p_arrcont2(t):
    '''ARRCONT :  ALGO '''

def p_arrcont3(t):
    '''ARRCONT :  '''
    grafo.generarHijos('')

def p_llamadaarr(t):
    '''LLAMADARR : id INDARS'''
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Indices')

def p_indarcvzx(t):
    '''INDARS : INDAR corchetec INDARS'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Indice', t[2], 'Indices')

def p_indars2(t):
    '''INDARS : INDAR corchetec'''
    grafo.generarPadre(1)
    grafo.generarHijos('Indice', t[2])

def p_indar2(t):
    '''INDAR : corchetea id'''
    t[0] = t[2]
    grafo.generarHijos(t[1], t[2])

def p_indar(t):
    '''INDAR :  corchetea SOPERACION '''
    t[0] = t[2]
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operación')

#  ------------------------------------FUNCIONES------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_declfunc(t):
    '''DECLFUNC : function id parentesisa PARAMS parentesisc INSTRUCCIONES end '''
    grafo.generarPadre(6)
    grafo.generarPadre(4)
    grafo.generarHijos(t[1], t[2], t[3], 'Parametros', t[5], 'Instrucciones', t[7])

def p_params(t):
    '''PARAMS : PARAMS coma PARAMS '''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Param', t[2], 'Param')


def p_params2(t):
    '''PARAMS : id '''
    grafo.generarHijos(t[1])

def p_params3(t):
    '''PARAMS :  '''
    grafo.generarHijos('')

def p_llamadafunc(t):
    '''LLAMADAFUNC : id parentesisa PARAMSFUNC parentesisc'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Parámetros', t[4])

def p_paramsfunc(t):
    '''PARAMSFUNC : PARAMSFUNC coma PARAMSFUNC'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Param', t[2], 'Param')

def p_paramsfunc3(t):
    '''PARAMSFUNC :  ALGO'''    
    #grafo.generarHijos('prueba')

def p_paramsfunc2(t):
    '''PARAMSFUNC :  '''
    grafo.generarHijos('')
#  ---------------------------------ASIGNACIONES------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sope(t):
    '''SCOPE : global ASIGNACION
            | local ASIGNACION
            | ASIGNACION'''
    t[0] = t[1]
    if t[1] == 'global'  : 
        grafo.generarPadre(2)
        grafo.generarHijos(t[1], 'Asign')
    elif t[1] == 'local'  : 
        grafo.generarPadre(2)
        grafo.generarHijos(t[1], 'Asign')
    else:
        x = 1
        
    

#cualquiera

def p_nombrealgo(t):
    '''NOMBREALGO : LLAMADARR
                | STRUCTASIGN'''
    #grafo.generarPadre(1)
    #grafo.generarHijos('Identificador')
    

def p_nombrealgo2(t):
    '''NOMBREALGO : id'''
    grafo.generarHijos(t[1])

#string

def p_asignaciones3(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING '''
    #grafo.generarHijos('prueba')
    grafo.generarPadre(3)    
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido') 

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING dos_dospuntos TIPOS '''
    #grafo.generarHijos('prueba')
    #grafo.generarHijos('prueba')
    grafo.generarPadre(5)    
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido', t[4], 'Tipo')


#cualquiera

def p_asignaciones(t):
    '''ASIGNACION : NOMBREALGO igual ALGO '''
    #grafo.generarHijos('prueba')
    grafo.generarPadre(3)    
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido')  


def p_asignaciones2(t):
    '''ASIGNACION : NOMBREALGO igual ALGO dos_dospuntos TIPOS '''
    #grafo.generarHijos('prueba')
    #grafo.generarHijos('prueba')
    grafo.generarPadre(5)    
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido', t[4], 'Tipo')


#nothing

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual nothing '''
    #grafo.generarHijos('prueba')
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], t[3])

#  ---------------------------------FUNCIONES---------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_funciones(t):
    '''FUNCIONES : FIF
                | FWHILE
                | FFOR'''
    grafo.generarPadre(1)
    grafo.generarHijos('FUNCIÓN')

def p_transferencia(t):
    '''TRANSF : break 
            | continue 
            | return '''
    grafo.generarHijos(t[1])

#  -------------------------------------- FOR---------------------------------------------------------

def p_ffor(t):
    '''FFOR : for id in RANGO INSTRUCCIONES end'''
    grafo.generarPadre(5)
    grafo.generarPadre(4)
    grafo.generarHijos(t[1], t[2], t[3], 'Rango', 'Instrucciones', t[6])

def p_rangofor(t):
    '''RANGO : int dospuntos int'''
    grafo.generarHijos(t[1], t[2], t[3])
    t[0] =  t[3] - (t[1] - 1)

def p_rangofor2(t):
    '''RANGO : cadena'''
    grafo.generarHijos(t[1])
    t[0] = len(str(t[1]))
#  ------------------------------------WHILE ---------------------------------------------------------

def p_fwhile(t):
    '''FWHILE : while SOPLOG INSTRUCCIONES end'''
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', t[4])

#  -------------------------------------- IF ---------------------------------------------------------

def p_fif(t):
    '''FIF : if SOPLOG INSTRUCCIONES FELSEIF
            | if SOPLOG INSTRUCCIONES FELSE''' 
    grafo.generarPadre(4)
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', 'Condicional')


def p_fif2(t):
    '''FIF :  if SOPLOG INSTRUCCIONES end''' 
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', t[4])
    print('BUSQ: ', grafo.textoEdges)
   

def p_felseif(t):
    '''FELSEIF : elseif SOPLOG INSTRUCCIONES FELSEIF
            | elseif SOPLOG INSTRUCCIONES FELSE'''
    grafo.generarPadre(4)
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', 'Condicional')

def p_felseif2(t):
    '''FELSEIF : elseif SOPLOG INSTRUCCIONES end'''
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', t[4])
    
        
def p_felse(t):
    '''FELSE : else INSTRUCCIONES end'''
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Instrucciones', t[3])

def p_fifunilinea(t):
    ''' FIFUNI : SOPLOG interrogacionc ALGO dospuntos ALGO'''
    grafo.generarPadre(5)
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Operacion', t[2], 'Termino', t[4], 'Termino')

#  ---------------------------------IMPRIMIR----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sprint(t):
    '''IMPRIMIR : println parentesisa SCONTPRNT parentesisc 
                | print parentesisa SCONTPRNT parentesisc '''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Terminos', t[4])
    

def p_scontprint(t):
    '''SCONTPRNT : SCONTPRNT coma SCONTPRNT'''
    t[0] = str(t[1]) + str(t[3])
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Termino', t[2], 'Termino')

def p_scontprintterm(t):
    '''SCONTPRNT :  ALGO
                | FIFUNI'''
    t[0] = t[1]
    grafo.generarPadre(1)
    grafo.generarHijos('Contenido')
    

#  -------------------------------OPERACION CON ID ---------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def operacionid(t):
    '''OPIDLOG : OPIDLOG and OPIDLOG
            | OPIDLOG or OPIDLOG
            | OPIDLOG mayorque OPIDLOG
            | OPIDLOG menorque OPIDLOG
            | OPIDLOG mayoriwal OPIDLOG
            | OPIDLOG menoriwal OPIDLOG
            | OPIDLOG iwaliwal OPIDLOG
            | OPIDLOG distintoque OPIDLOG'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Operacion', t[2], 'Operacion')

def p_sopid(t):
    '''OPIDLOG : parentesisa OPIDLOG parentesisc'''
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', t[3])

def p_sopid2(t):
    '''OPIDLOG : SOPERACIONES
                | OPID'''

def p_sopid3(t):
    '''OPID : OPID mas OPID
                    | OPID menos OPID
                    | OPID asterisco OPID
                    | OPID dividido OPID
                    | OPID modulo OPID
                    | OPID elevado OPID'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos("Operacion", t[2], 'Operacion')


def p_sopid4(t):
    '''OPID : menos OPID %prec umenos'''
    grafo.generarPadre(2)
    grafo.generarHijos('-', 'Operacion') 

def p_sopid8(t):
    '''OPID : parentesisa OPID parentesisc'''
    grafo.generarPadre(2)
    grafo.generarHijos("(", "Operacion", ")")

def p_sopid7(t):
    '''OPID : NATMATH parentesisa OPID parentesisc'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)    
    grafo.generarHijos('Función Matenática', t[2], "Operacion", t[4])

def p_sopid6(t):
    '''OPID : log parentesisa OPID coma OPID parentesisc'''
    grafo.generarPadre(3)
    grafo.generarPadre(5)
    grafo.generarHijos(t[1], t[2], "Operacion", t[4], "Operacion", t[6]) 

def p_sopid5(t):
    '''OPID : int
            | flotante
            | id'''
    grafo.generarHijos(t[1])


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
    #grafo.generarHijos('prueba')
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Operacion', t[2], 'Operacion')
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
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', t[3])

def p_soplogterm2(t):
    '''SOPLOG : SOPERACION'''
    t[0] = t[1]
    #grafo.generarPadre(1)
    #grafo.generarHijos('OPERACIÓN LÓGICA')
    

def p_soplogterm(t):
    '''SOPLOG : true
            | false
            | int
            | flotante
            | cadena
            | caracter'''
    t[0] = t[1]
    grafo.generarHijos(t[1])


            

#------------------------------OPERACIONES NATIVAS----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sopnativ(t):
    '''SOPNATIV : uppercase parentesisa SOPN parentesisc
                | lowercase parentesisa SOPN parentesisc
                | length parentesisa SOPN parentesisc'''
    #grafo.generarHijos('prueba')
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Termino', t[4])
    if t[1] == 'uppercase'  : t[0] = str(t[3]).upper()
    elif t[1] == 'lowercase'  : t[0] = str(t[3]).lower()
    elif t[1] == 'length'  : t[0] = len(str(t[3]))

def p_sopnativterm(t):
    ''' SOPN : cadena
            | caracter
            | id'''
    t[0] = t[1]
    grafo.generarHijos(t[1])

def p_sopnativterm(t):
    ''' SOPN :  SOPSTRING'''
    t[0] = t[1]
    grafo.generarPadre(1)


def p_declnativ(t):
    '''DECLNATIV : parse parentesisa TIPOS coma ALGO parentesisc'''
    grafo.generarPadre(5)
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Type', t[4], 'Termino', t[6])

def p_declnativ2(t):
    '''DECLNATIV : trunc parentesisa int64 coma flotante parentesisc'''
    grafo.generarHijos(t[1], t[2], t[3], t[4], t[5], t[6])


def p_declnativ3(t):
    '''DECLNATIV :  float parentesisa int parentesisc'''
    grafo.generarHijos(t[1], t[2], t[3], t[4])

def p_declnativ4(t):
    '''DECLNATIV :  string parentesisa ALGO parentesisc'''
    #grafo.generarHijos('algo')
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
    except Exception as e:
        print('Algo pasó en el error :c ', e)


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
    global grafo
    grafo.textoNodo = ""
    grafo.textoEdges = ""
    grafo.contador = 0
    paraImprimir('cosas que se imprimen -------------------------------------------------------\n')

    parser = yacc.yacc()
    result = parser.parse(texto)
    
    #for i in listaErrores:
    #    #print(i.descripcion, ' ', i.fila, ' ', i.columna, ' ', i.fecha)
    #print("\n\n\n")
    migrafo = 'digraph G { \n' + grafo.textoNodo + '\n' + grafo.textoEdges +'}'
    #print(migrafo)
    exportacion = Exporte(impresion, '', migrafo, listaErrores)

    return exportacion



def paraImprimir(texto):
    global impresion 
    impresion += texto


#fighting('uppercase()')
#parser = yacc.yacc()
#result = parser.parse('uppercase()')
#print(result)
