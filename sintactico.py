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
                    | SOPERACIONES'''  #este ultimo es temporal
    #grafo.generarPadre(1)   

#LO QUE VA ADENTRO DEL TEXTO
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
                    | SOPERACIONES'''  #este ultimo es temporal


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
    grafo.generarHijos(t[1])

def p_algo(t):
    '''ALGO : SOPERACIONES'''
    t[0] = t[1]
    grafo.generarPadre(1)
    grafo.generarHijos('Data')

def p_algo2(t):
    '''ALGO : id'''
    t[0] = t[1]
    grafo.generarHijos(t[1])
    


#  ------------------------------------FUNCIONES------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_declfunc(t):
    '''DECLFUNC : function id parentesisa PARAMS parentesisc INSTRUCCIONES end puntocoma'''
    grafo.generarPadre(6)
    grafo.generarPadre(4)
    grafo.generarHijos(t[1], t[2], t[3], 'Parametros', t[5], 'Instrucciones', t[7], t[8])

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
    '''LLAMADAFUNC : id parentesisa PARAMSFUNC parentesisc puntocoma'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Parámetros', t[4], t[5])

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
        x= 1
        #grafo.generarPadre(1)
        #grafo.generarHijos('ASIGNACION')
    

#cualquiera

def p_nombrealgo(t):
    '''NOMBREALGO : id'''
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador')
    

def p_nombrealgo(t):
    '''NOMBREALGO : id'''
    grafo.generarHijos(t[1])

#string

def p_asignaciones3(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING puntocoma'''
    #grafo.generarHijos('prueba')
    grafo.generarPadre(3)    
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido', t[4]) 

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING dos_dospuntos TIPOS puntocoma'''
    #grafo.generarHijos('prueba')
    #grafo.generarHijos('prueba')
    grafo.generarPadre(5)    
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido', t[4], 'Tipo', t[6])


#cualquiera

def p_asignaciones(t):
    '''ASIGNACION : NOMBREALGO igual ALGO puntocoma'''
    #grafo.generarHijos('prueba')
    grafo.generarPadre(3)    
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido', t[4])  


def p_asignaciones2(t):
    '''ASIGNACION : NOMBREALGO igual ALGO dos_dospuntos TIPOS puntocoma'''
    #grafo.generarHijos('prueba')
    #grafo.generarHijos('prueba')
    grafo.generarPadre(5)    
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido', t[4], 'Tipo', t[6])


#nothing

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual nothing puntocoma'''
    #grafo.generarHijos('prueba')
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], t[3], t[4])

#  ---------------------------------FUNCIONES---------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_funciones(t):
    '''FUNCIONES : FIF
                | FWHILE
                | FFOR'''
    grafo.generarPadre(1)
    grafo.generarHijos('FUNCIÓN')

def p_transferencia(t):
    '''TRANSF : break puntocoma
            | continue puntocoma
            | return puntocoma'''
    grafo.generarHijos(t[1], t[2])

#  -------------------------------------- FOR---------------------------------------------------------

def p_ffor(t):
    '''FFOR : for id in RANGO INSTRUCCIONES end puntocoma'''
    grafo.generarPadre(5)
    grafo.generarPadre(4)
    grafo.generarHijos(t[1], t[2], t[3], 'Rango', 'Instrucciones', t[6], t[7])

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
    '''FWHILE : while SOPLOG INSTRUCCIONES end puntocoma'''
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', t[4], t[5])

#  -------------------------------------- IF ---------------------------------------------------------

def p_fif(t):
    '''FIF : if SOPLOG INSTRUCCIONES FELSEIF
            | if SOPLOG INSTRUCCIONES FELSE''' 
    grafo.generarPadre(4)
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', 'Condicional')


def p_fif2(t):
    '''FIF :  if SOPLOG INSTRUCCIONES end puntocoma''' 
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', t[4], t[5])
    print('BUSQ: ', grafo.textoEdges)
   

def p_felseif(t):
    '''FELSEIF : elseif SOPLOG INSTRUCCIONES FELSEIF
            | elseif SOPLOG INSTRUCCIONES FELSE'''
    grafo.generarPadre(4)
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', 'Condicional')

def p_felseif2(t):
    '''FELSEIF : elseif SOPLOG INSTRUCCIONES end puntocoma'''
    grafo.generarPadre(3)
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', 'Instrucciones', t[4], t[5])
    
        
def p_felse(t):
    '''FELSE : else INSTRUCCIONES end puntocoma'''
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Instrucciones', t[3], t[4])

def p_fifunilinea(t):
    ''' FIFUNI : SOPLOG interrogacionc ALGO dospuntos ALGO'''
    grafo.generarPadre(5)
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Operacion', t[2], 'Termino', t[4], 'Termino')

#  ---------------------------------IMPRIMIR----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sprint(t):
    '''IMPRIMIR : println parentesisa SCONTPRNT parentesisc puntocoma
                | print parentesisa SCONTPRNT parentesisc puntocoma'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Terminos', t[4], t[5])

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
    grafo.generarHijos('CONTENIDO')
    


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
