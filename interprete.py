# importo todo de todos lados
from gramatica import fighting, tokens
import cst as cst
from operaciones import *
from semantico  import *
from sintactico import * 
import math

lista_simbolos = [] # acá van todos los valores que se hayan declarado
arbol =[]
ts_global = cst.TablaSimbolos()
contaerrores = 0
listasemanticos = []
textoimpresion = ""
contabucle = 0

def fightingfinal(texto):
    exportef = fighting2(texto)
    global arbol 
    arbol = exportef.arbol
    global lista_simbolos
    lista_simbolos = []
    global listasemanticos
    listasemanticos = []
    global contaerrores
    contaerrores = 0
    global textoimpresion
    textoimpresion = "Lo que imprimo va acá :3 ---------------------\n"
    global ts_global
    ts_global.simbolos.clear()

    
    procesarInstrucciones(arbol, ts_global)

    #print(ts_global.simbolos)
    exportef.interpretacion = textoimpresion
    exportef.tabla_simbolos = lista_simbolos
    exportef.listasemanticos = listasemanticos

    return exportef

def procesarInstrucciones(ast, tablaSimbolos : cst.TablaSimbolos):
    contador = 1
    print('\n')
    for instruccion in ast:
        print(contador)
        contador += 1
        global contabucle
        contabucle = 0
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

        
        print('\n', instruccion)

# ------------------------------------------------------------------------- 
# Inicio Auxiliares -------------------------------------------------------
# ------------------------------------------------------------------------- 

def siExiste(nombre, tablaSimbolos: cst.TablaSimbolos):
    aux = tablaSimbolos.obtener(nombre)
    if isinstance(aux, cst.NodoErrorSemantico):
        return False
    else: return aux

def siExisteHardcore(nombre, tablaSimbolos: cst.TablaSimbolos):
    aux = tablaSimbolos.obtener(nombre)
    if isinstance(aux, cst.NodoErrorSemantico):
        desc = "Error semántico - no se encuentra la variable: " + str(nombre)
        global contaerrores
        nuevo = cst.NodoErrorSemantico(desc)
        nuevo.contador = contaerrores
        contaerrores += 1
        global listasemanticos
        listasemanticos.append(nuevo)
        return False
    else: return aux

def añadiraTabla(simbolo: cst.NodoSimbolo):
    global lista_simbolos
    lista_simbolos.append(simbolo)

def getTipo(tipo: OPType):
    if isinstance(tipo.id, OPID):
        return tipo.id.id
    else :
        return tipo.id
    
def tipoVariable(var):
    x = str(type(var))
    if 'str' in x:
        return 'String'
    elif 'list' in x:
        return 'Array'
    elif 'int' in x:
        return 'Int64'
    elif 'float' in x:
        return 'Float64'
    elif 'dict' in x:
        return 'Struct'
    elif 'bool' in x:
        return 'Bool'
    elif 'None' in x:
        return 'None'

def errordeTipos(nombre_instruccion):
    desc = "Error semántico con la instruccion: "+ nombre_instruccion +". Los tipos no son compatibles"
    global contaerrores
    nuevo = cst.NodoErrorSemantico(desc)
    nuevo.contador = contaerrores
    contaerrores += 1
    global listasemanticos
    listasemanticos.append(nuevo)

def errorEquis(nombre_instruccion, razon):
    desc = "Error semántico con la instruccion: "+ nombre_instruccion +". "+ razon
    global contaerrores
    nuevo = cst.NodoErrorSemantico(desc)
    nuevo.contador = contaerrores
    contaerrores += 1
    global listasemanticos
    listasemanticos.append(nuevo)
# ------------------------------------------------------------------------- 
# Inicio Operaciones ------------------------------------------------------
# ------------------------------------------------------------------------- 

