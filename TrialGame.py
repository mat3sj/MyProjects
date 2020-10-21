import pygame, os
pygame.init()

win_size = 500
win = pygame.display.set_mode((win_size,win_size))
pygame.display.set_caption('Jumping square by Mates')

score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.vel = 5
        self.jump_count = 10
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.hitbox = (self.x + 3, self.y + 3, 30, 27)
        self.hit_jump_count = 5

    # image load
    cwd = os.path.dirname(__file__)
    image_dir = os.path.join(cwd,'pig')
    images_left = ['left1','left2','left3','left4','left5','left6','left7','left8','left9','left10','left11','left12']
    images_right = ['right1','right2','right3','right4','right5','right6','right7','right8','right9','right10','right11','right12']
    walk_left = []
    walk_right = []
    for idx in range (len(images_left)):        
        walk_left.append(pygame.image.load(os.path.join(image_dir,images_left[idx]+'.png')))
        walk_right.append(pygame.image.load(os.path.join(image_dir,images_right[idx]+'.png')))
   
    def draw(self,win):
        if self.walk_count + 1 >=12:
            self.walk_count = 0
        if self.left:
            win.blit(self.walk_left[self.walk_count], (self.x, self.y))
        else:
            win.blit(self.walk_right[self.walk_count], (self.x, self.y))
        self.hitbox = (self.x, self.y, 32, 32)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox,2)
    
    def hit(self):
        if self.hit_jump_count >= -5:
            neg = 1
            if self.hit_jump_count < 0:
                neg = -1            
            self.y -= (self.hit_jump_count ** 2) * 0.2 * neg
            self.hit_jump_count-= 1
        else:
            self.hit_jump_count = 5
        hit_font = pygame.font.SysFont('arial',20)
        text = hit_font.render('-5',1, (255,0,0))
        win.blit(text,(win_size/2 - text.get_width()/2, win_size/2))
        pygame.display.update()
        delay = 300
        i = 0
        while i < delay:
            #pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = delay + 1
                    pygame.quit()
            
class bird(object):
    def __init__(self, x, y, width, height, move_range):
        self.x, self.y = x, y
        self.width, self.height = width, height
        if self.x + move_range > win_size-width:
            self.end = win_size-width
        else:
            self.end = self.x + move_range
        self.walk_count = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x, self.y, 32, 32)
        self.health = 10
        self.visible = True
    
    # image load
    cwd = os.path.dirname(__file__)
    image_dir = os.path.join(cwd,'bird')
    images_left = ['left1','left2','left3','left4','left5','left6','left7','left8','left9']
    images_right = ['right1','right2','right3','right4','right5','right6','right7','right8','right9']
    walk_left = []
    walk_right = []
    for idx in range (len(images_left)):
        walk_left.append(pygame.image.load(os.path.join(image_dir,images_left[idx]+'.png')))
        walk_right.append(pygame.image.load(os.path.join(image_dir,images_right[idx]+'.png')))

    def draw(self, win):
        if self.visible:
            self.move()
            if self.walk_count + 1 >=18:
                self.walk_count = 0
            if self.vel < 0:
                win.blit(self.walk_left[self.walk_count//2], (self.x, self.y))
            else:
                win.blit(self.walk_right[self.walk_count//2], (self.x, self.y))
            self.walk_count +=1
            self.hitbox = (self.x, self.y, 32, 32)
            # Health bar
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0],self.hitbox[1]-20,50 - 5*(10-self.health),10))
            # Drawing a hitbox
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walk_count = 0
        else:
            if self.x - self.vel> self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walk_count = 0
                
    def hit(self):
        self.health -= 1
        if not self.health:
            self.visible = False

class projectile(object):
    def __init__(self,x,y,radius,direction,color):
        self.x = x
        self.y = y
        self.height = radius * 2
        self.width = radius *2
        self.vel = 8 * direction
        self.color = color
        self.radius = radius
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y),self.radius)

def redraw_game_window():
    text = score_font.render('Score: ' + str(score), 1, (255,0,0))
    win.fill((255,255,0))
    win.blit(text, (390,10))
    pig.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

run = True
score_font = pygame.font.SysFont('arial', 20, True)
pig = player(400,400,32,30)
bro = bird(100,400,32,32,400)
bullets = []
shoot_loop = 0
enemies = []

enemies.append(bro)

# Main game loop
while run:
    pygame.time.delay(50)

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
        # my bullets
    for enemy in enemies:
            if not enemy.visible:
                enemies.pop(enemies.index(enemy))
            # collision with an enemy
            if pig.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and pig.hitbox[1] + pig.hitbox[3]> enemy.hitbox[1]:
                if pig.hitbox[0] + pig.hitbox [2] > enemy.hitbox[0] and pig.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                    pig.hit()
                    score -= 1

    for bullet in bullets:
        for enemy in enemies:
            if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
                if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                    enemy.hit()
                    score += 5
                    bullets.pop(bullets.index(bullet))

        if bullet.x < win_size and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and not shoot_loop:
        if pig.left:
            direction = -1
        else:
            direction = 1
        if len(bullets) < 10:
            bullets.append(projectile(round(pig.x + pig.width//2),round(pig.y + pig.height//2),4,direction,(255,0,0)))
        shoot_loop = 1
    if keys[pygame.K_LEFT] and pig.x >= pig.vel:
        pig.x -= pig.vel
        pig.left = True
        pig.right = False
        pig.walk_count += 1
    if keys[pygame.K_RIGHT] and pig.x <= win_size - pig.width - pig.vel:
        pig.x += pig.vel
        pig.left = False
        pig.right = True
        pig.walk_count += 1
    if not pig.is_jump:
        if keys[pygame.K_UP]:
            pig.is_jump = True
    else:
        if pig.jump_count >= -10:
            neg = 1
            if pig.jump_count < 0:
                neg = -1            
            pig.y -= (pig.jump_count ** 2) * 0.2 * neg
            pig.jump_count -= 1
        else:
            pig.jump_count = 10
            pig.is_jump = False
    redraw_game_window()

pygame.quit()