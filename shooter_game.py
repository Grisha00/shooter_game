#Создай собственный Шутер!
from pygame import *
from random import randint
font.init()
mixer.init()
W_W = 700  # Ширина окна
W_H = 500  # Высота окна

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        sprite_img = image.load(img)
        self.image = transform.scale(sprite_img, (w, h))
        self.rect = self.image.get_rect()  # rect(x:0, y:0, w:w, h:h)
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Counter(sprite.Sprite):
    def __init__(self, x, y, text, value, size):
        super().__init__()
        self.text = text
        self.value = value
        self.font = font.SysFont('Arial', size)
        self.image = self.font.render(self.text + ":" + str(self.value), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def add(self, value):
        self.value += value
        self.image = self.font.render(self.text + ":" + str(self.value), True, (255, 255, 255))
    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global player
        global bullets
        global is_win
        global is_loose
        is_strike = False
        for bullet in bullets:
            is_strike = sprite.collide_rect(self, bullet)
            if is_strike:
                bullet.kill()
                break
        if self.rect.y >= W_H or is_strike:
            self.rect.y = 0
            self.rect.x = randint(0, W_W - self.rect.width)
            self.speed = randint(1, 3)    
            if is_strike:
                global score
                score.add(1)
                if score.value == 35:
                    is_win = True
            else:
                global missed
                missed.add(1)
                if score.value == 10:
                    is_loose = True
        if sprite.collide_rect(self, player): # попадание игрока
            is_loose = True
class Asteroid(GameSprite):
    def update(self):
        global bullets
        global is_loose
        global player
        self.rect.y += self.speed
        if self.rect.y >= W_H:
            self.rect.y = 0
            self.rect.x = randint(0, W_W - self.rect.width)  
        for bullet in bullets:
            if sprite.collide_rect(self, bullet):
                bullet.kill()
        if sprite.collide_rect(self, player):
            is_loose = True

class Bullet(GameSprite):
    def update(self,):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Player(GameSprite):
    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= self.speed
    def move_right(self):
        if self.rect.x + self.rect.width < W_W:
            self.rect.x += self.speed
    def fire(self):
        global bullets
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.y, 10, 20, 5)
        bullets.add(bullet)

#создай окно игры
window = display.set_mode((W_W, W_H))
display.set_caption("Шутер")
#задай фон сцены
background_img = image.load("galaxy.jpg")
background = transform.scale(background_img, (W_W, W_H))



#создай 2 спрайта и размести их на сцене
player = Player("rocket.png", 325, 430, 50, 70, 9)
enemies = sprite.Group()
for i in range(6):
    enemy = Enemy(
        "ufo.png", 
        randint(0, W_W - 60), 0, 
        60, 40, 
        randint(1, 2)
    )
    enemies.add(enemy)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid("asteroid.png", randint(0, W_W - 60), 0, 40, 40, 1)
    asteroids.add(asteroid)
bullets = sprite.Group()
score = Counter(10, 10, "Счёт", 0, 40)
missed = Counter(10, 35, "Пропущено", 0, 40)
clock = time.Clock()

#обработай событие «клик по кнопке "Закрыть окно"»
mixer.music.load('space.ogg')
is_win = False
is_loose = False
mixer.music.play()
fire = mixer.Sound('fire.ogg')
game = True
fnt = font.SysFont('Arial', 70)
win = fnt.render("ПОБЕДА!", True, (0, 255, 0)) # Картинка выйграл
loose = fnt.render("GAME OVER", True, (255, 0, 0)) #Картинка проиграл
while game:
    clock.tick(60)
    # Тут обрабатываем события
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            fire.play()
            player.fire()

    # Тут правила
    if not is_win and not is_loose:
        keys = key.get_pressed()
        if keys[K_LEFT]:
            player.move_left()
        if keys[K_RIGHT]:
            player.move_right()
        enemies.update()
        bullets.update()
        asteroids.update()

    # Тут мы всё отрисовываем
    window.blit(background, (0, 0))
    player.reset(window)
    score.reset(window)
    missed.reset(window)
    enemies.draw(window)
    bullets.draw(window)
    asteroids.draw(window)
    if is_win:
        window.blit(win, (200, 150))
    if is_loose:
        window.blit(loose, (200, 150))
    display.update()