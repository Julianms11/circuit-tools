from imps import Impedancia
from Fuente import FuentesY, FuentesD
from Circuitos import DeltaDelta, EstrellaEstrella, DeltaEstrella, EstrellaDelta, EstrellaEstrella3Hilos
import cmath as cm


V =120
ang = 0
Z = Impedancia([70-30j, 66+38j, 30+70j]).Z

fuentes = FuentesY(V, ang)
circuito = EstrellaDelta(fuentes, Z)

print(circuito)
