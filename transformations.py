import numpy as np
import cmath
from Fuente import FuentesY, FuentesD

# Transformar configuración delta a estrella de impedancias
def imp_DtoY(Z):
    Zab = Z[0]
    Zbc = Z[1]
    Zca = Z[2]
    Zsum = Zab + Zbc + Zca
    Za = (Zab*Zca)/Zsum
    Za = round(Za.real)+ round(Za.imag)*1j
    Zb = (Zbc*Zab)/Zsum
    Zb = round(Zb.real)+ round(Zb.imag)*1j
    Zc = (Zca*Zbc)/Zsum
    Zc = round(Zc.real)+ round(Zc.imag)*1j
    return [Za, Zb, Zc]

# Transformar configuración estrella a delta de impedancias
def imp_YtoD(Z):
    Za = Z[0]
    Zb = Z[1]
    Zc = Z[2]
    Znum = Za*Zb + Zb*Zc + Zc*Za
    Zab = Znum/Zc
    Zab = round(Zab.real)+ round(Zab.imag)*1j
    Zbc = Znum/Za
    Zbc = round(Zbc.real)+ round(Zbc.imag)*1j
    Zca = Znum/Zb
    Zca = round(Zca.real)+ round(Zca.imag)*1j
    return [Zab, Zbc, Zca]

