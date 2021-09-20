#  ------------------------------------------INICIO--------------------------------------------------
#----------------------------------------------------------------------------------------------------

class Instruccion:
    '''This is an abstract class'''


class Impresion:
    def __init__(self,  texto) :
        self.texto = texto

class Asignacion:
    def __init__(self,  nombre, valor, scope =0) :
        self.nombre = nombre
        self.valor = valor
        self.scope = scope
        

# Creacion de Funciones

class DefFuncion:
    def __init__(self,  nombre, params, instrucciones) :
        self.nombre = nombre
        self.params = params
        self.instrucciones = instrucciones

class FParse:
    def __init__(self,  term1, term2) :
        self.term1 = term1
        self.term2 = term2

class FTrunc:
    def __init__(self,  term1) :
        self.term1 = term1

class FFloat:
    def __init__(self,  term1) :
        self.term1 = term1

class FString:
    def __init__(self,  term1) :
        self.term1 = term1

class Ftypeof:
    def __init__(self,  term1) :
        self.term1 = term1


#condicionales

class FIF:
    def __init__(self,  oplog, instrucciones) :
        self.oplog = oplog
        self.instrucciones = instrucciones

class FElseIF:
    def __init__(self,  oplog, instrucciones) :
        self.oplog = oplog
        self.instrucciones = instrucciones

class FELSE:
    def __init__(self,  instrucciones) :
        self.instrucciones = instrucciones

class FWhile:
    def __init__(self,  oplog, instrucciones) :
        self.oplog = oplog
        self.instrucciones = instrucciones

class FFor:
    def __init__(self,  rango, instrucciones) :
        self.rango = rango
        self.instrucciones = instrucciones

#struct

class DeclStruct:
    def __init__(self,  nombre, caracteristicas, tipo=0) :
        self.nombre = nombre
        self.caracteristicas = caracteristicas
        self.tipo = tipo

class ConstruccionStruct:
    def __init__(self,  nombre, tipoStruct, caracteristicas) :
        self.nombre = nombre
        self.caracteristicas = caracteristicas
        self.tipoStruct = tipoStruct

class AsignacionAtributosStruct:
    def __init__(self,  struct, atributo, valor) :
        self.struct = struct
        self.atributo = atributo
        self.valor = valor

class AccesoAtributo:
    def __init__(self,  atributo, valor) :
        self.atributo = atributo
        self.valor = valor


