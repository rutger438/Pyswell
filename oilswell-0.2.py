"""
Auther: Rutger van Teutem
Version: 0.2
Release date: May 17th 2016
Python version: 2.7
Requires: pygame
"""
import pygame, random
from pygame.locals import *
screen = pygame.display.set_mode((640, 480),HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.transform.set_smoothscale_backend('SSE')

"""The screen manager manages all draw functions and also has some pre-made
functions for drawing presets like images."""
class ScreenManager():
    def __init__(self):
        self.surf = pygame.Surface((640, 480), pygame.SRCALPHA, 32)
        self.width = 800
        self.height = 600
        self.imgcache = {}

    def get_surf(self):
        return self.surf
        
    #draw trys to blit and draw the given suface at the location specified.
    def draw(self, obj, x, y): 
        try:
            self.surf.blit(obj, (x, y))
        except:
            pass

    """draw_img is a pre-made function for drawing images at a specified size
       in a specified place."""
    def draw_img(self, f, x, y, w=0, h=0):
        if f not in self.imgcache.keys():
            img = pygame.image.load(f)
            if w and h:
                img = pygame.transform.scale(img, (w, h))
            img2 = pygame.image.tostring(img, "RGBA")
            self.surf.blit(img, (x, y))
            self.imgcache[f] = [img2, img.get_width(), img.get_height()]
        else:
            img = pygame.image.frombuffer(self.imgcache[f][0], (self.imgcache[f][1], self.imgcache[f][2]), "RGBA")
            self.surf.blit(img, (x, y))

    #Draw circle at position with the color of color
    def draw_circle(self, color, pos):
        #Call pygame circle drawer and convert World posistion to screen position
        circle = pygame.draw.circle(self.surf, color, (int((pos[0] + 0.5)*22+12), int((pos[1] + 0.5)*22+12)), 11)
    
    def clear(self): #Clears the screen by filling it with black
        self.surf = pygame.Surface((640, 480), pygame.SRCALPHA, 32)
        screen.fill((0,0,0))

    def set_size(self, (width, height)):
        self.width = width
        self.height = height

    def is_large(self):
        if self.width>(640*2) and self.height>(480*2):
            return True
        else:
            return False
    
    def update(self): #Updates the screen every tick
        if self.width>(640*2) and self.height>(480*2):
            self.surf = pygame.transform.scale2x(self.surf)
        screen.blit(self.surf, (0, 0))
        pygame.display.update()


"""The world manager loads the map from a txt file and draws it to the screen,
it also has funtions for returning tiles based on coorinates."""
class WorldManager():
    #load_map loads the specified map into a 2D array
    def load_map(self, level):
        tiles_width = 28
        tiles_height = 16
        tiles_size = (22,22)
        self.tile_array = []
        self.level = level
        img1 = pygame.image.tostring(pygame.image.load('./images/0.png'), "RGBA")
        img2 = pygame.image.tostring(pygame.image.load('./images/1.png'), "RGBA")
        img3 = pygame.image.tostring(pygame.image.load('./images/12.png'), "RGBA")
        self.imgs = {'0':img1, '1':img2, '2':img3}
        with open ("./levels/"+level+".txt", "r") as myfile:
            file_array=[[digit for digit in line.strip()] for line in myfile]
        self.tile_array = file_array
        self.max_score = 0
        for line in self.tile_array:
            for item in line:
                if item == '1':
                    self.max_score = self.max_score + 1

    def isLoaded(self):
        if len(self.tile_array) > 0:
            return True
        return False

    def getMaxScore(self):
        return self.max_score

    def loadFinish(self):
        with open ("./levels2/"+self.level+"f.txt", "r") as myfile:
            file_array=[[digit for digit in line.strip()] for line in myfile]
        i=0
        j=0
        for line in file_array:
            for block in line:
                if block == '3':
                    self.tile_array[i][j] = '3'
                j=j+1
            j=0
            i=i+1
        self.tile_array

    def get_player_pos(self):
        i=0
        j=0
        for row in self.tile_array:
            for item in row:
                if item == "p":
                    return i, j
                i=i+1
            j=j+1
            i=0

    def get_enemies(self):
        a = []
        i=0
        j=0
        for row in self.tile_array:
            for item in row:
                if item == "e":
                    a.append([i, j])
                i=i+1
            j=j+1
            i=0
        return a

    #draw_map draws the loaded map to the screen manager specified
    def draw_map(self, sm):
        x = 0
        y = 0
        for line in self.tile_array:
            x = 0
            for char in line:
                if char:
                    img = pygame.image.frombuffer(self.imgs[str(char)], [22, 22], "RGBA")
                    sm.draw(img, x*22+12, y*22+92)
                x = x + 1
            y = y + 1

    #get_tile returns the value of a tile based on x and y coordinates
    def get_tile(self, x, y):
        tile = self.tile_array[int(y)][int(x)]
        return tile

    #Sets tile to a specified value
    def set_tile(self, x, y, value):
        self.tile_array[int(y)][int(x)] = value

    #get_tile_array returns the self.tile_array
    def get_tile_array(self):
        return self.tile_array
    
    #get_tile_solid returns if a tile is solid based on x and y coordinates
    def get_tile_solid(self, x, y):
        try:
            tile = self.tile_array[int(y)][int(x)]
        except:
            return 'False'
        if tile == '1':
            return 'False'
        elif tile == '2':
            return 'True'
        elif tile == '3':
            return 'Ladder'
        elif tile == '4':
            return 'Line'
        elif tile == '5':
            return 'False'
        else:
            return 'False'
class Enemy():
    def __init__(self, pos = [0,0], direction = 0, speed = 1):
        self.pos = pos
        self.direction = direction
        self.speed = speed
        if self.direction:
            self.speed = -self.speed
    def update(self, path):
        if self.pos in path[:-2]:
           #print "YEEEEAAAAAAAHHHH"
            return 1
        elif self.pos in path:
           #print "YEEEEAAAAAAAHHHH"
            return 2
        self.pos[0] = self.pos[0] + self.speed
        return False
    def offScreen(self):
        if self.pos[0] < 0:
            return True
        if self.pos[0] > 32:
            return True
        return False
    def draw(self, sm):
        sm.draw_img('./images/11.png', self.pos[0]*22+12, self.pos[1]*22+92, 22, 22)
"""Main runs and updates the game"""
class Main():
    #Setting up initial values
    pygame.init() #initialize pygame
    pygame.font.init() #initialize the pygame font manager
    wm = WorldManager() #create new WorldManager Class Instance
    sm = ScreenManager() #create new ScreenManager Class Instance
    #pm = PlayerManager() #create new PlayerManager Class Instance
    #pm.new_player((1.0,1.0), 10) #initialize the player with required args
    wm.load_map('1') #Load the first level with the WorldManager
    #gp = GeneratePath(wm, pm) #Initialize path finding system
    #broken_blocks = [] #List for storing destroyed blocks
    ticker = 0 #Tick counter for timed events
    idle_ticker = 0 #Tick counter for Idle Event
    #enemy = Enemy(20, 14) #Make new enemy
    score = 0 #Set base score
    clock = pygame.time.Clock() #Create clock value
    font = pygame.font.Font("./fonts/perfect-dos.ttf", 32) #Load font
    menu_items = ['Play', 'Highscores', 'Quit']
    path = [[13,0]]
    path_imgs = [3]
    playing = False
    menu = False
    username = True
    highscores = False
    travel_distance = 0
    name = ''
    global sort_scores
    sort_scores = 0
    last_move = [3]
    enemy_ticker = 0
    enemies = []
    end = False
    img1 = pygame.image.tostring(pygame.image.load('./images/2.png'), "RGBA")
    img2 = pygame.image.tostring(pygame.image.load('./images/3.png'), "RGBA")
    img3 = pygame.image.tostring(pygame.image.load('./images/4.png'), "RGBA")
    img4 = pygame.image.tostring(pygame.image.load('./images/5.png'), "RGBA")
    img5 = pygame.image.tostring(pygame.image.load('./images/6.png'), "RGBA")
    img6 = pygame.image.tostring(pygame.image.load('./images/7.png'), "RGBA")
    imgs = {'2':img1, '3':img2, '4':img3, '5':img4, '6':img5, '7':img6}
    while not end:
        while username:
            sm.clear() #Clear the screen
            text = font.render("Please type your name and hit Enter.", 1, (220,230,243))
            sm.draw(text, 0, 150)
            event=pygame.event.poll()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    name = name[:-1]
                elif event.key == K_RETURN:
                    username = False
                    menu = True
                else:
                    name = name + event.unicode
            if event.type==QUIT: #If the window is closed
                pygame.display.quit()
                pygame.quit()
                end = True
                menu = False
                break
            rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(200, 200, 300, 30))
            sm.draw(rect, 200, 200)
            text = font.render(str(name), 1, (220,230,243))
            sm.draw(text, 200, 200)
            pygame.event.pump() #Process event queue
            sm.update() #Update screen
        while menu:
            sm.clear() #Clear the screen
            sm.draw_img('./images/bg.png', 0, 0, 640, 92)
            wm.draw_map(sm) #Draw the world
            rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(10, 50, font.size(str(name))[0]+8, 30))
            sm.draw(rect, 10, 50)
            text = font.render(str(name), 1, (220,220,220))
            sm.draw(text, 15, 48)
            event=pygame.event.poll() #Poll events and store in event
            if event.type==QUIT: #If the window is closed
                pygame.display.quit()
                pygame.quit()
                end = True
                menu = False
                break
            elif event.type==VIDEORESIZE: #If window is resized
                #Resize screen value
                screen=pygame.display.set_mode(event.dict['size'],
                                               HWSURFACE|DOUBLEBUF|RESIZABLE)
                sm.set_size(event.dict['size'])
            pygame.event.pump() #Process event queue
            i=0
            for tile in path:
                if i > 0:
                    img = pygame.image.frombuffer(imgs[str(path_imgs[i])], [22, 22], "RGBA")
                    sm.draw(img, path[i-1][0]*22+12, path[i-1][1]*22+92)
                i=i+1
            if last_move[-1] == 1:
                sm.draw_img('./images/8.png', path[-1][0]*22+12, path[-1][1]*22+92, 22, 22)
            if last_move[-1] == 2:
                sm.draw_img('./images/9.png', path[-1][0]*22+12, path[-1][1]*22+92, 22, 22)
            if last_move[-1] == 3:
                sm.draw_img('./images/10.png', path[-1][0]*22+12, path[-1][1]*22+92, 22, 22)
            y=100
            for item in menu_items:
                text = font.render(str(item), 1, (220,230,243))
                rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(320-(font.size(str(item))[0])/2, y, font.size(str(item))[0]+3, 30))
                sm.draw(rect, 200, 30)
                sm.draw(text, 328-(font.size(str(item))[0]+8)/2, y)
                pos = pygame.mouse.get_pos()
                if pos[1] > y and pos[1] < y + 30:
                    if pygame.mouse.get_pressed()[0]:
                        if item == 'Play':
                            playing = True
                            menu = False
                            #pm.new_player((1.0,1.0), 10) #initialize the player with required args
                            if not wm.isLoaded():
                                wm.load_map('1') #Load the first level with the WorldManager
                            #gp = GeneratePath(wm, pm) #Initialize path finding system
                            broken_blocks = [] #List for storing destroyed blocks
                            enemiesPos = wm.get_enemies()
                            for enemy in enemies:
                                del enemy
                            enemies = []
                            #print 'score = ', score
                            for pos in enemiesPos:
                               #print 'new enemy at:', pos
                                enemy = Enemy(pos[0], pos[1])
                                enemies.append(enemy)
                        if item == 'Highscores':
                            highscores = True
                            menu = False
                        if item == 'Quit':
                            pygame.display.quit()
                            pygame.quit()
                            end = True
                            menu = False
                            break
                y = y + 40
            #pm.draw_player(sm) #Draw Player
            if not end:
                sm.update() #Update screen
        while highscores:
            sm.clear() #Clear the screen
            sm.draw_img('./images/bg.png', 0, 0, 640, 92)
            wm.draw_map(sm) #Draw the world
            rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(10, 50, font.size(str(name))[0]+8, 30))
            sm.draw(rect, 10, 50)
            text = font.render(str(name), 1, (220,220,220))
            sm.draw(text, 15, 48)
            event=pygame.event.poll() #Poll events and store in event
            if event.type==QUIT: #If the window is closed
                pygame.display.quit()
                pygame.quit()
                end = True
                highscores = False
                break
            elif event.type==VIDEORESIZE: #If window is resized
                #Resize screen value
                screen=pygame.display.set_mode(event.dict['size'],
                                               HWSURFACE|DOUBLEBUF|RESIZABLE)
                sm.set_size(event.dict['size'])
            pygame.event.pump() #Process event queue
            y=100
            rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(10, 10, 70, 30))
            sm.draw(rect, 10, 10)
            text = font.render('Back', 1, (220,230,243))
            sm.draw(text, 10, 10)
            if pos[1] > 10 and pos[1] < 10 + 30 and pos[0] > 10 and pos[0] < 80:
                if pygame.mouse.get_pressed()[0]:
                    highscores = False
                    menu = True
            rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(400, y, 40, 30))
            sm.draw(rect, 40, 30)
            sm.draw_img('./images/arrow.png', 400-5, y-5, 48, 48)
            pos = pygame.mouse.get_pos()
            if pos[1] > y and pos[1] < y + 30 and pos[0] > 400 and pos[0] < 440:
                if pygame.mouse.get_pressed()[0]:
                    sort_scores = 0
            rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(550, y, 40, 30))
            sm.draw(rect, 40, 30)
            sm.draw_img('./images/arrow.png', 550-5, y-5, 48, 48)
            if pos[1] > y and pos[1] < y + 30 and pos[0] > 550 and pos[0] < 590:
                if pygame.mouse.get_pressed()[0]:
                    #print "sort scores 1"
                    sort_scores = 1
            y=y+40
            #print sort_scores
            f = open('./highscores.txt')
            string = str(f.read())
            items = string.split('\n')
            item_dict = {}
            for item in items:
                if item:
                    item2 = item.split(':')
                    if item2[0] in item_dict.keys():
                        if item2[1] > item_dict[item2[0]][1]:
                            item_dict[item2[0]] = [item2[1], item2[2]]
                    else:
                        item_dict[item2[0]] = [item2[1], item2[2]]
            #print item_dict
            for key, value in sorted(item_dict.items(), key=lambda (k, v): int(v[sort_scores]), reverse=not sort_scores):
                #item2 = item_dict[item]
                rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(200, y, 440, 30))
                sm.draw(rect, 400, 30)
                text = font.render(str(key), 1, (220,230,243))
                sm.draw(text, 200, y)
                text = font.render('S:'+str(value[0]), 1, (220,230,243))
                sm.draw(text, 400, y)
                text = font.render('M:'+str(value[1]), 1, (220,230,243))
                sm.draw(text, 550, y)
                y = y + 40
            sm.update() #Update screen
        while playing: #Main game loop
            sm.clear() #Clear the screen
            sm.draw_img('./images/bg.png', 0, 0, 640, 92)
            wm.draw_map(sm) #Draw the world
            rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(10, 50, font.size(str(name))[0]+8, 30))
            sm.draw(rect, 10, 50)
            text = font.render(str(name), 1, (220,220,220))
            sm.draw(text, 15, 48)
            tile = None
            keys = pygame.key.get_pressed() #Get keyboard key events                    #If player dies reset all ball values
            delta = clock.get_time()
            if enemy_ticker > 300:
                enemy_ticker = 0
                r=0
                ran = random.randint(1,100)
                if ran < 30 and not r:
                    r = 6
                if ran < 50 and not r:
                    r = 5
                if ran < 70 and not r:
                    r = 4
                if ran < 85 and not r:
                    r = 3
                if ran < 94 and not r:
                    r = 2
                if ran <= 100 and not r:
                    r = 1
                pos1 = (r*3)-2
                pos2 = 0
                direction = 0
                if random.randint(0,1):
                    pos2 = 32
                    direction = 1
                enemies.append(Enemy([pos2, pos1], direction))
            else:
                enemy_ticker = enemy_ticker + 1
            if enemy_ticker%10 == 0:
                i=0
                for enemy in enemies:
                    test = enemy.update(path)
                    if test == 1:
                        path = [path[0]]
                        path_imgs = [3]
                        last_move = [3]
                    elif test == 2:
                        del enemy
                        enemies.pop(i)
                    elif enemy.offScreen():
                        enemies.pop(i)
                    i=i+1
            if keys[pygame.K_ESCAPE]:
                f = open('./highscores.txt', 'a')
                f.write(name+':'+str(score)+':'+str(travel_distance)+'\n')
                f.close()
                menu=True
                playing=False
            if keys[pygame.K_LEFT] and ticker > 10: #If left is pressed do:
                idle_ticker = 0 #Reset Idle ticker
                tile = [path[-1][0]-1, path[-1][1]]
                ticker = 0
                if tile in path:
                    tile = None
                if wm.get_tile(path[-1][0]-1, path[-1][1]) == '0':
                    tile = None
                if tile:
                    if last_move[-1] == 1:
                        path_imgs.append(2)
                    if last_move[-1] == 3:
                        path_imgs.append(5)
                    travel_distance = travel_distance + 1
                    last_move.append(1)
            elif keys[K_RIGHT] and ticker > 10: #If right is pressed do:
                ticker = 0
                idle_ticker = 0 #Reset Idle ticker
                tile = [path[-1][0]+1, path[-1][1]]
                if tile in path:
                    tile = None
                if wm.get_tile(path[-1][0]+1, path[-1][1]) == '0':
                    tile = None
                if tile:
                    if last_move[-1] == 2:
                        path_imgs.append(2)
                    if last_move[-1] == 3:
                        path_imgs.append(4)
                    travel_distance = travel_distance + 1
                    last_move.append(2)
            elif keys[K_SPACE]: #If up is pressed do:
                idle_ticker = 0 #Reset Idle ticker
                if len(path) > 1:
                    path.pop(-1)
                    path_imgs.pop(-1)
                    last_move.pop(-1)
            elif keys[K_DOWN] and ticker > 10: #If down is pressed do:
                ticker = 0
                idle_ticker = 0 #Reset Idle ticker
                tile = [path[-1][0], path[-1][1]+1]
                if tile in path:
                    tile = None
                #print wm.get_tile(13,0)
                #print wm.get_tile(13,1)
                #print wm.get_tile(13,2)
                if wm.get_tile(path[-1][0], path[-1][1]+1) == '0':
                    tile = None
                if tile:
                    if last_move[-1] == 1:
                        path_imgs.append(6)
                    if last_move[-1] == 2:
                        path_imgs.append(7)
                    if last_move[-1] == 3:
                        path_imgs.append(3)
                    travel_distance = travel_distance + 1
                    last_move.append(3)
            if tile:
                path.append(tile)
                #print path
            if wm.get_tile(path[-1][0], path[-1][1]) == '1':
                wm.set_tile(path[-1][0], path[-1][1], '2')
                score=score+1
            i=0
            #print last_move
            for tile in path:
                if i > 0:
                    img = pygame.image.frombuffer(imgs[str(path_imgs[i])], [22, 22], "RGBA")
                    sm.draw(img, path[i-1][0]*22+12, path[i-1][1]*22+92)
                i=i+1
            if last_move[-1] == 1:
                sm.draw_img('./images/8.png', path[-1][0]*22+12, path[-1][1]*22+92, 22, 22)
            if last_move[-1] == 2:
                sm.draw_img('./images/9.png', path[-1][0]*22+12, path[-1][1]*22+92, 22, 22)
            if last_move[-1] == 3:
                sm.draw_img('./images/10.png', path[-1][0]*22+12, path[-1][1]*22+92, 22, 22)

            #ticker = 0 #Reset ticker
            event=pygame.event.poll() #Poll events and store in event
            if event.type==QUIT: #If the window is closed
                pygame.display.quit()
                pygame.quit()
                end = True
                playing = False
                break
            pygame.event.pump() #Process event queue
            ticker = ticker + 1 #Increase ticker
            #idle_ticker = idle_ticker + 1 #Increase idle ticker
            text = font.render(str(score)+"/"+str(wm.getMaxScore()), 1, (220,230,243))
            sm.draw(text, 320-font.size(str(score)+"/"+str(wm.getMaxScore()))[0]/2, 20)
            rect = pygame.draw.rect(sm.get_surf(), (255,255,255, 100),(500-font.size(str(travel_distance)+"/"+str(166))[0]/2, 20, font.size(str(travel_distance)+"/"+str(166))[0]+8, 30))
            sm.draw(rect, 500-font.size(str(travel_distance)+"/"+str(166))[0]/2, 20)
            text = font.render(str(travel_distance)+"/"+str(166), 1, (250,200,50))
            sm.draw(text, 504-font.size(str(travel_distance)+"/"+str(166))[0]/2, 20)
            i=0
            for enemy in enemies:
                enemy.draw(sm)
            sm.update() #Update screen
            clock.tick(60) #Set clock speed to 60 fps
            #print travel_distance
           #print ticker
        #pygame.display.quit() #Quit the program
