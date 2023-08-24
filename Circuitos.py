import cmath as cm
import numpy as np
from Fuente import FuentesY, FuentesD
from imps import Impedancia

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
        
        i_linea = [cm.polar(i_f_ab-i_f_ca),
                    cm.polar(i_f_bc-i_f_ab),
                    cm.polar(i_f_ca-i_f_bc)]
        i_linea = [(i_linea[0][0], np.degrees(i_linea[0][1])), # Iab
                   (i_linea[1][0], np.degrees(i_linea[1][1])), # Ibc
                   (i_linea[2][0], np.degrees(i_linea[2][1]))] # Ica
        i_fase = [cm.polar(i_fase[0]), 
                  cm.polar(i_fase[1]),
                  cm.polar(i_fase[2])]
        i_fase = [(i_fase[0][0], np.degrees(i_fase[0][1])), # Iab
                  (i_fase[1][0], np.degrees(i_fase[1][1])), # Ibc
                  (i_fase[2][0], np.degrees(i_fase[2][1]))] # Ica
        
        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
    
    def t_fase(self):
        return self.tensiones_de_fase
    
    def t_linea(self):
        return self.tensiones_de_linea
    
    def i_fase(self):
        return self.corrientes_de_fase
    
    def i_linea(self):
        return self.corrientes_de_linea
    
    
    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}"""
    
    
class EstrellaEstrella:
    def __init__(self, F:FuentesY, Z):
        self.fuentes = F
        self.impedancias = Z
        VAN, VBN, VCN = F.rect()

        t_fase = F.polar()
        t_linea = [VAN-VBN, VBN-VCN, VCN-VAN]
        t_linea = [cm.polar(t_linea[0]),
                   cm.polar(t_linea[1]),
                   cm.polar(t_linea[2])]
        t_linea = [(t_linea[0][0], np.degrees(t_linea[0][1])), # Vab
                   (t_linea[1][0], np.degrees(t_linea[1][1])), # Vbc
                   (t_linea[2][0], np.degrees(t_linea[2][1]))] # Vca

        i_fase = [VAN/Z[0], # Ian
                  VBN/Z[1], # Ibn
                  VCN/Z[2]] # Icn     
        i_fase = [cm.polar(i_fase[0]), 
                  cm.polar(i_fase[1]),
                  cm.polar(i_fase[2])] 
        i_fase = [(i_fase[0][0], np.degrees(i_fase[0][1])), # Ian
                  (i_fase[1][0], np.degrees(i_fase[1][1])), # Ibn
                  (i_fase[2][0], np.degrees(i_fase[2][1]))] # Icn
        
        i_linea = i_fase

        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
    
    def t_fase(self):
        return self.tensiones_de_fase
    
    def t_linea(self):
        return self.tensiones_de_linea
    
    def i_fase(self):
        return self.corrientes_de_fase
    
    def i_linea(self):
        return self.corrientes_de_linea
    
    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}"""
    

class EstrellaEstrella3Hilos:
    def __init__(self, F, Z):
        self.fuentes = F
        self.impedancias = Z
        VAN, VBN, VCN = F.rect()
        Z_matrix = np.array([[Z[0]+Z[1], -Z[1]],
                             [-Z[1], Z[1]+Z[2]]])
        
        V_matrix = np.array([VAN-VBN, VBN-VCN])
        I_matrix = np.linalg.solve(Z_matrix, V_matrix) # [I1, I2]

        

        IAa = I_matrix[0] 
        IBb = I_matrix[1]-I_matrix[0]
        ICc = -I_matrix[1]
        i_fase = [IAa, IBb, ICc]

        Ian = IAa
        Ibn = IBb
        Icn = ICc
        i_linea = [Ian, Ibn, Icn]

        Van = Ian*Z[0]
        Vbn = Ibn*Z[1]
        Vcn = Icn*Z[2]
        t_fase = [Van, Vbn, Vcn]
        t_fase = [cm.polar(t_fase[0]),
                    cm.polar(t_fase[1]),
                    cm.polar(t_fase[2])]
        t_fase = [(round(t_fase[0][0],6), round(np.degrees(t_fase[0][1]),6)), # Van
                    (round(t_fase[1][0],6), round(np.degrees(t_fase[1][1]),6)), # Vbn
                    (round(t_fase[2][0],6), round(np.degrees(t_fase[2][1]),6))]
        

        t_linea = [Van-Vbn, Vbn-Vcn, Vcn-Van]
        t_linea = [cm.polar(t_linea[0]),
                   cm.polar(t_linea[1]),
                   cm.polar(t_linea[2])]
        t_linea = [(round(t_linea[0][0],6), round(np.degrees(t_linea[0][1]),6)), # Vab
                     (round(t_linea[1][0],6), round(np.degrees(t_linea[1][1]),6)), # Vbc
                     (round(t_linea[2][0],6), round(np.degrees(t_linea[2][1]),6))]
        
        # Corrimiento de neutro
        VNn1 = -VAN + Van 
        VNn1 = cm.polar(VNn1)
        VNn1 = (round(VNn1[0], 6), round(np.degrees(VNn1[1]), 6))
        VNn2 = -VBN + Vbn
        VNn2 = cm.polar(VNn2)
        VNn2 = (round(VNn2[0], 6), round(np.degrees(VNn2[1]), 6))
        VNn3 = -VCN + Vcn
        VNn3 = cm.polar(VNn3)
        VNn3 = (round(VNn3[0], 6), round(np.degrees(VNn3[1]), 6))
        

        i_fase = [cm.polar(i_fase[0]),
                    cm.polar(i_fase[1]),
                    cm.polar(i_fase[2])]
        i_fase = [(round(i_fase[0][0],6), round(np.degrees(i_fase[0][1]),6)), # Ian
                    (round(i_fase[1][0],6), round(np.degrees(i_fase[1][1]),6)), # Ibn
                    (round(i_fase[2][0],6), round(np.degrees(i_fase[2][1]),6))]
        i_linea = i_fase


        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
        self.corrimiento_neutro = [VNn1, VNn2, VNn3]

    def t_fase(self):
        return self.tensiones_de_fase
    
    def t_linea(self):
        return self.tensiones_de_linea
    
    def i_fase(self):
        return self.corrientes_de_fase
    
    def i_linea(self):
        return self.corrientes_de_linea
    
    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}
