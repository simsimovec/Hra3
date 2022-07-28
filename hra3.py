import pygame
import pygame.locals
import sys
import random

winWidth = 1024
winHeight = 768

playerWidth = 60
playerHeight = 20

posx=winWidth/2 - playerWidth/2
posy=winHeight - 20 - playerHeight-200

moveleft = False
moveright = False

speedx = 8.0

gamestate = "start"

fallSpeed = 4.0
thingEventInterval = 350
thingCnt = 3

itemSize = 20

class Player():
    def __init__(self, posx, posy, speedx, filename, windowWidth):
        self.surface = pygame.image.load(filename).convert_alpha()
        self.posX = posx
        self.posY = posy
        self.playerWidth = self.surface.get_width()
        self.playerHeight = self.surface.get_height()
        self.speedX = speedx
        self.moveleft = False
        self.moveright = False
        self.maxRight = windowWidth - self.playerWidth
        self.flip = True
        self.body = 0
    
    def update(self):
        if self.moveleft:
            self.posX = self.posX - self.speedX
            self.flip = True
            if self.posX < 0:
                self.moveleft = False
                self.posX = 0

        if self.moveright:
            self.flip = False
            self.posX = self.posX + self.speedX
            if self.posX > self.maxRight:
                self.moveright = False
                self.posX = self.maxRight

    def draw(self, window):
        # pygame.draw.rect(window, (168, 168, 168), (self.posX, self.posY,self.playerWidth, self.playerHeight))    
        if self.flip:
            window.blit(pygame.transform.flip(self.surface, True, False), (self.posX, self.posY))
        else:
            window.blit(self.surface, (self.posX, self.posY))

class Score():
    def __init__(self, posx = 10):
        self.points = 0
        self.pismo = pygame.font.SysFont("comicsansms", 30)
        self.text = self.pismo.render(str(self.points), True, (200, 200, 200))
        self.posx = posx
    
    def addPoints(self, howMuch = 1):
        self.points += howMuch
        self.text = self.pismo.render(str(self.points), True, (200, 200, 200))

    def draw(self, surface):
        surface.blit(self.text, (self.posx, 10))




class Item():
    def __init__(self):
        self.isFood = random.randint(0,1)
        self.posx = random.randint(0, winWidth - itemSize)
        if self.isFood:
            self.image = pygame.image.load('tary.png')
            self.sizey = self.image.get_height()
        else:
            self.image = pygame.image.load('pendovert.png')
            self.sizey = self.image.get_height()

        self.sizex = self.image.get_width()
        self.posy = - self.sizey

        self.fallSpeed = random.random()/2.0 + fallSpeed
        self.alive = True

        if self.isFood:
            self.color = (0, 200, 0)
        else:
            self.color = (150, 0, 0)
         
    def draw(self, surface):
        surface.blit(self.image, (self.posx, self.posy))
    
    def update(self):
        if self.alive:
            self.posy = self.posy + self.fallSpeed
        if self.posy > winHeight:
            self.alive = False
    
    def collision(self, leftx, rightx, upy, lowy):
        status = 0
        if (self.posy + self.sizey >= upy) and (self.posy < lowy):
            if (self.posx + self.sizex >= leftx) and (self.posx <= rightx):
                if self.alive and self.isFood:
                    status = 1
                elif self.alive and not self.isFood:
                    status = -1
                self.alive = False
                
        return status
        


