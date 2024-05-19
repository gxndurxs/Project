import pygame
import random
from pygame.sprite import Group

def events(screen, player, bullets, comets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.mtop = True
            if event.key == pygame.K_s:
                player.mbottom = True
            if event.key == pygame.K_a:
                player.mleft = True
            if event.key == pygame.K_d:
                player.mright = True
            if event.key == pygame.K_SPACE:
                bullets_movement(screen, player, bullets)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.mtop = False
            if event.key == pygame.K_s:
                player.mbottom = False
            if event.key == pygame.K_a:
                player.mleft = False
            if event.key == pygame.K_d:
                player.mright = False
        elif event.type == pygame.USEREVENT:
            for _ in range(2):
                create_comet(screen, comets)

class Comet(pygame.sprite.Sprite):
    """Создание препятствий для игрока - Кометы"""

    def __init__(self, y, screen, group):
        """Инициализация данных"""
        super(Comet, self).__init__()

        self.screen = screen
        self.size = random.randint(30, 100)
        self.image = pygame.transform.scale(pygame.image.load("Images/comet.png"), (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(random.randint(0, screen.get_width()), -50))
        self.speedy = random.uniform(1, 3)
        self.speedx = self.speedy * random.uniform(-0.5, 0.5)
        self.add(group)

    def update(self):
        """Движение комет"""
        self.rect.y += self.speedy
        self.rect.x += self.speedx

    def draw(self):
        """Отображение комет на экране"""
        self.screen.blit(self.image, self.rect)

class Bullet(pygame.sprite.Sprite):
    """Создание пуль персонажа"""

    def __init__(self, screen, player):
        """Инициализация данных"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.image = pygame.image.load("Images/bullets1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.top = player.rect.top
        self.speed = 2

    def update(self):
        self.rect.y -= self.speed

    def draw(self):
        self.screen.blit(self.image, self.rect)

def update(screen, player, bullets, comets, score):
    """Отображение и обновление движения объектов на экране"""
    screen.fill((0, 0, 0))
    for bullet in bullets.sprites():
        bullet.update()
        bullet.draw()
    player.update()
    player.draw()
    for comet in comets.sprites():
        comet.update()
        comet.draw()
    score.draw()
    player.draw_health_bar()
    pygame.display.flip()

def update_bullets(bullets, comets, score):
    """Обновление движения пуль и проверка на столкновения"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    collisions = pygame.sprite.groupcollide(bullets, comets, True, True)
    if collisions:
        score.add_score(10)

def bullets_movement(screen, player, bullets):
    """Отслеживание полета пуль"""
    new_bullet = Bullet(screen, player)
    bullets.add(new_bullet)

def update_comets(comets, player):
    """Обновление движения комет"""
    comets.update()
    for comet in comets.copy():
        if comet.rect.top >= player.screen.get_height() or comet.rect.left >= player.screen.get_width() or comet.rect.right <= 0:
            comets.remove(comet)
        offset = (comet.rect.x - player.rect.x, comet.rect.y - player.rect.y)
        if player.mask.overlap(comet.mask, offset):
            player.health -= 2
            comets.remove(comet)
            if player.health <= 0:
                pygame.quit()
                exit()

def create_comet(screen, group):
    """Создание кометы"""
    y = random.randint(-50, -10)
    comet = Comet(y, screen, group)
    while pygame.sprite.spritecollideany(comet, group):
        comet.rect.y -= 10
        comet.rect.x = random.randint(0, screen.get_width())

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Player, self).__init__()
        self.screen = screen
        self.image = pygame.image.load("Images/kor.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.mask = pygame.mask.from_surface(self.image)

        self.mtop = False
        self.mbottom = False
        self.mleft = False
        self.mright = False
        self.health = 10

    def update(self):
        if self.mtop and self.rect.top > 0:
            self.rect.centery -= 2
        if self.mbottom and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery += 2
        if self.mleft and self.rect.left > 0:
            self.rect.centerx -= 2
        if self.mright and self.rect.right < self.screen_rect.right:
            self.rect.centerx += 2

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def draw_health_bar(self):
        """Отображение полоски здоровья"""
        health_bar_width = 200
        health_bar_height = 20
        health_percentage = self.health / 10
        current_health_width = health_bar_width * health_percentage

        pygame.draw.rect(self.screen, (255, 0, 0), (10, 10, health_bar_width, health_bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, current_health_width, health_bar_height))

class Score:
    """Класс для подсчета и отображения очков"""
    
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)
        self.color = (255, 255, 255)
        self.prep_score()

    def add_score(self, points):
        self.score += points
        self.prep_score()

    def prep_score(self):
        self.score_image = self.font.render(str(self.score), True, self.color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen.get_rect().right - 20
        self.score_rect.top = 20

    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1620, 900))
    pygame.display.set_caption("My Game")

    player = Player(screen)
    bullets = pygame.sprite.Group()
    comets = Group()
    score = Score(screen)

    time = random.randint(300, 600)
    pygame.time.set_timer(pygame.USEREVENT, time)

    while True:
        events(screen, player, bullets, comets)
        update(screen, player, bullets, comets, score)
        update_bullets(bullets, comets, score)
        update_comets(comets, player)

if __name__ == '__main__':
    run_game()
