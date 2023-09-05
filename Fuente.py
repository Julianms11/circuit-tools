import numpy as np
import cmath as cm


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

    

