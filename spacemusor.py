#доделать кнопку паузы, метеориты/враги, размер метеоритов


import pygame
import random


WIDTH = 800
HEIGHT = 640
FPS = 30

global enemy1_spawn_delay, SCORE
enemy1_spawn_delay = 300
SCORE = 0
PAUSE = 1
TIMER = 0

class hit_effect(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.id = 0
        self.image = red_sprites[self.id]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        if self.id != 4:
            self.id += 1
            self.image = red_sprites[self.id]
        else:
            self.kill()

class explosive(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.id = 0
        self.image = explosive_sprites[self.id]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        if self.id != 17:
            self.id += 1
            self.image = explosive_sprites[self.id]
        else:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_idle_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-40)
        self.speed = 15
        self.shoot_delay = 3
        self.shoot_position = True
        self.hp = 100

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
            shoot1_snd.play()
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
        self.hp = 2

    def update(self):
        global SCORE
        self.rect.y += self.speed
        if self.rect.y > HEIGHT-10:
            self.kill()
        if self.hp == 0:
            SCORE += 1
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

class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pause_btn
        self.rect = self.image.get_rect()
        self.rect.x = 670
        self.rect.y = 10

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.id = random.randint(0,9)
        self.image = meteors_sprite[self.id]
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = random.randint(50, 600)
        self.angle = 0
        self.speedx = random.randint(1, 10)
        self.speedy = random.randint(1, 5)

    def update(self):
        self.angle += self.speedx * PAUSE
        self.image = pygame.transform.rotozoom(meteors_sprite[self.id], self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.move_ip(self.speedx * PAUSE, self.speedy * PAUSE)
        if self.rect.left > WIDTH + 100:
            self.kill()
        if self.rect.top > HEIGHT + 100:
            self.kill()

def enemies_spawn():
    global enemy1_spawn_delay
    if enemy1_spawn_delay < 0:
        enemy = Enemy1()
        enemies.add(enemy)
        enemy1_spawn_delay = 300
    else:
        enemy1_spawn_delay -= random.randint(1,3)

def meteor_spawn():
    if random.randint(1,100) == 50:
        x = Meteor()
        meteors.add(x)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, '#FFF222')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

pygame.init()
pygame.mixer.init()

maintheme_snd = 'spacemusor/sounds/maintheme.mp3'
maintheme_snd = pygame.mixer.Sound(maintheme_snd)
hit_snd = 'spacemusor/sounds/hit.mp3'
hit_snd = pygame.mixer.Sound(hit_snd)
exp_snd = 'spacemusor/sounds/enemy_dead.mp3'
exp_snd = pygame.mixer.Sound(exp_snd)
shoot1_snd = 'spacemusor/sounds/shoot1.mp3'
shoot1_snd = pygame.mixer.Sound(shoot1_snd)

maintheme_snd.set_volume(0.01)
hit_snd.set_volume(0.1)
exp_snd.set_volume(0.1)
shoot1_snd.set_volume(0.07)
maintheme_snd.play()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

bg = 'spacemusor/sprites/bg.png'
bg = pygame.image.load(bg)

health_bar = 'spacemusor/sprites/ui/health.png'
health_bar = pygame.image.load(health_bar)

score_bar = 'spacemusor/sprites/ui/time.png'
score_bar = pygame.image.load(score_bar)

player_idle_img = 'spacemusor/sprites/player/player1.png'
player_idle_img = pygame.image.load(player_idle_img)
player_left_img = 'spacemusor/sprites/player/player_left.png'
player_left_img = pygame.image.load(player_left_img)
player_right_img = 'spacemusor/sprites/player/player_right.png'
player_right_img = pygame.image.load(player_right_img)

play_btn = 'spacemusor/sprites/ui/play.png'
play_btn = pygame.image.load(play_btn)
pause_btn = 'spacemusor/sprites/ui/pause.png'
pause_btn = pygame.image.load(pause_btn)

bullet_yellow = 'spacemusor/sprites/weapons/bullet_yellow.png'
bullet_yellow = pygame.image.load(bullet_yellow)

explosive_sprites = []
red_sprites = []
meteors_sprite = []
for i in range(1,19):
    x = 'spacemusor/sprites/explosive/'+str(i)+'.png'
    x = pygame.image.load(x)
    explosive_sprites.append(x)
for i in range(1, 6):
    x = 'spacemusor/sprites/red/red' + str(i) + '.png'
    x = pygame.image.load(x)
    red_sprites.append(x)
for i in range(1, 11):
    x = 'spacemusor/sprites/meteors/meteor' + str(i) + '.png'
    x = pygame.image.load(x)
    meteors_sprite.append(x)

enemy1_img = 'spacemusor/sprites/enemies/enemy1.png'
enemy1_img = pygame.image.load(enemy1_img)

enemies = pygame.sprite.Group()
sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
other = pygame.sprite.Group()
meteors = pygame.sprite.Group()
player = Player()
sprites.add(player)
button = Button()




running = True


while running:
    clock.tick(FPS)
    screen.blit(bg, (0, 0))
    screen.blit(health_bar, (650, 560))
    screen.blit(score_bar, (0, 0))


    draw_text(screen, str(SCORE), 26, 60, 54)
    draw_text(screen, str(TIMER), 26, 60, 8)

    if PAUSE == 1:
        enemies_spawn()
        meteor_spawn()

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        if i.type == pygame.MOUSEBUTTONDOWN:
            if button.rect.collidepoint(i.pos):
                if PAUSE == 1:
                    PAUSE = 0
                    button.image = play_btn
                else:
                    PAUSE = 1
                    button.image = pause_btn

    hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
    for i in hits:
        i.hp -= 1
        hit_snd.play()
        if i.hp == 0:
            x = explosive(i.rect.centerx, i.rect.centery)
            exp_snd.play()
            other.add(x)

    hit_player = pygame.sprite.spritecollide(player, enemies, True)
    if hit_player:
        player.hp -= 10
        x = explosive(player.rect.centerx, player.rect.y)
        exp_snd.play()
        other.add(x)
        x = hit_effect()
        other.add(x)

    pygame.draw.rect(screen, '#ff183b', (654, 571, player.hp, 15))
    screen.blit(button.image, button.rect)

    sprites.update()
    enemies.update()
    bullets.update()
    other.update()
    meteors.update()

    button.update()

    sprites.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)
    other.draw(screen)
    meteors.draw(screen)



    pygame.display.flip()

pygame.quit()
