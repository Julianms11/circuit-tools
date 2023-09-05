from imps import Impedancia
from Fuente import FuentesY, FuentesD
from Circuitos import DeltaDelta, EstrellaEstrella, DeltaEstrella, EstrellaDelta, EstrellaEstrella3Hilos


V =120
ang = 0

# Cargas
# Z = Impedancia([70-30j, 66+38j, 30+70j]).Z 
# Z = Impedancia(90+120j).Z
# Z = Impedancia(30+40j).Z
Z = Impedancia([30+10j, 30-10j, 10+30j]).Z


# Fuentes
fuentes = FuentesY(V, ang)
# fuentes = FuentesD(V, ang)

# Circuitos
# circuito = DeltaDelta(fuentes, Z)
# circuito = EstrellaEstrella(fuentes, Z)
# circuito = DeltaEstrella(fuentes, Z)
# circuito = EstrellaDelta(fuentes, Z)
circuito = EstrellaEstrella3Hilos(fuentes, Z)

print(circuito)