def resolverCadena(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPBinaria):
        exp1 = resolverCadena(Exp.term1, tablaSimbolos)
        if isinstance(Exp.term2, OPNum):
            exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
        else: exp2 = resolverCadena(Exp.term2, tablaSimbolos) 

        print(Exp.term2)
        print(tipoVariable(exp2), ' ', exp2)

        if exp1 == 'Failed' or exp2 == 'Failed':
            return None

        if Exp.operador == ARITMETICA.ASTERISCO : 
            return exp1 + str(exp2)
        if Exp.operador == ARITMETICA.ELEVADO and tipoVariable(exp2) == 'Int64' and exp2 != None: 
            
            copia = str(exp1)
            i = 1
            while i < exp2:
                copia += str(exp1)
                i += 1
            return copia
    elif isinstance(Exp, OPCadena):
        return Exp.id
    elif isinstance(Exp, OPLength):
        cad = resolverCadena(Exp.term1, tablaSimbolos)
        if cad == 'Failed':
            return None
        
        return len(str(cad))
    elif isinstance(Exp, OPLowercase):
        cad = resolverCadena(Exp.term1, tablaSimbolos)
        if cad == 'Failed':
            return None
        
        return str(cad).lower()
    elif isinstance(Exp, OPUppercase):
        cad = resolverCadena(Exp.term1, tablaSimbolos)
        if cad == 'Failed':
            return None
        
        return str(cad).upper()
    elif isinstance(Exp, OPMergeString):
        exp1 = resolverCadena(Exp.term1, tablaSimbolos)
        if isinstance(Exp.term2, OPNum):
            exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
        else: exp2 = resolverCadena(Exp.term2, tablaSimbolos) 

        print(Exp.term2)
        print(tipoVariable(exp2), ' ', exp2)

        if exp1 == 'Failed' or exp2 == 'Failed':
            return None

        return exp1 + str(exp2)
    elif isinstance(Exp, OPElevarString):
        try: 
            exp1 = resolverCadena(Exp.term1, tablaSimbolos)
            if isinstance(Exp.term2, OPNum):
                exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
            else: exp2 = resolverCadena(Exp.term2, tablaSimbolos) 

            print(Exp.term2)
            print(tipoVariable(exp2), ' ', exp2)

            if exp1 == 'Failed' or exp2 == 'Failed':
                return None
            if tipoVariable(exp2) == 'Int64' and exp2 != None: 
            
                copia = str(exp1)
                i = 1
                while i < exp2:
                    copia += str(exp1)
                    i += 1
                return copia        
        except: return 'Failed'
    elif isinstance(Exp, OPID):
        x = siExisteHardcore(Exp.id, tablaSimbolos)
        if x:

            return x.valor
        else: 
            print('FALLA EN ID')
            return'Failed'
    else:
        print('viendo si se va a las lógicas')
        global contabucle
        contabucle += 1
        if contabucle > 20:
            return None
        return resolverBooleana(Exp, tablaSimbolos)


