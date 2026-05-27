from fastapi import FastAPI, HTTPException
from modelo.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteEliminar
from modelo.factura import Factura, FacturaCrear
from modelo.transacciones import Transacciones, TransaccionesCrear
from datetime import datetime



app = FastAPI()

#lista de facturas 
lista_facturas = []

#lista de clientes en bases de datos 
Lista_clientes: list[Cliente] = []

#lista transacciones 
lista_transacciones = []




@app.get("/clientes")
async def listar_clientes():
    if len (Lista_clientes) > 0:
        return {"hay clientes registrados": Lista_clientes}
    else:
        return {"no hay clientes registrados"}
    
@app.get("/clientes/{id}")
async def listar_cliente(id:int):
    for cliente in Lista_clientes:
        if cliente.id == id:
            return cliente 
        
@app.post("/clientes", response_model= Cliente)
async def crear_clientes (datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len (Lista_clientes) +1
    Lista_clientes.append(cliente_val)
    #return {"clientes": cliente_val}
    return cliente_val


@app.put("/clientes/{id}")
async def editar_cliente(id:int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(Lista_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())    
            cliente_val.id = id 
            Lista_clientes[i] = cliente_val
            
    return {"mensaje": "se actualizo el ciente satisfactoriamente.", "Cliente": cliente_val} 


@app.delete("/clientes")
async def eliminar_clientes (id:int, datos_cliente: ClienteEliminar):
    for i, obj_cliente in enumerate(Lista_clientes):
        if obj_cliente.id == id:
            cliente_eliminado = Lista_clientes.pop(i)
    return {"clientes": "cliente eliminado", "cliente": cliente_eliminado}    



#trabajo en casa 
@app.get ("/factura/{cliente_id}", response_model= Factura)
async def crear_facturas(cliente_id: int, datos_factura: FacturaCrear):
    cliente_encontrado= None 
    for c in Lista_clientes:
        if c.id== cliente_id:
            cliente_encontrado= c
            break
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail= f"Cliente con id {cliente_id}, no existe debes crear. ", 
        )
        
#continuacion de crear factura
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = datetime.now()
    factura_val.cliente = cliente_encontrado
    lista_facturas.append(factura_val)
    return factura_val


#transaccion 

@app.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones():
    return lista_transacciones

@app.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int, datos_transaccion: TransaccionesCrear, cliente_id: int
):
    cliente_encontrado = None
    for c in Lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break
        if not cliente_encontrado:
            raise HTTPException(
                status_code=400,
                detail=f"Error 400: No existe un cliente con ese id: {cliente_id}, debes crear el cliente.",)
            
            
#consultar factura 
@app.post(
    "/clientes/{cliente_id}/facturas/{factura_id}/transacciones",
    response_model=Transacciones
)
async def crear_transaccion(
    cliente_id: int,
    factura_id: int,
    datos_transaccion: TransaccionesCrear
):
    factura_encontrada = None
    for f in lista_facturas:
        if f.id == factura_id:
            factura_encontrada = f
            break
        if factura_encontrada:
            if factura_encontrada.cliente.id == cliente_id:
                transaccion_val = Transacciones.model_validate(
                    datos_transaccion.model_dump()
                    )
                transaccion_val.id = len(lista_transacciones) + 1
                transaccion_val.factura_id = factura_id
                lista_transacciones.append(transaccion_val)
