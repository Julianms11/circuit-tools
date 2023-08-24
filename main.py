from transformations import *
from Fuente import FuentesY, FuentesD
from Circuitos import DeltaDelta, EstrellaEstrella, DeltaEstrella, EstrellaEstrella3Hilos


V =120
ang = 0
Z = [30+40j, 30+40j, 30+40j]

fuentes = FuentesY(V, ang)
circuito = EstrellaEstrella(fuentes, Z)

print(circuito)
