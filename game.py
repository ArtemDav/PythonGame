import pygame
import random
from os import path

###############################
#       DEFINE COLOR
red = pygame.Color("red")
black = pygame.Color("black")
white = pygame.Color("white")
slateblue = pygame.Color("#191970")
blue = pygame.Color("#1E90FF")
#       CONST
FPS = 60
#       IMAGE
image_folder = path.join(path.dirname(__file__), 'assets\\Image')
sound_folder = path.join(path.dirname(__file__), 'assets\\Sounds')
print(sound_folder)
player_sprite = pygame.image.load(image_folder + "\\player.png")
enemy_sprite = pygame.image.load(image_folder + "\\enemy.png")
bullet_sprite = pygame.image.load(image_folder + "\\bullet.png")
#       Initialization
pygame.init()
shoot_sound = pygame.mixer.Sound(sound_folder + "\\shot.wav")
background_image = pygame.image.load(image_folder + "\\background_game.png")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
background_image = pygame.transform.scale(background_image, (width, height))
pygame.display.set_caption("Yandex Lyceum Project by Artem Davydov")
clock = pygame.time.Clock()
###############################
#       Persons
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 3
        self.image = pygame.transform.scale(player_sprite, (120, 140))
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        sprites.add(bullet)
        bullets.add(bullet)


# Enemy
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_sprite, (120, 140))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(0, width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

#       BULLET
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_sprite
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#       BOOM

class Boom(pygame.sprite.Sprite):
    def __init__(self, c, s):
        pygame.sprite.Sprite.__init__(self)
        self.size = s
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = c
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


bullets = pygame.sprite.Group()
sprites = pygame.sprite.Group()
enemy = pygame.sprite.Group()
player = Player()
sprites.add(player)
for i in range(5):
    en_emy = EnemyShip()
    sprites.add(en_emy)
    enemy.add(en_emy)

explosion_anim = {}
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(image_folder, filename)).convert()
    img.set_colorkey(black)
    img = pygame.transform.scale(img, (75, 75))
    explosion_anim['sm'].append(img)
###############################

def drawText(text, font_size, coords, color=white):
    font = pygame.font.Font("assets/Font/18876.ttf", font_size)
    text = font.render(text, 1, color)
    text_rect = text.get_rect()
    text_w, text_h = text.get_width(), text.get_height()
    text_x, text_y = coords[0], coords[1]
    text_rect.midtop = (text_x, text_y)
    screen.blit(text, text_rect)

start = False
running = True
while running:
    clock.tick(FPS)
    screen.blit(background_image, [0, 0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            start = True
            if event.key == pygame.K_SPACE:
                shoot_sound.play()
                player.shoot()
    if not start:
        drawText("[Press any buttons to start the game]", 45, (width / 2, height / 2))
        drawText("[!] Press the 'A' button to move left and the 'D' button to move right [!]", 45, (width / 2, height - 125))
        drawText("[!] And Press 'Space' button to shoot [!]", 45, (width / 2, height - 70))
    else:
        sprites.update()
        hits = pygame.sprite.groupcollide(enemy, bullets, True, True)
        for hit in hits:
            expl = Boom(hit.rect.center, "sm")
            sprites.add(expl)
            en_emy = EnemyShip()
            sprites.add(en_emy)
            enemy.add(en_emy)
        hits = pygame.sprite.spritecollide(player, enemy, True)
        if hits:
            expl = Boom(hits[0].rect.center, "sm")
            sprites.add(expl)
            start = False
        sprites.draw(screen)
    pygame.display.flip()
pygame.quit()