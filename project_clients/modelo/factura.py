from pydantic import BaseModel

class Factura(BaseModel):
    
    id: int
    fecha: int 
    total:int 
    cliente_id: int 
    