Corrimiento de neutro:\n{self.corrimiento_neutro}"""


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

        # Tension de fase:
        t_fase = [i_fase[0]*Z[0], i_fase[1]*Z[1], i_fase[2]*Z[2]]
        t_fase = [cm.polar(t_fase[0]),
                    cm.polar(t_fase[1]),
                    cm.polar(t_fase[2])]
        t_fase = [(round(t_fase[0][0],6), round(np.degrees(t_fase[0][1]),6)), # Vab
                    (round(t_fase[1][0],6), round(np.degrees(t_fase[1][1]),6)), # Vbc
                    (round(t_fase[2][0],6), round(np.degrees(t_fase[2][1]),6))]

        # Tension de linea:
        t_linea = F.polar()

        i_linea = [cm.polar(i_linea[0]),
                    cm.polar(i_linea[1]),
                    cm.polar(i_linea[2])]
        i_linea = [(round(i_linea[0][0],6), round(np.degrees(i_linea[0][1]),6)), # Iab
                   (round(i_linea[1][0],6), round(np.degrees(i_linea[1][1]),6)), # Ibc
                    (round(i_linea[2][0],6), round(np.degrees(i_linea[2][1]),6))] # Ica 
        i_fase = i_linea           

        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
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
    
    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}
Corrimiento de neutro:\n{self.corrimiento_neutro}"""
    

class EstrellaDelta:
    def __init__(self, F:FuentesY, Z):
        self.fuentes = F
        self.impedancias = Z

        F.toD()
        fuentesD = FuentesD(F.VAB[0], F.VAB[1])
        self.delta_delta = DeltaDelta(fuentesD, Z)

        # Corriente de linea:
        i_linea = self.delta_delta.i_linea_aux
        i_linea = [cm.polar(i_linea[0]),
                    cm.polar(i_linea[1]),
                    cm.polar(i_linea[2])]
        i_linea = [(round(i_linea[0][0],6), round(np.degrees(i_linea[0][1]),6)), # Iab
                     (round(i_linea[1][0],6), round(np.degrees(i_linea[1][1]),6)), # Ibc
                      (round(i_linea[2][0],6), round(np.degrees(i_linea[2][1]),6))]
        

        # Corriente de fase:
        i_fase = self.delta_delta.i_fase()
        i_fase = [(round(i_fase[0][0],6), round(i_fase[0][1],6)),
                  (round(i_fase[1][0],6), round(i_fase[1][1],6)),
                  (round(i_fase[2][0],6), round(i_fase[2][1],6))]

        # Tension de fase:
        t_fase = F.polar()

        # Tension de linea:
        t_linea = [(round(F.VAB[0],6), round(F.VAB[1],6)),
                   (round(F.VBC[0],6), round(F.VBC[1]),6),
                   (round(F.VCA[0],6), round(F.VCA[1]),6)]

        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
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
    
    def __str__(self):
        return f"""Tensiones de fase:\n{self.tensiones_de_fase}
Tensiones de linea:\n{self.tensiones_de_linea}
Corrientes de fase:\n{self.corrientes_de_fase}
Corrientes de linea:\n{self.corrientes_de_linea}
Corrimiento de neutro:\n{self.corrimiento_neutro}"""
    



  
        

        



        
        
