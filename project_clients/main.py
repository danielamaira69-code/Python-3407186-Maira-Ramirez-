from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.modelos.cliente import Cliente, ClienteCrear, ClienteEditar
from app.modelos.transacciones import crearTransacciones,editarTransacciones,Transacciones
from app.modelos.factura import  Factura, FacturaCrear, FacturaEditar


app= FastAPI()

#lista clientes en bd

lista_clientes: list [Cliente] = []

@app.get("/clientes")
async def listar_clientes():
    return {"Cliente": lista_clientes}

@app.get("/clientes/{id}")
async def listar_cliente(id:int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente


@app.post("/clientes", response_model = Cliente)
async def crear_clientes(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len(lista_clientes)+1
    
    lista_clientes.append(cliente_val)
    return cliente_val


@app.put("/clientes/{id}")
async def editar_clientes(id:int, datos_cliente:ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):  
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val 
            return {"mensaje": "Se actualizo el cliente correctamente", "Cliente": cliente_val}
    



    
@app.delete("/clientes/{id}")
async def listar_cliente(id:int):
    for i, obj_cliente in enumerate(lista_clientes):  
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(obj_cliente.model_dump())
            cliente_val.id = id
            lista_clientes.pop(i) 
            return {"mensaje" : "se elmino correctamente","Clientes":cliente_val}


#actividad en casa parte 2

#1. factura

lista_factura: list [Factura] = []

@app.get ("/factura")
async def listar_factura():
    return {"Factura": lista_factura}

@app.get ("/factura/{id}")
async def listar_factura_id(id: int):
    for factura in lista_factura:
        if factura.id == id:
            return factura
    return {"mensaje": "Factura no encontrada"}

@app.post("/factura", response_model=Factura)
async def crear_factura(datos_factura: FacturaCrear):
    # buscar el cliente
    cliente = next((c for c in lista_clientes if c.id == datos_factura.cliente_id), None)
    
    if cliente is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Cliente no encontrado"}
        )

    factura_val = Factura(
        id=len(lista_factura) + 1,
        cliente=cliente,
        transacciones=datos_factura.transacciones,
        total=0
    )
    factura_val.total = factura_val.calcular_total()
    lista_factura.append(factura_val)
    return factura_val



@app.put("/factura/{id}")
async def editar_factura(id: int, datos_factura: FacturaEditar):
    cliente = next((c for c in lista_clientes if c.id == datos_factura.cliente_id), None)
    factura = next((f for f in lista_factura if f.id == id), None)
    
    if cliente is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Cliente no encontrado"}
        )

    if factura is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Factura no encontrada"}
        )
    
    for i, obj_factura in enumerate(lista_factura):  
        if obj_factura.id == id:
            factura_val = Factura(
                id=id,
                cliente=cliente,
                transacciones=datos_factura.transacciones,
                total=0
            )
            factura_val.total = factura_val.calcular_total()  
            lista_factura[i] = factura_val 
            return {"mensaje": "Se actualizó la factura correctamente", "Factura": factura_val}


@app.delete("/factura/{id}")
async def eliminar_factura(id: int):
    for i, obj_factura in enumerate(lista_factura):  
        if obj_factura.id == id:
            factura_val = Factura.model_validate(obj_factura.model_dump())
            factura_val.id = id
            lista_factura.pop(i) 
            return {"mensaje" : "Se eliminó correctamente","Factura":factura_val}
    return {"mensaje": "Factura no encontrada"}


#2. transacciones 



@app.get("/factura/{id}/transacciones")
async def listar_transacciones(id: int):
    factura = next((f for f in lista_factura if f.id == id), None)
    
    if factura is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Factura no encontrada"}
        )
    
    return {"transacciones": factura.transacciones}

@app.post("/factura/{id}/transacciones")
async def agregar_transaccion(id: int, datos_transaccion: crearTransacciones):
    factura = next((f for f in lista_factura if f.id == id), None)
    
    if factura is None:
        return JSONResponse(
            status_code=404,
            content={"error": "no se encontro la factura"}
        )
    
    transaccion_val = Transacciones(
        id=len(factura.transacciones) + 1,
        cantidad=datos_transaccion.cantidad,
        vr_unitario=datos_transaccion.vr_unitario,
        descripcion=datos_transaccion.descripcion
    )
    
    factura.transacciones.append(transaccion_val)
    factura.total = factura.calcular_total()
    
    return {"mensaje": "Se agrego la transaccion", "factura": factura}


@app.put("/factura/{id}/transacciones/{transacciones_id}")
async def editar_transacciones(id: int,transacciones_id: int, datos_transaccion: editarTransacciones):
    factura = next((f for f in lista_factura if f.id == id), None)
    
    if factura is None:
        return JSONResponse(
            status_code=404,
            content={"error": "No se encontro la transaccion"}
        )

    for t in factura.transacciones:
        if t.id == transacciones_id:
            t.cantidad = datos_transaccion.cantidad
            t.vr_unitario = datos_transaccion.vr_unitario
            t.descripcion = datos_transaccion.descripcion

            factura.total = factura.calcular_total()
            return {"mensaje": "Se actualizo la transaccion", "factura": factura}
        
    return {"mensaje": "No se encontro la transaccion"}
    
@app.delete("/factura/{id}/transacciones/{transacciones_id}")
async def eliminar_transacciones(id: int, transacciones_id: int):
    factura = next((f for f in lista_factura if f.id == id), None)
    
    if factura is None:
        return JSONResponse(
            status_code=404,
            content={"error": "No se encontro la transaccion"}
        )

    for t in factura.transacciones:
        if t.id == transacciones_id:
            factura.transacciones.remove(t)
            factura.total = factura.calcular_total()
            return {"mensaje": "Se elimino la transaccion", "factura": factura}
        
    return {"mensaje": "No se encontro la transaccion"}
