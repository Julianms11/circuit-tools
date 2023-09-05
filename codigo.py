#Repositorio de github: github.com/Julianms11/circuit-tools
import numpy as np
import cmath as cm

### Archivo equivalencias.py ###
# import numpy as np

def paralelo(Z: list):
    Imps = np.ones(len(Z), dtype=complex)
    for i in range(len(Z)):
        Imps[i] = 1/Z[i]
    ImpPar = 1/np.sum(Imps)
    return ImpPar

def serie(Z: list):
    return np.sum(Z)
####################################################
### Archivo imps.py ###
class Impedancia:
    def __init__(self, Z):
        if type(Z) == list:
            self.Z = Z
        else:
            self.Z = [Z, Z, Z]
    
    # Transformar configuración delta a estrella de impedancias
    @classmethod
    def imp_DtoY(cls,Z):
        Zab = Z[0]
        Zbc = Z[1]
        Zca = Z[2]
        Zsum = Zab + Zbc + Zca
        Za = (Zab*Zca)/Zsum
        Za = round(Za.real,6)+ round(Za.imag,6)*1j
        Zb = (Zbc*Zab)/Zsum
        Zb = round(Zb.real,6)+ round(Zb.imag,6)*1j
        Zc = (Zca*Zbc)/Zsum
        Zc = round(Zc.real,6)+ round(Zc.imag,6)*1j
        return [Za, Zb, Zc]

    # Transformar configuración estrella a delta de impedancias
    @classmethod
    def imp_YtoD(cls,Z):
        Zan = Z[0]
        Zbn = Z[1]
        Zcn = Z[2]
        Znum = Zan*Zbn + Zbn*Zcn + Zcn*Zan
        Zab = Znum/Zcn
        Zab = round(Zab.real,6)+ round(Zab.imag,6)*1j
        Zbc = Znum/Zan
        Zbc = round(Zbc.real,6)+ round(Zbc.imag,6)*1j
        Zca = Znum/Zbn
        Zca = round(Zca.real,6)+ round(Zca.imag,6)*1j
        return [Zab, Zbc, Zca]
####################################################
### Archivo Fuente.py ###
# import numpy as np
# import cmath as cm
# Fuentes en configuarción Y
class FuentesY:
    def __init__(self, V, ang):
        self.VAN = [V, ang]
        self.VBN = [V, ang-120]
        self.VCN = [V, ang-240]

    def __str__(self):
        return str(self.V)
    
    def polar(self):
        return [self.VAN, self.VBN, self.VCN]
    
    def rect(self):
        va = cm.rect(self.VAN[0], np.radians(self.VAN[1]))
        vb = cm.rect(self.VBN[0], np.radians(self.VBN[1]))
        vc = cm.rect(self.VCN[0], np.radians(self.VCN[1]))
        return [va, vb, vc]
    
    def toD(self):
        self.VAB = [self.VAN[0] * np.sqrt(3), self.VAN[1]+30]
        self.VBC = [self.VBN[0] * np.sqrt(3), self.VBN[1]+30]
        self.VCA = [self.VCN[0] * np.sqrt(3), self.VCN[1]+30]

    
# Fuentes en configuarción delta
class FuentesD:
    def __init__(self, V, ang):
        self.VAB = [V, ang]
        self.VBC = [V, ang-120]
        self.VCA = [V, ang+120]

    def __str__(self):
        return str(self.V)

    def polar(self):
        return [self.VAB, self.VBC, self.VCA]
    
    def rect(self):
        vab = cm.rect(self.VAB[0], np.radians(self.VAB[1]))
        vbc = cm.rect(self.VBC[0], np.radians(self.VBC[1]))
        vca = cm.rect(self.VCA[0], np.radians(self.VCA[1]))
        return [vab, vbc, vca]
    
    def toY(self):
        self.VAN = [self.VAB[0]/np.sqrt(3), self.VAB[1]-30]
        self.VBN = [self.VBC[0]/np.sqrt(3), self.VBC[1]-30]
        self.VCN = [self.VCA[0]/np.sqrt(3), self.VCA[1]-30]

####################################################
### Archivo Circuitos.py ###
# import cmath as cm
# import numpy as np
# from Fuente import FuentesY, FuentesD
# from imps import Impedancia