pygame.init()
window = pygame.display.set_mode((winWidth,winHeight), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
fnt = pygame.font.SysFont("comicsansms", 12)

veci = []
body1 = Score(winWidth - 100)
body2 = Score()
hrac1 = Player(posx, posy, speedx, 'truck_mini.png', winWidth)
hrac2 = Player(posx, posy, speedx, 'trubiroh.png', winWidth)

NEWTHINGEVENT, milisecs, trail = pygame.USEREVENT+1, thingEventInterval, [] 

pygame.time.set_timer(NEWTHINGEVENT, milisecs)

startImage = pygame.image.load('intro.png').convert_alpha()
p1wins = pygame.image.load('truck_mini.png').convert_alpha()
p2wins = pygame.image.load('trubiroh.png').convert_alpha()

def startScreen():
    global gamestate
    for evt in pygame.event.get():
        if evt.type == pygame.KEYDOWN:
            gamestate = "playing"

    pygame.draw.rect(window, (0, 0, 0), (0,0, winWidth, winHeight))
    window.blit(startImage,(winWidth/2 - startImage.get_width()/2,winHeight/2 - startImage.get_height()/2))


def playing():
    global gamestate
    # prochazime vsechny udalosti
    for evt in pygame.event.get():
        # nastala udalost konec?
        if evt.type == pygame.QUIT:
            sys.exit(0)
        if  evt.type == NEWTHINGEVENT:
            for i in range(0,thingCnt):
                veci.append(Item())

        
        #nastala udalost stisknuti klavesy?
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                sys.exit(0)
            if evt.key == pygame.K_LEFT:
                hrac1.moveleft = True
            if evt.key == pygame.K_RIGHT:
                hrac1.moveright = True
            if evt.key == pygame.K_a:
                hrac2.moveleft = True
            if evt.key == pygame.K_d:
                hrac2.moveright = True

        if evt.type == pygame.KEYUP:
            if evt.key == pygame.K_LEFT:
                hrac1.moveleft = False
            if evt.key == pygame.K_RIGHT:
                hrac1.moveright = False
            if evt.key == pygame.K_a:
                hrac2.moveleft = False
            if evt.key == pygame.K_d:
                hrac2.moveright = False


    # smazat hrace
    # TODO upravit mazani hrace
    pygame.draw.rect(window,(0, 0, 0),(posx,posy,playerWidth,playerHeight))

    # Smazat objeky
    # TODO: optimalizovat mazani objektu
    pygame.draw.rect(window, (0, 0, 0), (0,0, winWidth, winHeight))


    # posuneme hrace
    hrac1.update()
    hrac2.update()
    for vec in veci:
        vec.update()

    # jdeme kreslit hrace
    hrac1.draw(window)
    hrac2.draw(window)
    
    for vec in veci:
        kolize1 = vec.collision(hrac1.posX, hrac1.posX+hrac1.playerWidth, hrac1.posY, hrac1.posY + hrac1.playerHeight)
        kolize2 = vec.collision(hrac2.posX, hrac2.posX+hrac2.playerWidth, hrac2.posY, hrac2.posY + hrac2.playerHeight)
        if not vec.alive:
            veci.remove(vec)
        if kolize1 == 1:    
            body1.addPoints(10)
        elif kolize1 == -1:
            body1.addPoints(-100)
        if kolize2 == 1:    
            body2.addPoints(10)
        elif kolize2 == -1:
            body2.addPoints(-100)
        vec.draw(window)

    body1.draw(window)
    body2.draw(window)
    if body1.points >= 500 or body2.points <= -500:
        gamestate = "p1wins"
    if body2.points >= 500 or body1.points <= -500:
        gamestate = "p2wins"
    
    statistics = fnt.render("Pocet objektu: " + str(len(veci)), True, (200, 200, 200))
    window.blit(statistics, (10, 100))


def gameOver():
    global gamestate
    global hrac1, hrac2
    for evt in pygame.event.get():
        if evt.type == pygame.KEYDOWN:
            gamestate = "playing"
            body1.points = 0
            body2.points = 0


    pygame.draw.rect(window, (0, 0, 0), (0,0, winWidth, winHeight))
    if gamestate == "p1wins":
        window.blit(p1wins,(winWidth/2 - startImage.get_width()/2,winHeight/2 - startImage.get_height()/2))
    else:
        window.blit(p2wins,(winWidth/2 - startImage.get_width()/2,winHeight/2 - startImage.get_height()/2))


while True:

    if gamestate == "start":
        startScreen()
    elif gamestate == "playing":
        playing()
    else:
        gameOver()

    clock.tick(60)
    pygame.display.flip()

