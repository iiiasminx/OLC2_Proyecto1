# importo todo de todos lados
from gramatica import fighting, tokens
import cst as cst
from operaciones import *
from semantico  import *
from sintactico import * 

lista_simbolos = [] # acá van todos los valores que se hayan declarado
arbol =[]
ts_global = cst.TablaSimbolos()

def fightingfinal(texto):
    exportef = fighting2(texto)
    global arbol 
    arbol = exportef.arbol
    procesarInstrucciones(arbol, ts_global)

    return exportef

def procesarInstrucciones(ast, tablaSimbolos : cst.TablaSimbolos):
    contador = 1
    print('\n')
    for instruccion in ast:
        print(contador)
        contador += 1
        if isinstance(instruccion, Impresion): intImpresion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Impresionln): intImpresionLN(instruccion, tablaSimbolos)


        elif isinstance(instruccion, Declaracion): intDeclaracion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Asignacion): intAsignacion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, AsignacionTipada): intAsignacionTipada(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Scope): intScope(instruccion, tablaSimbolos)


        elif isinstance(instruccion, DefFuncion): intDefFuncion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, DefFuncParam): intDefFuncParam(instruccion, tablaSimbolos)
        elif isinstance(instruccion, DefFuncParams): intDefFuncParam(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FuncParams): intDefFuncParam(instruccion, tablaSimbolos)

        elif isinstance(instruccion, LlamadaFuncion): intLlamadaFuncion(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FParse): intFParse(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FTrunc): intFTrunc(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FFloat): intFFloat(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FString): intFString(instruccion, tablaSimbolos)
        elif isinstance(instruccion, Ftypeof): intFtypeof(instruccion, tablaSimbolos)


        elif isinstance(instruccion, FIFuni): intFIFuni(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FIF): intFIF(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FElseIF): intFElseIF(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FELSE): intFELSE(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FWhile): intFWhile(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FFor): intFFor(instruccion, tablaSimbolos)
        elif isinstance(instruccion, FForRangoNum): intFForRangoNum(instruccion, tablaSimbolos)

        elif isinstance(instruccion, SBreak): intSBreak(instruccion, tablaSimbolos)
        elif isinstance(instruccion, SContinue): intSContinue(instruccion, tablaSimbolos)
        elif isinstance(instruccion, SReturn): intSReturn(instruccion, tablaSimbolos)


        elif isinstance(instruccion, DeclStruct): intDeclStruct(instruccion, tablaSimbolos)
        elif isinstance(instruccion, ConstruccionStruct): intConstruccionStruct(instruccion, tablaSimbolos)
        elif isinstance(instruccion, AsignacionAtributosStruct): intAsignacionAtributosStruct(instruccion, tablaSimbolos)
        elif isinstance(instruccion, AccesoAtributo): intAccesoAtributo(instruccion, tablaSimbolos)
        
        print('\n', instruccion)

# ------------------------------------------------------------------------- 
# Inicio Operaciones ------------------------------------------------------
# ------------------------------------------------------------------------- 

# numericas
def resolverNumerica(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPBinaria): 
        pass
    elif isinstance(Exp, OPNeg):
        pass
    elif isinstance(Exp, OPNativa):#log10, sin, cos, tan, sqrt
        pass
    elif isinstance(Exp, OPNativaLog):
        pass
    elif isinstance(Exp, OPNum):
        pass
    elif isinstance(Exp, OPID):
        return tablaSimbolos

def resolverBooleana(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPLogica): 
        pass
    elif isinstance(Exp, OPBool):
        pass
    elif isinstance(Exp, OPID):
        pass

def resolverCadena(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPCadena): 
        pass
    elif isinstance(Exp, OPLength):
        pass
    elif isinstance(Exp, OPLowercase):
        pass
    elif isinstance(Exp, OPUppercase):
        pass
    elif isinstance(Exp, OPElevarString):
        pass
    elif isinstance(Exp, OPMergeString):
        pass
    elif isinstance(Exp, OPID):
        pass






# ------------------------------------------------------------------------- 
# Fin Operaciones ---------------------------------------------------------
# -------------------------------------------------------------------------       

# Impresion ---------------------------------------------------------------
# -------------------------------------------------------------------------
def intImpresion(instr, tablaSimbolos: cst.TablaSimbolos):
    print('impresion')

def intImpresionLN(instr, tablaSimbolos : cst.TablaSimbolos):
    print('impresionLN')

#variables o cosos del struct ---------------------------------------------
# -------------------------------------------------------------------------
def intDeclaracion(instr, tablaSimbolos : cst.TablaSimbolos): #ver si necesito más de estas
    print('intDeclaracion')

def intAsignacion(instr, tablaSimbolos : cst.TablaSimbolos):

    print('intAsignacion')

def intAsignacionTipada(instr, tablaSimbolos : cst.TablaSimbolos):
    print('intAsignacionTipada')

def intScope(instr, tablaSimbolos : cst.TablaSimbolos): #ver si cambio este por otro como lo hice en el sintactico
    print('intScope')
    # acá sepáro asignacion de asignacion tipada y eso

# Funciones ---------------------------------------------------------------
# -------------------------------------------------------------------------
def intDefFuncion(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intDefFuncParam(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intDefFuncParams(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFuncParams(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intLlamadaFuncion(instr, tablaSimbolos : cst.TablaSimbolos):
    pass

# Funciones nativas -------------------------------------------------------
# -------------------------------------------------------------------------
def intFParse(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFTrunc(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFFloat(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFString(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFtypeof(instr, tablaSimbolos : cst.TablaSimbolos):
    pass


# Condicionales -----------------------------------------------------------
# -------------------------------------------------------------------------

def intFIFuni(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFIF(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFElseIF(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFELSE(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFWhile(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFFor(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intFForRangoNum(instr, tablaSimbolos : cst.TablaSimbolos):
    pass

# Sentencias de transicion
def intSBreak(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intSContinue(instr, tablaSimbolos : cst.TablaSimbolos):
    pass
def intSReturn(instr, tablaSimbolos : cst.TablaSimbolos):
    pass

# Struct ------------------------------------------------------------------
# -------------------------------------------------------------------------
def intDeclStruct(instr, tablaSimbolos : cst.TablaSimbolos):
    pass

def intConstruccionStruct(instr, tablaSimbolos : cst.TablaSimbolos):# esto es en p = Carro(1,2)
    pass

def intAsignacionAtributosStruct(instr, tablaSimbolos : cst.TablaSimbolos):
    pass

def intAccesoAtributo(instr, tablaSimbolos : cst.TablaSimbolos):
    pass

