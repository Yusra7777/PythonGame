import os

import pygame


class BasisObjekt:
    def __init__(self, x, y, bild):
        self.x = x
        self.y = y
        self.bild = bild
        self.mask = pygame.mask.from_surface(bild)
        self.rect = self.bild.get_rect(topleft=(self.x, self.y))
        self.schrift = pygame.font.SysFont(None, 24)

    def zeichnen(self, bildschirm):
        bildschirm.blit(self.bild, (self.x, self.y))

    def kollision(self, *andere):
        for objekt in andere:
            if self.rect.colliderect(objekt.rect):
                objekt.kollision(self)
                return True
        return False

    def set_ui_info(self):
        return []


def bild_laden(name):
    basispfad = os.path.dirname(os.path.abspath(__file__))
    bildpfad = os.path.join(basispfad, "../../bilder", f"{name}.png")

    if not os.path.exists(bildpfad):
        raise FileNotFoundError(f"Das Bild {bildpfad} konnte nicht gefunden werden.")

    try:
        bild = pygame.image.load(bildpfad).convert_alpha()
        return bild
    except pygame.error as e:
        raise IOError(f"Fehler beim Laden des Bildes {name}.png: {e}")

