import pygame

class Bullets(pygame.sprite.Sprite):
    """Создание пуль персонажа"""

    def __init__(self, screen, player):
        """Инициализация данных"""
        super(Bullet, self).__init__()

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load("Images/player.png")