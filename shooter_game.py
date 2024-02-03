from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__ (self, img, x, y, speed, width = 65, height = 65):
        super().__init__()
        self.image = image.load(img)
        self.image = transform.scale(self.image, (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LSHIFT]:
            self.speed = 10
        else:
            self.speed = 5

        if keys[K_d] and self.rect.x < 700 - 65:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -10,15,20)
        bullets.add(bullet)
        

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(50, 500)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -20:
            self.kill()

player = Player("rocket.png", 400, 425, 5)

enemies = sprite.Group()

for i in range(6):
    enemy = Enemy("ufo.png", randint(50, 500), 0, randint(1, 4))
    enemies.add(enemy)

SCREENSIZE = (700, 500)
TEXTCOLOR = (255, 255, 255)
display.set_caption('shooter')
window = display.set_mode(SCREENSIZE)

background_img = image.load("galaxy.jpg")
background = transform.scale(background_img, (SCREENSIZE))

mixer.init()
mixer.music.load('03-gungeon-up-gungeon-down_b568sfd4.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.2)

time = time.Clock()
FPS = 60

bullets = sprite.Group()

run = True
finish = False

font.init()
fontfamily = font.Font(None, 40)

lost = 0
killed = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
    




if killed >= 50:
    finish = True
elif lost >= 10:
    finish = True





    if finish != True:





        deleted = sprite.groupcollide(enemies,bullets,True,True)
        for element in deleted:
            enemy = Enemy("ufo.png", randint(50, 500), 0, randint(1, 4))
            enemies.add(enemy)
            killed += 1



        window.blit(background, (0, 0))
        player.reset()
        player.update()

        enemies.draw(window)
        enemies.update()

        bullets.draw(window)
        bullets.update()

        lost_text = fontfamily.render("Пропущено 10/ " + str(lost ,) ,True, TEXTCOLOR)
        killed_text = fontfamily.render("Счет 50/" + str(killed), True, TEXTCOLOR)

        window.blit(lost_text, (10, 10))
        window.blit(killed_text, (10, 50))

    display.update()
    time.tick(FPS)