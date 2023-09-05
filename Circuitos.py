import cmath as cm
import numpy as np
from Fuente import FuentesY, FuentesD
from imps import Impedancia

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
