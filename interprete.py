# importo todo de todos lados
from gramatica import fighting, tokens
import cst as cst
from operaciones import *
from semantico  import *
from sintactico import * 

lista_simbolos = [] # acá van todos los valores que se hayan declarado
arbol =[]
ts_global = cst.TablaSimbolos()
contaerrores = 0
listasemanticos = []

def fightingfinal(texto):
    exportef = fighting2(texto)
    global arbol 
    arbol = exportef.arbol
    procesarInstrucciones(arbol, ts_global)

    #print(ts_global.simbolos)
    global lista_simbolos
    exportef.tabla_simbolos = lista_simbolos

    global listasemanticos
    exportef.listasemanticos = listasemanticos
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
        else :
            desc = "Error semántico con la instruccion: " + str(contador)
            global contaerrores
            nuevo = cst.NodoErrorSemantico(desc)
            nuevo.contador = contaerrores
            contaerrores += 1
            global listasemanticos
            listasemanticos.append(nuevo)

        
        #print('\n', instruccion)

# ------------------------------------------------------------------------- 
# Inicio Operaciones ------------------------------------------------------
# ------------------------------------------------------------------------- 

def resolverCadena(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPBinaria):
        if Exp.operador == ARITMETICA.ASTERISCO : 
            return Exp.term1.id + Exp.term2.id
        if Exp.operador == ARITMETICA.ELEVADO : 
            copia = Exp.term1.id
            i = 1
            while i < Exp.term2.val:
                copia += Exp.term1.id
                i += 1
            return copia
    elif isinstance(Exp, OPCadena):
        pass
    elif isinstance(Exp, OPLength):
        pass
    elif isinstance(Exp, OPLowercase):
        pass
    elif isinstance(Exp, OPUppercase):
        pass
    elif isinstance(Exp, OPMergeString):
        return Exp.term1.id + Exp.term2.id
    elif isinstance(Exp, OPElevarString):
        copia = Exp.term1.id
        i = 1
        while i < Exp.term2.val:
            copia += Exp.term1.id
            i += 1
        return copia
    elif isinstance(Exp, OPID):
        pass

# numericas
def resolverNumerica(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPBinaria): 
        
        print('RESOLVIENDO BINARIA')
        print(Exp.term1, ' ', Exp.term2)
        if isinstance(Exp.term1, OPCadena) or isinstance(Exp.term2, OPCadena):
            x = resolverCadena(Exp, tablaSimbolos)
            print('retornando opcadena: ', x)
            return x

        if not isinstance(Exp.term1, OPNum) or not isinstance(Exp.term2, OPNum): 
            print('Binaria sin numeros :C')
            return 0

        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos) 

        if Exp.operador == ARITMETICA.MAS : return exp1 + exp2
        if Exp.operador == ARITMETICA.MENOS : return exp1 - exp2
        if Exp.operador == ARITMETICA.ASTERISCO : return exp1 * exp2
        if Exp.operador == ARITMETICA.DIVIDIDO : return exp1 / exp2
        if Exp.operador == ARITMETICA.MODULO : return exp1 % exp2
        if Exp.operador == ARITMETICA.ELEVADO : return exp1 ** exp2
        else:  return 0
    elif isinstance(Exp, OPNeg):
        pass
    elif isinstance(Exp, OPNativa):#log10, sin, cos, tan, sqrt
        pass
    elif isinstance(Exp, OPNativaLog):
        pass
    elif isinstance(Exp, OPNum):
        pass
    elif isinstance(Exp, OPID):
        return 

def resolverBooleana(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPLogica): 
        pass
    elif isinstance(Exp, OPBool):
        pass
    elif isinstance(Exp, OPID):
        pass


# ------------------------------------------------------------------------- 
# Inicio Auxiliares -------------------------------------------------------
# ------------------------------------------------------------------------- 

def siExiste(nombre, tablaSimbolos: cst.TablaSimbolos):
    aux = tablaSimbolos.obtener(nombre)
    if isinstance(aux, cst.NodoErrorSemantico):
        return False
    else: return True

def añadiraTabla(simbolo: cst.NodoSimbolo):
    global lista_simbolos
    lista_simbolos.append(simbolo)


# ------------------------------------------------------------------------- 
# Inicio Interprete -------------------------------------------------------
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

def intScope(instr: Scope, tablaSimbolos : cst.TablaSimbolos): #ver si cambio este por otro como lo hice en el sintactico
    print('Asignando')
    ambito = instr.scope

    # si lo que esta a la izq del parentesis es un id
    if isinstance(instr.asignacion.nombre[0], OPID):
        
        print(instr.asignacion.valor)
        if isinstance(instr.asignacion, Asignacion) : 
            valor = resolverNumerica(instr.asignacion.valor, tablaSimbolos)
            tipo = type(valor)
            aux = siExiste(instr.asignacion.nombre[0].id, tablaSimbolos)
            if aux:
                # actualizo el valor
                print('siexiste')
            else:
                # creo una nueva variable
                simbolo = cst.NodoSimbolo(instr.asignacion.nombre[0].id, tipo, ambito)
                tablaSimbolos.agregar(simbolo)
                añadiraTabla(simbolo)
        elif isinstance(instr.asignacion, AsignacionTipada):
            valor = resolverNumerica(instr.asignacion.valor, tablaSimbolos)
            aux = siExiste(instr.asignacion.nombre[0].id, tablaSimbolos)
            if aux:
                # actualizo el valor
                print('siexiste')
            else:
                # creo una nueva variable
                print('noexiste')
        

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

