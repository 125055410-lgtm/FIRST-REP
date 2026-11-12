from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel


app = FastAPI(title="Inventario")


class Dispositivo(BaseModel):
    """Representa un equipo del inventario."""

    nombre: str
    tipo: str
    ip: str
    activo: bool = True

    def apagar(self):
        self.activo = False

    def encender(self):
        self.activo = True

    def etiqueta(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"{self.nombre} ({self.tipo}) - {estado}"


class DispositivoActualizar(BaseModel):
    """Todos los campos opcionales: sirve para actualizaciones parciales."""

    nombre: str | None = None
    tipo: str | None = None
    ip: str | None = None
    activo: bool | None = None


inventario = [
    Dispositivo(nombre="R1", tipo="router", ip="10.0.0.1"),
    Dispositivo(nombre="SW1", tipo="switch", ip="10.0.0.10", activo=False),
    Dispositivo(nombre="FW1", tipo="firewall", ip="10.0.0.254"),
]


def buscar(nombre: str) -> Dispositivo | None:
    """Devuelve el equipo con ese nombre, o None si no existe."""
    for equipo in inventario:
        if equipo.nombre.upper() == nombre.upper():
            return equipo
    return None


@app.get("/dispositivos")
async def listar(activo: bool | None = None):
    """Lista el inventario. Con ?activo=true filtra los equipos en línea."""
    if activo is None:
        return inventario
    return [equipo for equipo in inventario if equipo.activo == activo]


@app.get("/dispositivos/{nombre}")
async def obtener(nombre: str):
    """Devuelve un equipo por su nombre."""
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el equipo {nombre}",
        )
    return equipo


@app.post("/dispositivos", status_code=status.HTTP_201_CREATED)
async def crear(equipo: Dispositivo):
    """Da de alta un equipo nuevo."""
    if buscar(equipo.nombre) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe el equipo {equipo.nombre}",
        )
    inventario.append(equipo)
    return equipo


@app.put("/dispositivos/{nombre}")
async def reemplazar(nombre: str, datos: Dispositivo):
    """Reemplaza todos los datos del equipo. Exige el objeto completo."""
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el equipo {nombre}",
        )
    equipo.nombre = datos.nombre
    equipo.tipo = datos.tipo
    equipo.ip = datos.ip
    equipo.activo = datos.activo
    return equipo


@app.patch("/dispositivos/{nombre}")
async def modificar(nombre: str, datos: DispositivoActualizar):
    """Modifica solo los campos enviados."""
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el equipo {nombre}",
        )
    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(equipo, campo, valor)
    return equipo


@app.delete("/dispositivos/{nombre}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar(nombre: str):
    """Da de baja un equipo."""
    equipo = buscar(nombre)
    if equipo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el equipo {nombre}",
        )
    inventario.remove(equipo)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
