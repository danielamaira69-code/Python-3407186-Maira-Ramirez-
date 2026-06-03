from pydantic import BaseModel

class ClienteBase (BaseModel):
    #atribitos
    nombre: str
    edad: int
    descripcion: str | None
    
class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass


class Cliente(ClienteBase):
    id : int | None = None 


    
    