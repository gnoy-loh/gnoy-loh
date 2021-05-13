import pygame
import random

WIDTH = 800
HEIGHT = 640
FPS = 30



global enemy1_spawn_delay
enemy1_spawn_delay = 300


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_idle_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-40)
        self.speed = 15
        self.shoot_delay = 3
        self.shoot_position = True

    def update(self):
        keystate = pygame.key.get_pressed()
        self.image = player_idle_img
        if keystate[pygame.K_a] and self.rect.left > 10:
            self.rect.x -= self.speed
            self.image = player_left_img
        if keystate[pygame.K_d] and self.rect.right < WIDTH-10:
            self.rect.x += self.speed
            self.image = player_right_img
        if keystate[pygame.K_SPACE] and self.shoot_delay < 0:
            if self.shoot_position == True:
                bullet = Bullet_Yellow(self.rect.centerx-15, self.rect.y+30)
                self.shoot_position = False
            else:
                bullet = Bullet_Yellow(self.rect.centerx+15, self.rect.y)
                self.shoot_position = True
            bullets.add(bullet)
            self.shoot_delay = 3
        else:
            self.shoot_delay -= 1


class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy1_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50,WIDTH-50)
        self.rect.bottom = 0
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT-10:
            self.kill()

class Bullet_Yellow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_yellow
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 15

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

def enemies_spawn():
    global enemy1_spawn_delay
    if enemy1_spawn_delay < 0:
        enemy = Enemy1()
        enemies.add(enemy)
        enemy1_spawn_delay = 300
    else:
        enemy1_spawn_delay -= random.randint(1,3)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

bg = 'spacemusor/sprites/bg.png'
bg = pygame.image.load(bg)

player_idle_img = 'spacemusor/sprites/player1.png'
player_idle_img = pygame.image.load(player_idle_img)
player_left_img = 'spacemusor/sprites/player_left.png'
player_left_img = pygame.image.load(player_left_img)
player_right_img = 'spacemusor/sprites/player_right.png'
player_right_img = pygame.image.load(player_right_img)

bullet_yellow = 'spacemusor/sprites/bullet_yellow.png'
bullet_yellow = pygame.image.load(bullet_yellow)

enemy1_img = 'spacemusor/sprites/enemy1.png'
enemy1_img = pygame.image.load(enemy1_img)

enemies = pygame.sprite.Group()
sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
sprites.add(player)



running = True

while running:
    clock.tick(FPS)
    screen.blit(bg, (0, 0))

    enemies_spawn()

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False

    sprites.update()
    enemies.update()
    bullets.update()

    sprites.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)

    pygame.display.flip()

pygame.quit()
