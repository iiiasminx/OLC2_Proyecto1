#  ------------------------------------------INICIO--------------------------------------------------
#----------------------------------------------------------------------------------------------------

class Instruccion:
    '''This is an abstract class'''


class Impresion(Instruccion):
    def __init__(self,  texto) :
        self.texto = texto

class Declaracion(Instruccion):
    def __init__(self,  nombre, scope =0) :
        self.nombre = nombre
        self.scope = scope

class Asignacion(Instruccion):
    def __init__(self,  nombre, valor, scope =0) :
        self.nombre = nombre
        self.valor = valor
        self.scope = scope
        

# Creacion de Funciones

class DefFuncion(Instruccion):
    def __init__(self,  nombre, params, instrucciones) :
        self.nombre = nombre
        self.params = params
        self.instrucciones = instrucciones

class FParse(Instruccion):
    def __init__(self,  term1, term2) :
        self.term1 = term1
        self.term2 = term2

class FTrunc(Instruccion):
    def __init__(self,  term1) :
        self.term1 = term1

class FFloat(Instruccion):
    def __init__(self,  term1) :
        self.term1 = term1

class FString(Instruccion):
    def __init__(self,  term1) :
        self.term1 = term1

class Ftypeof(Instruccion):
    def __init__(self,  term1) :
        self.term1 = term1


class LlamadaFuncion(Instruccion):
    def __init__(self,  funcion, params) :
        self.funcion = funcion
        self.params = params

#condicionales

class FIF(Instruccion):
    def __init__(self,  oplog, instruccionesv, instruccionesF) :
        self.oplog = oplog
        self.instruccionesv = instruccionesv
        self.instruccionesF = instruccionesF

class FElseIF(Instruccion):
    def __init__(self,  oplog, instruccionesv, instruccionesF) :
        self.oplog = oplog
        self.instruccionesv = instruccionesv
        self.instruccionesF = instruccionesF

class FELSE(Instruccion):
    def __init__(self,  instrucciones) :
        self.instrucciones = instrucciones

class FWhile(Instruccion):
    def __init__(self,  oplog, instrucciones) :
        self.oplog = oplog
        self.instrucciones = instrucciones

class FFor(Instruccion):
    def __init__(self,  rango, instrucciones) :
        self.rango = rango
        self.instrucciones = instrucciones

class SBreak(Instruccion):
    pass

class SContinue(Instruccion):
    pass

class SReturn(Instruccion):
    def __init__(self,  contenido) :
        self.contenido = contenido

#struct

class DeclStruct(Instruccion):
    def __init__(self,  nombre, caracteristicas, tipo=0) :
        self.nombre = nombre
        self.caracteristicas = caracteristicas
        self.tipo = tipo

class ConstruccionStruct(Instruccion):
    def __init__(self,  nombre, tipoStruct, caracteristicas) :
        self.nombre = nombre
        self.caracteristicas = caracteristicas
        self.tipoStruct = tipoStruct

class AsignacionAtributosStruct(Instruccion):
    def __init__(self,  struct, atributo, valor) :
        self.struct = struct
        self.atributo = atributo
        self.valor = valor

class AccesoAtributo(Instruccion):
    def __init__(self,  atributo, valor) :
        self.atributo = atributo
        self.valor = valor


