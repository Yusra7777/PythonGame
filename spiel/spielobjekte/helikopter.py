from spiel.spielobjekte.basisobjekt import BasisObjekt


class Helikopter(BasisObjekt):
    def __init__(self, bild, x, y, lkw):
        super().__init__(x, y, bild)
        self.lkw = lkw
        self.geschwindigkeit = 2.5
        self.geladenes_erz = 0

    def kollision(self, objekt):
        if self.geladenes_erz < 50:
            self.geladenes_erz += 50
            objekt.kollision(self)

    def set_ui_info(self):
        return [
            f'Geladenes Erz (H): {self.geladenes_erz}'
        ]
