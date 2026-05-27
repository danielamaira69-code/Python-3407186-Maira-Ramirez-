from pydantic import BaseModel

class Transacciones(BaseModel):
    id: int
    tipo: str
    valor: float
    
class TransaccionesCrear(BaseModel):
    tipo: str
    valor: float