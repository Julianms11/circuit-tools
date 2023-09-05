import cmath as cm
import numpy as np
from equivalencias import *
from Fuente import *

##################################################################################

# V_fuente = cm.rect(208, 0)
# V_carga = cm.rect(205.94, 0)
# I = cm.rect(0.20594, 0)

# potencia_carga = V_carga * I.conjugate()
# potencia_fuente = V_fuente * I.conjugate()
# print("Potencia fuente:",potencia_fuente)
# print("Potencia carga:",potencia_carga)
# eficiencia = (potencia_carga / potencia_fuente) * 100
# print("Eficiencia:", eficiencia)

# regulacion = ((np.abs(V_fuente)-np.abs(V_carga))/np.abs(V_fuente)) * 100

# print("Regulacion:", regulacion)

##################################################################################

# p_real = 4000
# factor_potencia = 0.83

# potencia_aparente = p_real / factor_potencia

# potencia_reactiva = potencia_aparente * np.sin(np.arccos(factor_potencia))

# potencia_compleja = p_real + potencia_reactiva * 1j

# print("Potencia compleja:", potencia_compleja+100)

# print("Potencia aparente:", potencia_aparente)

# print("Potencia reactiva:", potencia_reactiva)

# I_conj = potencia_compleja / 400

# I = I_conj.conjugate()

# print("Corriente:", I)

# V_rw = (100/I_conj)

# print("V_rw:", V_rw)

# Rw = V_rw/I

# print("Rw:", Rw)

##################################################################################

Zs = [-100j, 100, 50 + 50j]

Zs_paralelo = paralelo(Zs)

# print(Zs_paralelo)

fuentes = FuentesD(400, 0)
fuentes.toY()
fuentesY = [fuentes.VAN, fuentes.VBN, fuentes.VCN]

f_fase1 = cm.rect(fuentesY[0][0], np.radians(fuentesY[0][1]))
iAa = f_fase1/50

pot = f_fase1*iAa.conjugate()

print(f_fase1)

print(cm.polar(f_fase1/50)[0], np.degrees(cm.polar(f_fase1/50)[1]))

print(pot*3)

##################################################################################