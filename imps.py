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

