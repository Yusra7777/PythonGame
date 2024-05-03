from spiel.spielobjekte.basisobjekt import BasisObjekt


class Tankstelle(BasisObjekt):
    def __init__(self, bild, x, y):
        super().__init__(x, y, bild)
