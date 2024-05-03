from spiel.spielobjekte.basisobjekt import BasisObjekt


class Landeplatz(BasisObjekt):
    def __init__(self, bild, x, y, gestohlenes_erz):
        super().__init__(x, y, bild)
        self.gestohlenes_erz = gestohlenes_erz

    def kollision(self, hubschrauber):
        self.gestohlenes_erz += 50

    def set_ui_info(self):
        return [
            f'Gestohlenes Erz: {self.gestohlenes_erz}'
        ]
