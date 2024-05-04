from spiel.spielobjekte.basisobjekt import BasisObjekt


class Landeplatz(BasisObjekt):
    def __init__(self, bild, x, y, gestohlenes_erz):
        super().__init__(x, y, bild)
        self.gestohlenes_erz = gestohlenes_erz

    def kollision(self, hubschrauber):
        self.erz_hinzufügen(hubschrauber.geladenes_erz)

    def position_abrufen(self):
        return self.x, self.y

    def erz_hinzufügen(self, erz):
        self.gestohlenes_erz += erz

    def set_ui_info(self):
        return [
            f'Gestohlenes Erz: {self.gestohlenes_erz}'
        ]
