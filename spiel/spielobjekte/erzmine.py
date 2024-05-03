from spiel.spielobjekte.basisobjekt import BasisObjekt


class Erzmine(BasisObjekt):
    def __init__(self, bild, x, y, vorkommen):
        super().__init__(x, y, bild)
        self.vorkommen = vorkommen

    def kollision(self, lkw):
        self.vorkommen -= 50

    def set_ui_info(self):
        return [
            f'Erz vorkommen: {self.vorkommen}'
        ]
