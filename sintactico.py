# ----------------------------------------------------------------------------------------------------- 
#---------------------------------------- INICIO SINTÁCTICO -------------------------------------------
# -----------------------------------------------------------------------------------------------------


import ply.yacc as yacc
import os
import codecs
import re 
from gramatica import fighting, tokens
from cst import NodoError, Exporte, GrafoCST 
from sys import stdin
import math

from operaciones import *
from semantico import *

global impresion
impresion = ""
global listaErrores
listaErrores = []
global contaerrores
contaerrores = 0

grafo = GrafoCST()

# cosas para el semántico 


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
    grafo.generarHijos('InstruccionF', t[2], 'InstruccionesF')


def p_instrucciones11(t):
    '''INSTRUCCIONES :  INSTRUCCION puntocoma'''
    grafo.generarPadre(1)
    grafo.generarHijos('InstruccionF', t[2])
    


def p_instruccion(t):
    '''INSTRUCCION  :  IMPRIMIR
                    | FUNCIONES
                    | SCOPE
                    | DECLFUNC
                    | LLAMADAFUNC
                    | TRANSF
                    | SOPERACIONES
                    | TYPESTRUCT''' 

    

def p_soperaciones(t):
    '''SOPERACIONES : SOPSTRING
                    | SOPNATIV
                    | OPID
                    | SOPLOG
                    | DECLNATIV'''
    
    

#  ----------------------------------------TIPOS------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_tipos(t):
    '''TIPOS : int64
            | float64
            | bool
            | char
            | string
            | id'''
    
    grafo.generarHijos(t[1])

def p_algo(t):
    '''ALGO : SOPERACIONES
            | ARREGLO
            | LLAMADARR
            | STRUCTINI'''
    

def p_algo2(t):
    '''ALGO : id'''
    
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
    '''STRUCTASIGN : id '''
    
    grafo.generarHijos(t[1])

def p_structasign1(t):
    '''STRUCTASIGNS : STRUCTASIGN punto STRUCTASIGNS'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('StructName', t[2], 'StructName')


def p_structasign2(t):
    '''STRUCTASIGNS :  STRUCTASIGN'''
    #grafo.generarPadre(1)
    #grafo.generarHijos('StructName')

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
    
    grafo.generarHijos(t[1], t[2])

def p_indar(t):
    '''INDAR :  corchetea OPID '''
    
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

def p_params3(t):
    '''PARAMS : id dos_dospuntos TIPOS'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Type')

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
                | STRUCTASIGNS'''
    

def p_nombrealgo2(t):
    '''NOMBREALGO : id'''
    grafo.generarHijos(t[1])
    

#string

def p_asignaciones3(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING '''
    grafo.generarPadre(3)    
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido') 

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual SOPSTRING dos_dospuntos TIPOS '''
    grafo.generarPadre(5)    
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido', t[4], 'Tipo')


#cualquiera

def p_asignaciones(t):
    '''ASIGNACION : NOMBREALGO igual ALGO '''
    grafo.generarPadre(3)    
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido')  



def p_asignaciones2(t):
    '''ASIGNACION : NOMBREALGO igual ALGO dos_dospuntos TIPOS '''
    grafo.generarPadre(5)    
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], 'Contenido', t[4], 'Tipo')


#nothing

def p_asignaciones4(t):
    '''ASIGNACION : NOMBREALGO igual nothing '''
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador', t[2], t[3])

def p_asignaciones5(t):
    '''ASIGNACION : NOMBREALGO  '''
    grafo.generarPadre(1)
    grafo.generarHijos('Identificador')


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

def p_transferencia2(t):
    '''TRANSF : return ALGO'''
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Contenido')

#  -------------------------------------- FOR---------------------------------------------------------

def p_ffor(t):
    '''FFOR : for id in RANGO INSTRUCCIONES end'''
    grafo.generarPadre(5)
    grafo.generarPadre(4)
    grafo.generarHijos(t[1], t[2], t[3], 'Rango', 'Instrucciones', t[6])

def p_rangofor(t):
    '''RANGO : OPID dospuntos OPID'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Operacion', t[2], 'Operacion')
    

def p_rangofor2(t):
    '''RANGO : cadena'''
    grafo.generarHijos(t[1])
    
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
    
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Termino', t[2], 'Termino')

def p_scontprintterm(t):
    '''SCONTPRNT :  ALGO
                | FIFUNI'''
    
    grafo.generarPadre(1)
    grafo.generarHijos('Contenido')
    

#  -------------------------------OPERACION CON ID ---------------------------------------------------
#-----------------------------------------------------------------------------------------------------


def p_sopid3(t):
    '''OPID : OPID mas OPID
                    | OPID menos OPID
                    | OPID asterisco OPID
                    | OPID dividido OPID
                    | OPID modulo OPID
                    | OPID elevado OPID'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos("OperacionID", t[2], 'OperacionID')


def p_sopid4(t):
    '''OPID : menos OPID %prec umenos'''
    grafo.generarPadre(2)
    grafo.generarHijos('-', 'OperacionID') 

def p_sopid8(t):
    '''OPID : parentesisa OPID parentesisc'''
    grafo.generarPadre(2)
    grafo.generarHijos("(", "OperacionID", ")")

def p_sopid7(t):
    '''OPID : NATMATH parentesisa OPID parentesisc'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)    
    grafo.generarHijos('Función Matenática', t[2], "OperacionID", t[4])