# numericas
def resolverNumerica(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPBinaria): 
        
        print('RESOLVIENDO BINARIA')
        print(Exp.term1, ' ', Exp.term2)
        if isinstance(Exp.term1, OPCadena) or isinstance(Exp.term2, OPCadena):
            x = resolverCadena(Exp, tablaSimbolos)
            print('retornando opcadena: ', x)
            return x

       # if not isinstance(Exp.term1, OPNum) and not isinstance(Exp.term2, OPNum): 
       #     if not isinstance(Exp.term1, OPBinaria) and not isinstance(Exp.term2, OPBinaria):
       #         print('metiendome al if2')
       #         return resolverCadena(Exp, tablaSimbolos)

        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos) 

        if exp1 == 'Failed' or exp2 == 'Failed':
            return None

        if tipoVariable(exp1) != 'Int64' and tipoVariable(exp2) != 'Int64':
            if tipoVariable(exp1) != 'Float64' and tipoVariable(exp2) != 'Float64':
                print('metiendome al if3')
                return resolverCadena(Exp, tablaSimbolos)

        if Exp.operador == ARITMETICA.MAS : return exp1 + exp2
        if Exp.operador == ARITMETICA.MENOS : return exp1 - exp2
        if Exp.operador == ARITMETICA.ASTERISCO : return exp1 * exp2
        if Exp.operador == ARITMETICA.DIVIDIDO : return exp1 / exp2
        if Exp.operador == ARITMETICA.MODULO : return exp1 % exp2
        if Exp.operador == ARITMETICA.ELEVADO : return exp1 ** exp2
        else:  return None
    elif isinstance(Exp, OPNeg):
        exp1 = resolverNumerica(Exp.term, tablaSimbolos)
        if exp1 == 'Failed':
            return None

        return - exp1
    elif isinstance(Exp, OPNativa):#log10, sin, cos, tan, sqrt
        exp1 = resolverNumerica(Exp.term, tablaSimbolos)
        if exp1 == 'Failed':
            return None

        if Exp.tipo == MATH.LOG10 : return math.log10(exp1)
        if Exp.tipo == MATH.SIN : return math.sin(exp1)
        if Exp.tipo == MATH.COS : return math.cos(exp1)
        if Exp.tipo == MATH.TAN : return math.tan(exp1)
        if Exp.tipo == MATH.SQRT : return math.sqrt(exp1)
    elif isinstance(Exp, OPNativaLog):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos)
        if exp1 == 'Failed' or exp2 == 'Failed':
            return None

        return math.log(exp2, exp1)
    elif isinstance(Exp, FParse):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        exp2 = resolverNumerica(Exp.term2, tablaSimbolos)

        if exp1 == 'Failed' or exp2 == 'Failed':
            return None

        if exp1 == 'Float64':
            try:  
                return float(exp2)
            except:
                errordeTipos('Parse')
            return None
        elif exp1 == 'Int64':
            try:  
                return int(exp2)
            except:
                errordeTipos('Parse')
            return None
        else:
            errordeTipos('Parse')
            return None
    elif isinstance(Exp, FTrunc):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        if exp1 == 'Failed':
            return None

        try:  
            return math.trunc(float(exp1))
        except:
            errordeTipos('Trunc')
            return None      
    elif isinstance(Exp, FFloat):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        if exp1 == 'Failed':
            return None

        try:  
            return float(exp1)
        except:
            errordeTipos('Float')
            return None        
    elif isinstance(Exp, FString):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        if exp1 == 'Failed':
            return None

        return str(exp1)
    elif isinstance(Exp, Ftypeof):
        exp1 = resolverNumerica(Exp.term1, tablaSimbolos)
        if exp1 == 'Failed':
            return None

        return tipoVariable(exp1)
    elif isinstance(Exp, OPNum):
        return Exp.val
    elif isinstance(Exp, OPID):
        x = siExisteHardcore(Exp.id, tablaSimbolos)
        if x:
            return x.valor
        else: 
            print('FALLA EN ID')
            return'Failed'
    elif isinstance(Exp, OPType):
        return getTipo(Exp)
    elif isinstance(Exp, list):
        #print('Acá hay un arreglol')
        aux = []
        for term in Exp:
            if isinstance(term, OPNothing):
                return aux

            if isinstance(term, OPID):
                aux.append(term.id)
                continue
        
            x = resolverNumerica(term, tablaSimbolos)
            aux.append(x)
        return aux
    else: 
        print('viendo si se va a las cadenas')
        global contabucle
        contabucle += 1
        if contabucle > 20:
            return None
        return resolverCadena(Exp, tablaSimbolos)


def resolverBooleana(Exp, tablaSimbolos: cst.TablaSimbolos):
    if isinstance(Exp, OPLogica): 
        print('RESOLVIENDO LOGICA')
        print(Exp.term1, ' ', Exp.term2)

        exp1 = resolverBooleana(Exp.term1, tablaSimbolos)
        exp2 = resolverBooleana(Exp.term2, tablaSimbolos) 

        if exp1 == 'Failed' or exp2 == 'Failed':
            return None

        if Exp.operador == LOGICA.AND : return exp1 and exp2
        if Exp.operador == LOGICA.OR : return exp1 or exp2
        if Exp.operador == LOGICA.MAYORQUE : return exp1 > exp2
        if Exp.operador == LOGICA.MENORQUE : return exp1 < exp2
        if Exp.operador == LOGICA.MAYORIWAL : return exp1 >= exp2
        if Exp.operador == LOGICA.MENORIWAL : return exp1 <= exp2
        if Exp.operador == LOGICA.IWAL : return exp1 == exp2
        if Exp.operador == LOGICA.DISTINTO : return exp1 != exp2
        else:  return None
    elif isinstance(Exp, OPBool):
        if Exp.id == 'false':
            return False
        return True
    elif isinstance(Exp, OPNum):
        return Exp.val
    elif isinstance(Exp, OPCadena):
        return Exp.id
    elif isinstance(Exp, OPID):
        x = siExisteHardcore(Exp.id, tablaSimbolos)
        if x:
            return x.valor
        else: 
            print('FALLA EN ID')
            return'Failed'
    else: 
        print('viendo si se va a los numeros')
        global contabucle
        contabucle += 1
        if contabucle > 20:
            return None
        return resolverNumerica(Exp, tablaSimbolos)


# ------------------------------------------------------------------------- 
# Inicio Interprete -------------------------------------------------------
# ------------------------------------------------------------------------- 

