from pydantic import BaseModel
from app.modelos.transacciones import Transacciones
from app.modelos.cliente import Cliente
from datetime import datetime


class FacturaBase(BaseModel):
    fecha: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transacciones: list[Transacciones] = []
    
    def calcular_total(self):
        return sum(t.cantidad * t.vr_unitario for t in self.transacciones)

class FacturaCrear(FacturaBase):
    cliente_id: float   

class FacturaEditar(FacturaBase):
    cliente_id: int

class Factura(FacturaBase):
    id: int | None 
    cliente: Cliente | None
    total: float | None
    
    
    