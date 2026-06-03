from pydantic import BaseModel

class TransaccionesBase(BaseModel):
    descripcion: str
    cantidad: int
    vr_unitario: float

class crearTransacciones(TransaccionesBase):
    pass

class editarTransacciones(TransaccionesBase):
    pass

class Transacciones(TransaccionesBase):
    id: int | None