def rect_to_polar(fasores):
    fasores_en_polar = []
    for fasor in fasores:
        fasores_en_polar.append((cm.polar(fasor)[0], np.degrees(cm.polar(fasor)[1])))
    return fasores_en_polar
    

class DeltaDelta:
    def __init__(self, F, Z):
        self.fuentes = F
        self.impedancias = Z
        VAB, VBC, VCA = F.rect()
        t_linea = F.polar()
        t_fase = t_linea
        i_fase = [VAB/Z[0], # Iab
                  VBC/Z[1], # Ibc
                  VCA/Z[2]] # Ica
        i_f_ab, i_f_bc, i_f_ca = i_fase
        self.i_linea_aux = [i_f_ab-i_f_ca,
                    i_f_bc-i_f_ab,
                    i_f_ca-i_f_bc]
        # Corriente de linea:
        i_linea = rect_to_polar(self.i_linea_aux)
        # Corriente de fase:
        i_fase = rect_to_polar(i_fase)
        
        # Potencia compleja
        S = [VAB*np.conjugate(i_f_ab)+
             VBC*np.conjugate(i_f_bc)+
             VCA*np.conjugate(i_f_ca)]
        S_fases = [VAB*np.conjugate(i_f_ab),
                   VBC*np.conjugate(i_f_bc),
                   VCA*np.conjugate(i_f_ca)]
        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
        self.potencia = S
        self.potencia_fases = S_fases
    
    def t_fase(self):
        return self.tensiones_de_fase
    
    def t_linea(self):
        return self.tensiones_de_linea
    
    def i_fase(self):
        return self.corrientes_de_fase
    
    def i_linea(self):
        return self.corrientes_de_linea
    
    def potencia(self):
        return self.potencia
    
    
    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}
Potencia:\n{self.potencia}
Potencia por fases:\n{self.potencia_fases}"""
    
    
class EstrellaEstrella:
    def __init__(self, F:FuentesY, Z):
        self.fuentes = F
        self.impedancias = Z
        VAN, VBN, VCN = F.rect()

        t_fase = F.polar()
        t_linea = [VAN-VBN, VBN-VCN, VCN-VAN]
        t_linea_aux = t_linea
        t_linea = rect_to_polar(t_linea)


        i_fase = [VAN/Z[0], # Ian
                  VBN/Z[1], # Ibn
                  VCN/Z[2]] # Icn 
        i_fase_aux = i_fase    

        i_fase = rect_to_polar(i_fase)
        
        i_linea = i_fase

        # Corriente de neutro:
        i_neutro = cm.polar(i_fase_aux[0]+i_fase_aux[1]+i_fase_aux[2])
        i_neutro = (i_neutro[0], np.degrees(i_neutro[1])+180)

        # Potencia compleja
        S = [(VAN*np.conjugate(i_fase_aux[0]))+
             (VBN*np.conjugate(i_fase_aux[1]))+
             (VCN*np.conjugate(i_fase_aux[2]))]
        S_fases = [(VAN*np.conjugate(i_fase_aux[0])),
                   (VBN*np.conjugate(i_fase_aux[1])),
                   (VCN*np.conjugate(i_fase_aux[2]))]


        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
        self.corriente_neutro = i_neutro
        self.potencia = S
        self.potencia_fases = S_fases
    
    def t_fase(self):
        return self.tensiones_de_fase
    
    def t_linea(self):
        return self.tensiones_de_linea
    
    def i_fase(self):
        return self.corrientes_de_fase
    
    def i_linea(self):
        return self.corrientes_de_linea
    
    def potencia(self):
        return self.potencia

    
    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}
Corriente de neutro:\n{self.corriente_neutro}
Potencia:\n{self.potencia}
Potencia por fases:\n{self.potencia_fases}"""
    

