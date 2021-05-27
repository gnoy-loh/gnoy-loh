#доделать кнопку паузы, метеориты/враги, размер метеоритов


import pygame
import random


WIDTH = 800
HEIGHT = 640
FPS = 30

global enemy1_spawn_delay, enemy2_spawn_delay, enemy3_spawn_delay, SCORE, WEAPON
global enemy1_delay, enemy2_delay, enemy3_delay
global delay_flag, pr_score

delay_flag = True
pr_score = 0

enemy1_delay = 300
enemy2_delay = 300
enemy3_delay = 300

enemy1_spawn_delay = 300
enemy2_spawn_delay = 300
enemy3_spawn_delay = 300

SCORE = 0
PAUSE = 1
TIMER = 0
WEAPON = 1

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
            self.id += 1 * PAUSE
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
            self.id += 1 * PAUSE
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
        global WEAPON
        if PAUSE == 1:
            keystate = pygame.key.get_pressed()
            self.image = player_idle_img

            if keystate[pygame.K_1]:
                WEAPON = 1
            if keystate[pygame.K_2]:
                WEAPON = 2

            if keystate[pygame.K_a] and self.rect.left > 10:
                self.rect.x -= self.speed
                self.image = player_left_img
            if keystate[pygame.K_d] and self.rect.right < WIDTH-10:
                self.rect.x += self.speed
                self.image = player_right_img
            if keystate[pygame.K_SPACE] and self.shoot_delay < 0:
                if WEAPON == 1:
                    if self.shoot_position == True:
                        bullet = Bullet_Yellow(self.rect.centerx-15, self.rect.y+30)
                        self.shoot_position = False
                    else:
                        bullet = Bullet_Yellow(self.rect.centerx+15, self.rect.y)
                        self.shoot_position = True
                    bullets.add(bullet)
                    self.shoot_delay = 3
                    shoot1_snd.play()
                if WEAPON == 2:
                    bullet = Bullet_Laser(self.rect.centerx, self.rect.top)
                    bullets.add(bullet)
                    self.shoot_delay = 6
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
        self.hp = 5

    def update(self):
        global SCORE
        self.rect.y += self.speed * PAUSE
        if self.rect.y > HEIGHT-10:
            self.kill()
        if self.hp == 0:
            SCORE += 1
            self.kill()

class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy2_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50,WIDTH-50)
        self.rect.bottom = 0
        self.speed = 8
        self.hp = 2

    def update(self):
        global SCORE
        self.rect.y += self.speed * PAUSE
        if self.rect.y > HEIGHT-10:
            self.kill()
        if self.hp == 0:
            SCORE += 2
            self.kill()

class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy3_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50,WIDTH-50)
        self.rect.bottom = 0
        self.speed = 1
        self.hp = 10

    def update(self):
        global SCORE
        if random.randint(1,50) == 5:
            x = Bullet_Enemy(self.rect.centerx, self.rect.bottom)
            bullets_enemy.add(x)
        self.rect.y += self.speed * PAUSE
        if self.rect.y > HEIGHT-10:
            self.kill()
        if self.hp == 0:
            SCORE += 5
            self.kill()

class Bullet_Yellow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_yellow
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 15
        self.hp = 1

    def update(self):
        self.rect.y -= self.speed * PAUSE
        if self.rect.y < 0 or self.hp < 0:
            self.kill()

class Bullet_Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_laser
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 20
        self.hp = 10

    def update(self):
        self.rect.y -= self.speed * PAUSE
        if self.rect.y < 0 or self.hp < 0:
            self.kill()

class Bullet_Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_enemy
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 12

    def update(self):
        self.rect.y += self.speed * PAUSE
        if self.rect.y > HEIGHT:
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
    global enemy1_spawn_delay, enemy1_delay, enemy2_spawn_delay, enemy2_delay, enemy3_spawn_delay, enemy3_delay
    if enemy1_spawn_delay < 0:
        enemy = Enemy1()
        enemies.add(enemy)
        enemy1_spawn_delay = enemy1_delay
    else:
        enemy1_spawn_delay -= random.randint(1,3)

    if enemy2_spawn_delay < 0 and enemy1_delay == 100:
        enemy = Enemy2()
        enemies.add(enemy)
        enemy2_spawn_delay = enemy2_delay
    else:
        enemy2_spawn_delay -= random.randint(1,3)

    if enemy3_spawn_delay < 0 and enemy2_delay == 100:
        enemy = Enemy3()
        enemies.add(enemy)
        enemy3_spawn_delay = enemy3_delay
    else:
        enemy3_spawn_delay -= random.randint(1,3)

def difficult():
    global enemy1_delay, pr_score, delay_flag, enemy2_delay, enemy3_delay
    print(enemy1_delay)
    if SCORE > pr_score:
        delay_flag = True

    if delay_flag == True:
        if SCORE % 2 == 0:
            if enemy1_delay > 100:
                enemy1_delay -= 20
            if enemy2_delay > 100 and enemy1_delay == 100:
                enemy2_delay -= 20
            if enemy3_delay > 100 and enemy2_delay == 100:
                enemy3_delay -= 20
            pr_score = SCORE
            delay_flag = False

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
hit_snd.set_volume(0.05)
exp_snd.set_volume(0.05)
shoot1_snd.set_volume(0.02)
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

bullet_laser = 'spacemusor/sprites/weapons/laser.png'
bullet_laser = pygame.image.load(bullet_laser)

bullet_enemy = 'spacemusor/sprites/weapons/bullet_enemy.png'
bullet_enemy = pygame.image.load(bullet_enemy)

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

enemy2_img = 'spacemusor/sprites/enemies/enemy2.png'
enemy2_img = pygame.image.load(enemy2_img)

enemy3_img = 'spacemusor/sprites/enemies/enemy3.png'
enemy3_img = pygame.image.load(enemy3_img)

enemies = pygame.sprite.Group()
sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets_enemy = pygame.sprite.Group()
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
        difficult()

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

    hits = pygame.sprite.groupcollide(enemies, bullets, False, False)
    for i in hits:
        i.hp -= 1
        hit_snd.play()
        if i.hp == 0:
            x = explosive(i.rect.centerx, i.rect.centery)
            exp_snd.play()
            other.add(x)

    hits = pygame.sprite.groupcollide(bullets, enemies, False, False)
    for i in hits:
        i.hp -= 1

    hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
    hits = pygame.sprite.groupcollide(enemies, meteors, True, True)
    for i in hits:
        x = explosive(i.rect.centerx, i.rect.centery)

    hit_player = pygame.sprite.spritecollide(player, enemies, True)
    if hit_player:
        player.hp -= 10
        x = explosive(player.rect.centerx, player.rect.y)
        exp_snd.play()
        other.add(x)
        x = hit_effect()
        other.add(x)

    hit_player = pygame.sprite.spritecollide(player, bullets_enemy, True)
    if hit_player:
        player.hp -= 5

    pygame.draw.rect(screen, '#ff183b', (654, 571, player.hp, 15))
    screen.blit(button.image, button.rect)

    sprites.update()
    enemies.update()
    bullets.update()
    other.update()
    meteors.update()
    bullets_enemy.update()

    button.update()

    sprites.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)
    other.draw(screen)
    meteors.draw(screen)
    bullets_enemy.draw(screen)



    pygame.display.flip()

pygame.quit()
