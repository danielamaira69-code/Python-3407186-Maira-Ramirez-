from fastapi import FastAPI
from modelo.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteEliminar

app = FastAPI()

#lista de clientes en bases de datos 
Lista_clientes: list[Cliente] = []


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


