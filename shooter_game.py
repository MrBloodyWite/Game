from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y, ))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 615:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 415:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        
bullets = sprite.Group()

lost = 0
score = 0
goal = 10
max_lost = 5

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        
        if self.rect.y > 500:
            lost = lost + 1



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > 500:
            self.rect.x = randint(40, 600)
            self.rect.y = 0
            lost = lost + 1

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

window = display.set_mode((700, 500))
display.set_caption('Симулятор MrBeast')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

rocket = Player('rocket.png', 80, 400, 80, 100, 5)

monsters = sprite.Group()
for i in range(0, 6):
    monster = Enemy('ufo.png', randint(40, 600), 0, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(30, 600), 0, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

game = True
finish = False
clock = time.Clock()
FPS = 25

font.init()
font2 = font.Font(None, 70)
win = font2.render('YOU WIN!', True, (255, 215, 0))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))

fire_sound = mixer.Sound('fire.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
    if not finish:

        window.blit(background, (0, 0))

        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))



        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        display.update()
        clock.tick(FPS)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(40, 600), 0, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(rocket, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True 
            window.blit(win, (200, 200))