class DeltaEstrella:
    def __init__(self, F:FuentesD, Z):
        self. fuentes = F
        self.impedancias = Z
        self.impedanciasD = Impedancia.imp_YtoD(Z)
        self.delta_delta = DeltaDelta(F, self.impedanciasD)

        # Corriente de linea:
        i_linea = self.delta_delta.i_linea_aux
        # Corriente de fase:
        i_fase = i_linea
        i_fase_aux = i_fase

        # Tension de fase:
        t_fase = [i_fase[0]*Z[0], i_fase[1]*Z[1], i_fase[2]*Z[2]]
        t_fase_aux = t_fase
        t_fase = rect_to_polar(t_fase)

        # Tension de linea:
        t_linea = F.polar()
        # Corriente de linea:
        i_linea = rect_to_polar(i_linea)
        # Corriente de fase:
        i_fase = i_linea           

        # Potencia compleja
        S = [t_fase_aux[0]*np.conjugate(i_fase_aux[0])+
             t_fase_aux[1]*np.conjugate(i_fase_aux[1])+
             t_fase_aux[2]*np.conjugate(i_fase_aux[2])]
        S_fases = [t_fase_aux[0]*np.conjugate(i_fase_aux[0]),
                   t_fase_aux[1]*np.conjugate(i_fase_aux[1]),
                   t_fase_aux[2]*np.conjugate(i_fase_aux[2])]

        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
        self.potencia = S
        self.potencia_fases = S_fases

        # Corrimiento del neutro:
        F.toY()
        fuentesY= FuentesY(F.VAN[0], F.VAN[1])
        self.estrella_estrella = EstrellaEstrella3Hilos(fuentesY, Z)
        self.corrimiento_neutro = self.estrella_estrella.corrimiento_neutro
        # Construir el circuito en Y-Y y calcular el corrimiento del neutro en Y-Y

    def t_fase(self):
        return self.tensiones_de_fase
    
    def t_linea(self):
        return self.tensiones_de_linea
    
    def i_fase(self):
        return self.corrientes_de_fase
    
    def i_linea(self):
        return self.corrientes_de_linea
    
    def potencia(self):
        return self.potencia

    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}
Corrimiento de neutro:\n{self.corrimiento_neutro}
Potencia:\n{self.potencia}
Potencia por fases:\n{self.potencia_fases}"""
    

class EstrellaDelta:
    def __init__(self, F:FuentesY, Z):
        self.fuentes = F
        self.impedancias = Z

        F.toD()
        fuentesD = FuentesD(F.VAB[0], F.VAB[1])
        self.delta_delta = DeltaDelta(fuentesD, Z)

        # Corriente de linea:
        i_linea = self.delta_delta.i_linea_aux
        i_linea = rect_to_polar(i_linea)
        

        # Corriente de fase:
        i_fase = self.delta_delta.i_fase()
        i_fase_aux = i_fase
        i_fase_aux = [cm.rect(i_fase_aux[0][0], np.radians(i_fase_aux[0][1])),
                      cm.rect(i_fase_aux[1][0], np.radians(i_fase_aux[1][1])),
                      cm.rect(i_fase_aux[2][0], np.radians(i_fase_aux[2][1]))]
        i_fase = [(round(i_fase[0][0],6), round(i_fase[0][1],6)),
                  (round(i_fase[1][0],6), round(i_fase[1][1],6)),
                  (round(i_fase[2][0],6), round(i_fase[2][1],6))]

        # Tension de fase:
        t_fase = F.polar()
        # Tension de linea:
        t_linea = [(round(F.VAB[0],6), round(F.VAB[1],6)),
                   (round(F.VBC[0],6), round(F.VBC[1]),6),
                   (round(F.VCA[0],6), round(F.VCA[1]),6)]
        t_linea_aux = t_linea
        t_linea_aux = [cm.rect(t_linea_aux[0][0], np.radians(t_linea_aux[0][1])),
                       cm.rect(t_linea_aux[1][0], np.radians(t_linea_aux[1][1])),
                       cm.rect(t_linea_aux[2][0], np.radians(t_linea_aux[2][1]))]
        # Potencia compleja
        t_fase = t_linea
        S = [t_linea_aux[0]*np.conjugate(i_fase_aux[0])+
             t_linea_aux[1]*np.conjugate(i_fase_aux[1])+
             t_linea_aux[2]*np.conjugate(i_fase_aux[2])]
        S_fases = [t_linea_aux[0]*np.conjugate(i_fase_aux[0]),
                   t_linea_aux[1]*np.conjugate(i_fase_aux[1]),
                   t_linea_aux[2]*np.conjugate(i_fase_aux[2])]        
        # S = ((cm.rect(207.85, np.radians(30)))*np.conjugate(cm.rect(1.386, np.radians(-23.13))))
        
        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
        self.potencia = S
        self.potencia_fases = S_fases

        # Corrimiento del neutro:
        fuentesY= FuentesY(F.VAN[0], F.VAN[1])
        self.estrella_estrella = EstrellaEstrella3Hilos(fuentesY, Z)
        self.corrimiento_neutro = self.estrella_estrella.corrimiento_neutro

    def t_fase(self):
        return self.tensiones_de_fase
    
    def t_linea(self):
        return self.tensiones_de_linea
    
    def i_fase(self):
        return self.corrientes_de_fase
    
    def i_linea(self):
        return self.corrientes_de_linea
    
    def potencia(self):
        return self.potencia

    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}
Corrimiento de neutro:\n{self.corrimiento_neutro}
Potencia:\n{self.potencia}
Potencia por fases:\n{self.potencia_fases}"""
    

