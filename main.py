import pygame
pygame.init()

gameWidth = 852
gameHeight = 480

win = pygame.display.set_mode((gameWidth, gameHeight), vsync=1)
pygame.display.set_caption("Grimgore")

walkRight = [pygame.image.load(f'assets/assets/R{n}.png') for n in range(1, 10)]
walkLeft = [pygame.image.load(f'assets/assets/L{n}.png') for n in range (1, 10)]
bg = pygame.image.load('assets/assets/bg.jpg')
char = pygame.image.load('assets/assets/standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('assets/assets/bullet.mp3')
hitSound = pygame.mixer.Sound('assets/assets/hit.mp3')
playerHit = pygame.mixer.Sound('assets/assets/player_hit.mp3')

music = pygame.mixer.music.load('assets/assets/music.mp3')
pygame.mixer.music.play(-1)

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.jumpCount = 10
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
       # To draw hitbox:
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
    
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 300
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.Font(None, 48)
        loss_text = font1.render('-50', 1, (255, 0, 0))
        win.blit(loss_text, ((gameWidth / 2) - (loss_text.get_width() / 2), (gameHeight / 2) - (loss_text.get_height() / 2)))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 7 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def redrawGameWindow():
    win.blit(bg, (0,0))
    score_text = score_font.render(f'Score: {score}', True, (0, 0, 0))
    win.blit(score_text, (10, 10))
    butch.draw(win)
    gob1.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

class enemy(object):
    walkRight = [pygame.image.load(f'assets/assets/R{n}E.png') for n in range(1, 12)]
    walkLeft = [pygame.image.load(f'assets/assets/L{n}E.png') for n in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 20, 45)
        self.health = 100
        self.visible = True
        self.directionCounter = 0

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 10, 10), (self.hitbox[0], self.hitbox[1] - 20, 50, 10) )
            pygame.draw.rect(win, (10, 130, 10), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (100 - self.health) / 10) , 10 ))
            self.hitbox = (self.x + 17, self.y + 2, 20, 45)
            # To draw hitbox:
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount =0
    
    def hit(self):
        if self.health > 11:  
            self.health -= 10
        else:
            self.visible = False
        # test hitting:
        # print('hit')
            
    def player_hit(self):
        self.x = 100
        self.y = 410
        self.walkCount = 0
    
    def respawn(self):
        if self.directionCounter == 0:
            self.x = 0
            self.directionCounter = 1
        else:
            self.x = gameWidth - 10
            self.vel *= -1
            self.directionCounter = 0

        self.y = 410
        self.walkCount = 0
        self.visible = True
        self.health = 100



# main loop
butch = player(300, 410, 64, 64)
gob1 = enemy(100, 410, 64, 64, 600)
bulletLoop = 0
bullets = []
respawnLoop = 0
score = 0
score_increment = 5
run = True
while run:
    clock.tick(60)

    score_font = pygame.font.Font(None, 40)

    if bulletLoop > 0:
        bulletLoop += 1
    if bulletLoop > 10:
        bulletLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if gob1.visible == True:
        if butch.hitbox[1] < gob1.hitbox[1] + gob1.hitbox[3] and butch.hitbox[1] + butch.hitbox[3] > gob1.hitbox[1]:
            if butch.hitbox[0] + butch.hitbox[2] > gob1.hitbox[0] and butch.hitbox[0] < gob1.hitbox[0] + gob1.hitbox[2]:
                playerHit.play()
                score -= 50
                butch.hit()
                gob1.player_hit()
    
    if gob1.visible == False:
        if respawnLoop < 100:
            respawnLoop += 1
        else:
            respawnLoop = 0
            gob1.respawn()


    for bullet in bullets:
        if gob1.visible == True:
            if bullet.y - bullet.radius < gob1.hitbox[1] + gob1.hitbox[3] and bullet.y + bullet.radius > gob1.hitbox[1]:
                if bullet.x + bullet.radius > gob1.hitbox[0] and bullet.x - bullet.radius < gob1.hitbox[0] + gob1.hitbox[2]:
                    hitSound.play()
                    gob1.hit()
                    score += score_increment
                    bullets.pop(bullets.index(bullet))
            
        if bullet.x < gameWidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_q] and bulletLoop == 0:
        if butch.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 3:
            bullets.append(projectile(round(butch.x + butch.width // 2), round(butch.y + butch.height // 2), 6, (220, 0, 20), facing))
            bulletSound.play()
        
        bulletLoop = 1

    if keys[pygame.K_a] and butch.x > butch.vel:
        butch.x -= butch.vel
        butch.left = True
        butch.right = False
        butch.standing = False
    elif keys[pygame.K_d] and butch.x < gameWidth - butch.width - butch.vel:
        butch.x += butch.vel
        butch.left = False
        butch.right = True
        butch.standing = False
    else:
        butch.standing = True
        butch.walkCount = 0    

    if not(butch.isJump):
        if keys[pygame.K_SPACE]:
            butch.isJump = True
            butch.walkCount = 0
    else:
        if butch.jumpCount >= -10:
            neg = 1
            if butch.jumpCount < 0:
                neg = -1
            butch.y -= (butch.jumpCount ** 2) * 0.2 * neg
            butch.jumpCount -= 1
        else:
            butch.isJump = False
            butch.jumpCount = 10

    redrawGameWindow()

pygame.quit()