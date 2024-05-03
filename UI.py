import pygame


class UI:
    def __init__(self, spielobjekte):
        self.spielobjekte = spielobjekte
        self.font = pygame.font.SysFont(None, 24)

    def zeichnen(self, bildschirm):
        y_offset = 10
        for objekt in self.spielobjekte:
            objekt_info = objekt.set_ui_info()
            for info_text in objekt_info:
                text = self.font.render(info_text, True, (0, 0, 0))
                bildschirm.blit(text, (10, y_offset))
                y_offset += 30
