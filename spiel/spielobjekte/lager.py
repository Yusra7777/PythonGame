from spiel.spielobjekte.basisobjekt import BasisObjekt


class Lager(BasisObjekt):
    def __init__(self, bild, x, y, bestand):
        super().__init__(x, y, bild)
        self.bestand = bestand

    def kollision(self, lkw):
        self.bestand += 50

    def set_ui_info(self):
        return [
            f'Lagerbestand: {self.bestand}'
        ]