class EstrellaEstrella3Hilos:
    def __init__(self, F, Z):
        self.fuentes = F
        self.impedancias = Z

        VAN, VBN, VCN = F.rect()
        # Matriz de impedancias
        Z_matrix = np.array([[Z[0]+Z[1], -Z[1]],
                             [-Z[1], Z[1]+Z[2]]])
        # Matriz de tensiones
        V_matrix = np.array([VAN-VBN, VBN-VCN])
        # Matriz de corrientes
        I_matrix = np.linalg.solve(Z_matrix, V_matrix) # [I1, I2]

        IAa = I_matrix[0] 
        IBb = I_matrix[1]-I_matrix[0]
        ICc = -I_matrix[1]
        i_fase = [IAa, IBb, ICc]

        Ian = IAa
        Ibn = IBb
        Icn = ICc
        i_linea = [Ian, Ibn, Icn]

        # Tensiones de fase
        Van = Ian*Z[0]
        Vbn = Ibn*Z[1]
        Vcn = Icn*Z[2]
        t_fase = [Van, Vbn, Vcn]
        t_fase = rect_to_polar(t_fase)

        # Tensiones de linea
        t_linea = [Van-Vbn, Vbn-Vcn, Vcn-Van]
        t_linea = rect_to_polar(t_linea)
        
        # Corrimientos de neutro
        VNn1 = -VAN + Van 
        VNn1 = cm.polar(VNn1)
        VNn1 = (round(VNn1[0], 6), round(np.degrees(VNn1[1]), 6))
        VNn2 = -VBN + Vbn
        VNn2 = cm.polar(VNn2)
        VNn2 = (round(VNn2[0], 6), round(np.degrees(VNn2[1]), 6))
        VNn3 = -VCN + Vcn
        VNn3 = cm.polar(VNn3)
        VNn3 = (round(VNn3[0], 6), round(np.degrees(VNn3[1]), 6))
        
        # Corrientes de fase
        i_fase = rect_to_polar(i_fase)
        # Corrientes de linea
        i_linea = i_fase

        # Potencia compleja
        S = [Van*np.conjugate(IAa)+
             Vbn*np.conjugate(IBb)+
             Vcn*np.conjugate(ICc)]
        S_fase = [Van*np.conjugate(IAa),
                  Vbn*np.conjugate(IBb),
                  Vcn*np.conjugate(ICc)]
        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
        self.corrimiento_neutro = [VNn1, VNn2, VNn3]
        self.potencia = S
        self.potencia_fases = S_fase

    def t_fase(self):
        return self.tensiones_de_fase
    
    def t_linea(self):
        return self.tensiones_de_linea
    
    def i_fase(self):
        return self.corrientes_de_fase
    
    def i_linea(self):
        return self.corrientes_de_linea
    
    def potencia(self):
        return self.potencia
    
    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}
Corrimiento de neutro:\n{self.corrimiento_neutro}
Potencia:\n{self.potencia}
Potencia por fases:\n{self.potencia_fases}""" 
####################################################
### Archivo tests.py ###
# import cmath as cm
# import numpy as np
# from equivalencias import *
# from Fuente import *

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

### Archivo main.py ###
# from imps import Impedancia
# from Fuente import FuentesY, FuentesD
# from Circuitos import DeltaDelta, EstrellaEstrella, DeltaEstrella, EstrellaDelta, EstrellaEstrella3Hilos


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
