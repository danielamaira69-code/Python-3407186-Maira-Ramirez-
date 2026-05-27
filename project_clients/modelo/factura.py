from pydantic import BaseModel

class Factura(BaseModel):
    id: int
    cliente: str
    total: float
    
class FacturaCrear(BaseModel):
    cliente: str
    total: float 
    
    
    