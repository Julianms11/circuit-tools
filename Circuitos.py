import cmath as cm
import numpy as np
from Fuente import FuentesY, FuentesD
from transformations import imp_DtoY, imp_YtoD

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

        t_fase = F.polar()

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
        t_linea = [Van, Vbn, Vcn]
        t_linea = [cm.polar(t_linea[0]),
                   cm.polar(t_linea[1]),
                   cm.polar(t_linea[2])]
        t_linea = [(t_linea[0][0], np.degrees(t_linea[0][1])), # Vab
                     (t_linea[1][0], np.degrees(t_linea[1][1])), # Vbc
                     (t_linea[2][0], np.degrees(t_linea[2][1]))]
        VNn = -VAN + Van # Corrimiento de neutro
        VNn = cm.polar(VNn)
        VNn = (VNn[0], np.degrees(VNn[1]))
        

        i_fase = [cm.polar(i_fase[0]),
                    cm.polar(i_fase[1]),
                    cm.polar(i_fase[2])]
        i_fase = [(i_fase[0][0], np.degrees(i_fase[0][1])), # Ian
                    (i_fase[1][0], np.degrees(i_fase[1][1])), # Ibn
                    (i_fase[2][0], np.degrees(i_fase[2][1]))]
        i_linea = i_fase


        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
        self.corrimiento_neutro = VNn

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
        self.impedanciasD = imp_YtoD(Z)
        VAB, VBC, VCA = F.rect()
        # Corriente de linea:
        aux_i_fase = [VAB/self.impedanciasD[0], # Iab
                        VBC/self.impedanciasD[1], # Ibc
                        VCA/self.impedanciasD[2]] # Ica
        aux_i_f_ab, aux_i_f_bc, aux_i_f_ca = aux_i_fase
        aux_i_linea = [aux_i_f_ab-aux_i_f_ca,
                    aux_i_f_bc-aux_i_f_ab,
                    aux_i_f_ca-aux_i_f_bc]
        i_linea = [cm.polar(aux_i_linea[0]),
                    cm.polar(aux_i_linea[1]),
                    cm.polar(aux_i_linea[2])]
        
        i_linea = [(i_linea[0][0], np.degrees(i_linea[0][1])), # Iab
                     (i_linea[1][0], np.degrees(i_linea[1][1])), # Ibc
                        (i_linea[2][0], np.degrees(i_linea[2][1]))]
        # Corriente de fase:
        i_fase = i_linea
        # Tension de linea:
        t_linea = [VAB, VBC, VCA]
        t_linea = F.polar()
        # Tension de fase:
        t_fase = [aux_i_linea[0]*Z[0], aux_i_linea[1]*Z[1], aux_i_linea[2]*Z[2]]
        t_fase = [cm.polar(t_fase[0]),
                    cm.polar(t_fase[1]),
                    cm.polar(t_fase[2])]
        t_fase = [(t_fase[0][0], np.degrees(t_fase[0][1])), # Vab
                        (t_fase[1][0], np.degrees(t_fase[1][1])), # Vbc
                        (t_fase[2][0], np.degrees(t_fase[2][1]))]
        
        self.tensiones_de_fase = t_fase
        self.tensiones_de_linea = t_linea
        self.corrientes_de_fase = i_fase
        self.corrientes_de_linea = i_linea
        # Corrimiento del neutro:


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
Corrientes de linea:\n{self.corrientes_de_linea}"""
    


class EstrellaDelta:
    def __init__(self, F:FuentesY, Z):
        self.fuentes = F
        self.fuentes.toD()
        self.impedancias = Z
        VAB = self.fuentes.VAB
        VBC = self.fuentes.VBC
        VCA = self.fuentes.VCA
        VAB = cm.rect(VAB[0], np.radians(VAB[1]))
        VBC = cm.rect(VBC[0], np.radians(VBC[1]))
        VCA = cm.rect(VCA[0], np.radians(VCA[1]))
  
        

        



        
        
