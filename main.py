# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import pygame, time, os, random

pygame.font.init()


WIDTH, HEIGHT = 800, 1000

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game test")

#main player
Red_Ship = pygame.transform.scale(pygame.image.load(os.path.join("assets", "red ship.png")), (75,75))

#enemy cpus
Blue_Ship = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blue ship.png")), (75,75))
Green_Ship = pygame.transform.scale(pygame.image.load(os.path.join("assets", "green ship.png")), (75,75))
Yellow_Ship = pygame.transform.scale(pygame.image.load(os.path.join("assets", "yellow ship.png")), (75,75))
#lasers
Red_Laser = pygame.transform.scale(pygame.image.load(os.path.join("assets", "red laser.png")), (80,80))
Blue_Laser = pygame.image.load(os.path.join("assets", "blue laser.png"))
Green_Laser = pygame.image.load(os.path.join("assets", "green laser.png"))
Yellow_Laser = pygame.image.load(os.path.join("assets", "yellow laser.png"))
#background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bgreal.png")), (WIDTH, HEIGHT))
class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        win.blit(self.img, (self.x, self.y))


    def move (self, vel):
        self.y += vel

    def off_screen (self, height):
        return not(self.y <HEIGHT and self.y >=0)

    def collision (self, obj):
        return collide(self, obj)

class Ship:
     COOLDOWN = 15
     def __init__(self, x, y, health=100):
         self.x = x
         self.y = y
         self.health = health
         self.ship_img = None
         self.laser_img = None
         self.lasers = []
         self.cool_down_counter = 0

     def draw(self, window):
         window.blit(self.ship_img, (self.x,self.y))
         for laser in self.lasers:
             laser.draw(window)

     def movelasers(self, vel, obj):
         self.cooldown()
         for laser in self.lasers:
             laser.move(vel)
             if laser.off_screen(HEIGHT):
                 self.lasers.remove(laser)
             elif laser.collision(obj):
                 obj.health -= 40
                 self.lasers.remove(laser)

     def cooldown(self):
         if self.cool_down_counter >= self.COOLDOWN  :
             self.cool_down_counter = 0
         elif self.cool_down_counter > 0:
             self.cool_down_counter += 1
     def shoot(self):
         if self.cool_down_counter == 0:
             laser = Laser(self.x, self.y, self.laser_img)
             self.lasers.append(laser)
             self.cool_down_counter = 1


     def get_width(self):
         return self.ship_img.get_width()
     def get_height(self):
         return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y , health)
        self.ship_img = Red_Ship
        self.laser_img = Red_Laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    def movelasers(self, vel, objs):
         self.cooldown()
         for laser in self.lasers:
             laser.move(vel)
             if laser.off_screen(HEIGHT):
                 self.lasers.remove(laser)
             else:
                 for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
class Enemy(Ship):
    colormap = {
                "blue": (Blue_Ship, Blue_Laser),
                "green": (Green_Ship, Green_Laser),
                "yellow": (Yellow_Ship, Yellow_Laser)
    }
    def __init__(self,x,y,color,health = 100):
        super().__init__(x,y,health)
        self.ship_img, self.laser_img = self.colormap[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None



def main():

    run = True
    fps = 100
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 70)
    enemies = []
    wavelength = 5
    enemy_vel = 1
    lost = False
    lostcount = 0
    player_vel = 8
    laser_vel = 6
    player = Player(300,650)
    clock = pygame.time.Clock()

    def redraw_window():
        win.blit(BG, (0,0))

        #draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        win.blit(lives_label, (10,10))
        win.blit(level_label, (WIDTH - level_label.get_width()-10, 10))

        for enemy in enemies:
            enemy.draw(win)

        player.draw(win)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            win.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2))




        pygame.display.update()


    while run:
        clock.tick(fps)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lostcount += 1
        if lost:
            if lostcount > fps*3:
                run = False
            else:
                continue


        if len(enemies) == 0:
            level += 1
            wavelength += 5
            for i in range(wavelength):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["yellow", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel>0: #left
            player.x -= player_vel
        if keys[pygame.K_w] and player.y - player_vel >0: #up
            player.y -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #right
            player.x += player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT  : #down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.movelasers(laser_vel,player)

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.movelasers(-laser_vel, enemies)
main()




