import pygame
import random
from pygame.sprite import Group

# Определение состояний игры
RUNNING, PAUSED, GAME_OVER = 0, 1, 2


def events(screen, player, bullets, comets, bullet_sound, game_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == RUNNING:
                    return PAUSED
                else:
                    return RUNNING
            if game_state == RUNNING and player.alive:
                if event.key == pygame.K_w:
                    player.mtop = True
                if event.key == pygame.K_s:
                    player.mbottom = True
                if event.key == pygame.K_a:
                    player.mleft = True
                if event.key == pygame.K_d:
                    player.mright = True
                if event.key == pygame.K_SPACE:
                    bullet_sound.play()
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
    return game_state


def pause_events(resume_button, quit_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return RUNNING
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if resume_button.collidepoint(event.pos):
                return RUNNING
            elif quit_button.collidepoint(event.pos):
                pygame.quit()
                exit()
    return PAUSED


def draw_pause_screen(screen):
    font = pygame.font.SysFont(None, 100)
    text = font.render("Paused", True, (255, 255, 255))
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    screen.blit(text, rect)

    font = pygame.font.SysFont(None, 75)
    resume_text = font.render("Resume", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))

    resume_button = resume_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    quit_button = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    screen.blit(resume_text, resume_button)
    screen.blit(quit_text, quit_button)

    pygame.display.flip()
    return resume_button, quit_button


def game_over_events(retry_button, quit_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if retry_button.collidepoint(event.pos):
                return RUNNING
            elif quit_button.collidepoint(event.pos):
                pygame.quit()
                exit()
    return GAME_OVER


def draw_game_over_screen(screen):
    font = pygame.font.SysFont(None, 100)
    text = font.render("Вы проиграли", True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    screen.blit(text, rect)

    font = pygame.font.SysFont(None, 75)
    retry_text = font.render("Попробовать еще раз", True, (255, 255, 255))
    quit_text = font.render("Выйти из игры", True, (255, 255, 255))

    retry_button = retry_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    quit_button = quit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    screen.blit(retry_text, retry_button)
    screen.blit(quit_text, quit_button)

    pygame.display.flip()
    return retry_button, quit_button


class Comet(pygame.sprite.Sprite):
    """Создание препятствий для игрока - Кометы"""

    comet_images = [
        "Images/comet.png",
        "Images/comet2.png",
        "Images/comet3.png"
    ]

    def __init__(self, y, screen, group):
        """Инициализация данных"""
        super().__init__()
        self.screen = screen
        self.image_path = random.choice(self.comet_images)
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.size = random.randint(30, 100)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(center=(random.randint(0, screen.get_width()), y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speedy = random.uniform(1, 3)  # Скорость кометы по y
        self.angle = random.uniform(-60, 60)  # Угол движения кометы
        self.speedx = self.speedy * random.uniform(-0.5, 0.5)  # Скорость кометы по x
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
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Images/bullets1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.top = player.rect.top
        self.speed = 2

    def update(self):
        self.rect.y -= self.speed

    def draw(self):
        self.screen.blit(self.image, self.rect)


def update(screen, player, bullets, comets, score, background):
    """Отображение и обновление движения объектов на экране"""
    screen.blit(background, (0, 0))  # Обновление заднего фона
    for bullet in bullets.sprites():
        bullet.update()
        bullet.draw()
    if player.alive:
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
        if comet.rect.top >= player.screen.get_height() or comet.rect.left >= player.screen.get_width() or comet.rect.right <= 0 or comet.rect.bottom <= 0:
            comets.remove(comet)
        offset = (comet.rect.x - player.rect.x, comet.rect.y - player.rect.y)
        if player.mask.overlap(comet.mask, offset):
            player.health -= 2
            comets.remove(comet)
            if player.health <= 0:
                player.alive = False


def create_comet(screen, group):
    """Создание кометы"""
    y = random.randint(-50, -10)
    Comet(y, screen, group)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("Images/kor.png").convert_alpha()
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
        self.alive = True

    def update(self):
        if self.alive:
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
    screen = pygame.display.set_mode((1600, 880))
    pygame.display.set_caption("My Game")

    # Инициализация и загрузка фоновой музыки
    pygame.mixer.init()
    pygame.mixer.music.load("Sounds/run.mp3")
    pygame.mixer.music.set_volume(0.5)  # Установка громкости
    pygame.mixer.music.play(-1)  # Фоновая музыка играет бесконечно

    # Загрузка звука стрельбы
    bullet_sound = pygame.mixer.Sound("Sounds/bullet.mp3")
    bullet_sound.set_volume(0.5)  # Установка громкости

    # Создание игровых объектов
    player = Player(screen)
    bullets = pygame.sprite.Group()
    comets = Group()
    score = Score(screen)
    background = pygame.image.load("Images/fongame.png").convert()
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))  # Масштабирование фона

    time = random.randint(300, 600)  # Уменьшение интервала времени между событиями
    pygame.time.set_timer(pygame.USEREVENT, time)

    game_state = RUNNING

    while True:
        if game_state == RUNNING:
            game_state = events(screen, player, bullets, comets, bullet_sound, game_state)
            if player.alive:
                update(screen, player, bullets, comets, score, background)
                update_bullets(bullets, comets, score)
                update_comets(comets, player)
            else:
                game_state = GAME_OVER

        elif game_state == PAUSED:
            resume_button, quit_button = draw_pause_screen(screen)
            game_state = pause_events(resume_button, quit_button)

        elif game_state == GAME_OVER:
            retry_button, quit_button = draw_game_over_screen(screen)
            game_state = game_over_events(retry_button, quit_button)
            if game_state == RUNNING:
                player = Player(screen)
                bullets = pygame.sprite.Group()
                comets = Group()
                score = Score(screen)
                time = random.randint(300, 600)
                pygame.time.set_timer(pygame.USEREVENT, time)


if __name__ == "__main__":
    run_game()