# Impresion ---------------------------------------------------------------
# -------------------------------------------------------------------------
def intImpresion(instr, tablaSimbolos: cst.TablaSimbolos):
    print('impresion')
    aux = ""

    for instruccion in instr.texto:
        aux += str(resolverNumerica(instruccion, tablaSimbolos))

    global textoimpresion
    textoimpresion += aux

def intImpresionLN(instr, tablaSimbolos : cst.TablaSimbolos):
    print('impresionLN')
    aux = ""

    for instruccion in instr.texto:
        aux += str(resolverNumerica(instruccion, tablaSimbolos))

    aux += "\n"
    global textoimpresion
    textoimpresion += aux

#variables ----------------------------------------------------------------
# -------------------------------------------------------------------------
def intDeclaracion(instr, tablaSimbolos : cst.TablaSimbolos): #ver si necesito más de estas
    print('intDeclaracion')
def intScope(instr: Scope, tablaSimbolos : cst.TablaSimbolos): #ver si cambio este por otro como lo hice en el sintactico
    print('Asignando')
    ambito = instr.scope

    #si lo que está a la izq es un array 
    if isinstance(instr.asignacion.nombre, LlamadaArr):
        print('ESUNARRAY')
        print(instr.asignacion.nombre.nombre, ' , ', instr.asignacion.nombre.inds)
        valor = resolverNumerica(instr.asignacion.valor, tablaSimbolos)

        arr_indices = []
        contadimensiones = 0
        for indice in instr.asignacion.nombre.inds:
            x = resolverNumerica(indice, tablaSimbolos)
            print (tipoVariable(x), ' , ', x)

            if tipoVariable(x) != 'Int64':
                errordeTipos('Asignacion de Array')
                return None

            arr_indices.append(x)
            contadimensiones += 1

        arr = siExisteHardcore(instr.asignacion.nombre.nombre, tablaSimbolos)
        if arr == False or not arr:
            return None
        
        placeholder = ""
        try:
            if contadimensiones == 0: return errordeTipos('Asignación a arreglo')
            elif contadimensiones == 1: 
                placeholder = arr.valor[arr_indices[0]]
                arr.valor[arr_indices[0]] = valor
            elif contadimensiones == 2:
                placeholder = arr.valor[arr_indices[0]][arr_indices[1]]
                arr.valor[arr_indices[0]][arr_indices[1]] = valor
            elif contadimensiones == 3: 
                placeholder = arr.valor[arr_indices[0]][arr_indices[1]][arr_indices[2]]
                arr.valor[arr_indices[0]][arr_indices[1]][arr_indices[2]] = valor
        except Exception as e:
            print(e)
            return errorEquis('Asignación a arreglo', str(e))

        print('valor de arr izq: ', placeholder)
        if placeholder == "":
            return
        arr.nota = 'Actualización Array'
        tablaSimbolos.actualizar(arr)
        añadiraTabla(arr)

    # si lo que esta a la izq del parentesis es un id
    elif isinstance(instr.asignacion.nombre[0], OPID):
        
        print(instr.asignacion.valor)
        valor = resolverNumerica(instr.asignacion.valor, tablaSimbolos)
        aux = siExiste(instr.asignacion.nombre[0].id, tablaSimbolos)
        if isinstance(instr.asignacion, Asignacion) : 
            tipo = tipoVariable(valor)
            if aux:
                print('actualizando')
                # actualizo el valor
                simbolo = cst.NodoSimbolo(instr.asignacion.nombre[0].id, tipo, ambito, valor)
                simbolo.nota = 'Actualización'
                tablaSimbolos.actualizar(simbolo)
                añadiraTabla(simbolo)
            else:
                print('nuevo')
                # creo una nueva variable
                simbolo = cst.NodoSimbolo(instr.asignacion.nombre[0].id, tipo, ambito, valor)
                tablaSimbolos.agregar(simbolo)
                añadiraTabla(simbolo)
        elif isinstance(instr.asignacion, AsignacionTipada): 
            if aux:
                print('actualizando')
                # actualizo el valor
                simbolo = cst.NodoSimbolo(instr.asignacion.nombre[0].id, getTipo(instr.asignacion.tipo), ambito, valor)
                simbolo.nota = 'Actualización'
                tablaSimbolos.actualizar(simbolo)
                añadiraTabla(simbolo)
            else:
                print('nuevo')
                # creo una nueva variable
                simbolo = cst.NodoSimbolo(instr.asignacion.nombre[0].id, getTipo(instr.asignacion.tipo), ambito, valor)
                tablaSimbolos.agregar(simbolo)
                añadiraTabla(simbolo)
        

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