def p_sopid6(t):
    '''OPID : log parentesisa OPID coma OPID parentesisc'''
    grafo.generarPadre(3)
    grafo.generarPadre(5)
    grafo.generarHijos(t[1], t[2], "OperacionID", t[4], "OperacionID", t[6]) 

def p_sopid5(t):
    '''OPID : int
            | flotante
            | id            
            | cadena
            | caracter'''
    grafo.generarHijos(t[1])



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
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos('Operacion', t[2], 'Operacion')
    t[0] = OPLogica(t[1], t[2], t[3])
    

def p_soplogPar(t):
    '''SOPLOG : parentesisa SOPLOG parentesisc'''
    
    grafo.generarPadre(2)
    grafo.generarHijos(t[1], 'Operacion', t[3])
    t[0] = t[2]

def p_soplogterm2(t):
    '''SOPLOG : OPID'''
    t[0] = t[1]
    

def p_soplogterm(t):
    '''SOPLOG : int
            | flotante'''    
    grafo.generarHijos(t[1])
    t[0] = OPNum(t[1])

def p_soplogterm3(t):
    '''SOPLOG : cadena
            | caracter'''    
    grafo.generarHijos(t[1])
    t[0] = OPCadena(t[1])

def p_soplogterm4(t):
    '''SOPLOG : id'''    
    grafo.generarHijos(t[1])
    t[0] = OPID(t[1])

def p_soplogterm(t):
    '''SOPLOG : true
            | false'''    
    grafo.generarHijos(t[1])
    t[0] = OPBool(t[1])
            

#------------------------------OPERACIONES NATIVAS----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sopnativ(t):
    '''SOPNATIV : uppercase parentesisa SOPN parentesisc
                | lowercase parentesisa SOPN parentesisc
                | length parentesisa SOPN parentesisc'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Termino', t[4])
    if t[1] == 'uppercase' : t[0] = OPUppercase(t[3])
    elif t[1] == 'lowercase' : t[0] = OPLowercase(t[3])
    else : t[0] == OPLength(t[3])


def p_sopnativterm(t):
    ''' SOPN :  SOPSTRING''' 
    t[0] = t[1]


def p_declnativ(t):
    '''DECLNATIV : parse parentesisa TIPOS coma ALGO parentesisc'''
    grafo.generarPadre(5)
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Type', t[4], 'Termino', t[6])
    t[0] = FParse(t[3], t[5])

def p_declnativ2(t):
    '''DECLNATIV : trunc parentesisa int64 coma ALGO parentesisc'''
    grafo.generarPadre(5)
    grafo.generarHijos(t[1], t[2], t[3], t[4], 'Termino', t[6])
    t[0] = FTrunc(t[3])


def p_declnativ3(t):
    '''DECLNATIV :  float parentesisa ALGO parentesisc'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Termino', t[4])
    t[0] = FFloat(t[3])

def p_declnativ4(t):
    '''DECLNATIV :  string parentesisa ALGO parentesisc'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Termino', t[4])
    t[0] = FString(t[3])

def p_declnativ5(t):
    '''DECLNATIV : typeof parentesisa ALGO parentesisc'''
    grafo.generarPadre(3)
    grafo.generarHijos(t[1], t[2], 'Termino', t[4])
    
    t[0] = Ftypeof(t[3])

#------------------------------OPERACIONES STRING ----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

def p_sopstring(t):
    '''SOPSTRING : SOPSTRING asterisco SOPSTRING'''
    grafo.generarPadre(3)
    grafo.generarPadre(1)
    grafo.generarHijos("OPString", t[2], 'OPString')
    t[0] = OPMergeString(t[1], t[3])


def p_sopstring2(t):
    '''SOPSTRING :  SOPSTRING elevado int'''
    grafo.generarPadre(1)
    grafo.generarHijos('OPString', t[2], t[3])

    t[0] = OPElevarString(t[1], OPNum(t[3]))

def p_sopstring3(t):
    '''SOPSTRING :  SOPSTRING elevado id'''
    grafo.generarPadre(1)
    grafo.generarHijos('OPString', t[2], t[3])

    t[0] = OPElevarString(t[1], OPID(t[3]))
    

def p_sopstringterm(t):
    '''SOPSTRING : cadena
                | caracter'''
    
    grafo.generarHijos(t[1])
    t[0] = OPCadena(t[1])

def p_sopstringterm3(t):
    '''SOPSTRING : id'''    
    grafo.generarHijos(t[1])
    t[0] = OPID(t[1])


def p_sopstringterm2(t):
    '''SOPSTRING : SOPNATIV'''    
    grafo.generarPadre(1)
    t[0] = t[1]

#  ----------------------------OPERACIONES NUMÉRICAS--------------------------------------------------
#-----------------------------------------------------------------------------------------------------


def p_nathmath(t):
    '''NATMATH : log10
                | sin
                | cos
                | tan
                | sqrt '''
    grafo.generarHijos(t[1])
    t[0] = t[1]


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

    migrafo = 'digraph G { \n' + grafo.textoNodo + '\n' + grafo.textoEdges +'}'

    exportacion = Exporte(impresion, '', migrafo, listaErrores)

    return exportacion



def paraImprimir(texto):
    global impresion 
    impresion += texto


#fighting('uppercase()')
#parser = yacc.yacc()
#result = parser.parse('uppercase()')
#print(result)
