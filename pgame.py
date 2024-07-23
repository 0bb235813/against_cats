import pygame
from os import listdir
from os.path import isfile, join
import math
import random

pygame.init()

WIDTH = 800
HEIGHT = 450
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


background = [
    pygame.image.load('image/background/1.png'),
    pygame.image.load('image/background/2.png'),
    pygame.image.load('image/background/3.png'),
    pygame.image.load('image/background/4.png'),
    pygame.image.load('image/background/5.png')
 ]

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir, dir2, width, height, direction = False):
    path = join("assets", dir, dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]
    # images = ['hit.png', 'run.png', 'stand.png']

    all_sprts = {}

    for image in images[1:]:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        # if direction:
        all_sprts[image.replace(".png", "") + "_right"] = sprites
        all_sprts[image.replace(".png", "") + "_left"] = flip(sprites)
        # else:
        #     all_sprts[image.replace(".png", "")] = sprites
    print(all_sprts)
    return all_sprts

def get_block(size):
    path = join("assets", "Terrain", "block.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)

class Cat(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheets("MainCharacters", "MaskCat", 32, 32, True)
    ANIMATION_DELAY = 10
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(100, 100, 50, 50)
        self.rect.center = (x, y)
        self.d_x = 0
        self.d_y = 0
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.CAT_VEL = random.choice([1,2,3])
        self.death_count = 0
        self.sprite_sheet = ''
        self.hit_count = 40
        self.hp = 100
        self.die = False
        self.image = self.SPRITES["stand_right"][0]
        self.hit_flag = False
        self.last_attack_time = 0
        self.is_attacking = False
        self.attack_frame_count = 0

    def move(self, dx, dy):
        if self.die:
            self.rect.x += 0
        else:
            self.rect.x += dx
            self.rect.y += dy

    def move_left(self):
        self.d_x = -self.CAT_VEL
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self):
        self.d_x = self.CAT_VEL
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    def dead(self):
        # if not self.die:
        self.animation_count = 0
        self.hit_count = 40
        self.die = True
        self.is_attacking = False
    
    def hit(self):
        if not self.die:
            self.hit_count = 0
        # self.is_attacking = True
        # self.attack_frame_count = 0
        # self.animation_count = 0
        # if self.animation_count < 40:
        #     self.animation_count = 0

    def damage(self):
        if not self.die:
            self.hp -= 50
            if self.hp <= 0:
                self.dead()

    def loop(self, fps):
        # self.d_y = min(1, (self.fall_count / fps) * self.GRAVITY)
        # self.move(self.d_x, self.d_y)
        self.move(self.d_x, self.d_y)
        # self.fall_count += 1
        if self.die:
            self.death_count += 1

        self.update_sprite()

    def update_sprite(self):
        if self.die:
            self.sprite_sheet = "death"
        elif self.hit_count < 40:
            self.sprite_sheet = "hit"
            self.hit_count += 1
            self.d_x = 0
        # elif self.is_attacking:
        #     self.sprite_sheet = "hit"
        #     self.attack_frame_count += 1
        #     if self.attack_frame_count >= len(self.SPRITES[self.sprite_sheet + "_" + self.direction]) * self.ANIMATION_DELAY:
        #         self.is_attacking = False
        #         self.attack_frame_count = 0
        elif self.d_x != 0:
            self.sprite_sheet = "run"
            self.hit_count = 40
        elif self.d_x == 0:
            self.sprite_sheet = "stand"
        
        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        if self.hit_count < 40:
            sprite_index = self.hit_count // self.ANIMATION_DELAY
        else:
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        # if self.is_attacking:
        #     sprite_index = self.attack_frame_count // self.ANIMATION_DELAY
        # else:
        #     sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        # sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.iamge = self.sprite

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskPlayer", 64, 32, True)
    ANIMATION_DELAY = 5
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(400, 200, 10, 10)
        self.d_x = 0
        self.d_y = 5
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.hit_count = 20
        self.hp = 100
        self.die = False
        self.last_attack_time = 0
        
    def move(self, dx, dy):
        if self.die:
            self.rect.x += 0
        else:
            self.rect.x += dx
            self.rect.y += dy

    def move_left(self):
        self.d_x = -PLAYER_VEL
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self):
        self.d_x = PLAYER_VEL
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def jump(self):
        self.d_y = -self.GRAVITY * 8
        self.animation_count = 0
    
    def landed(self):
        self.fall_count = 0
        self.d_y = 0

    def dead(self):
        if not self.die:
            self.animation_count = 0
            self.die = True

    def hit(self):
        self.hit_count = 0
        self.animation_count = 0

    def loop(self, fps):
        self.d_y += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.d_x, self.d_y)

        if self.d_y != 0:
            self.fall_count += 1

        self.update_sprite()
    
    def update_sprite(self):
        sprite_sheet = "stand"
        if self.die:
            sprite_sheet = "dead"
        elif self.d_y < 0:
            sprite_sheet = "up"
            self.hit_count = 20
        elif self.d_y > 0:
            sprite_sheet = "down"
        elif self.hit_count < 20:
            sprite_sheet = "hit"
            self.hit_count += 1          
        elif self.d_x != 0:
            sprite_sheet = "run"
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        cur = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        sprite_index = cur
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))


def handle_vertical_collision(player, objects, dy):
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            player.rect.bottom = obj.rect.top + 8
            player.landed()

def collide(player, cats, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for cat in cats:
        if pygame.sprite.collide_mask(player, cat):
            collided_object = cat
            break
    player.move(-dx, 0)
    player.update()
    return collided_object
    

def handle_move(objects, events):
    keys = pygame.key.get_pressed()
    player.d_x = 0
    # collide_left = collide(player, cats, -PLAYER_VEL)
    # collide_right = collide(player, cats, PLAYER_VEL)

    if keys[pygame.K_a]:
        player.move_left()
    elif keys[pygame.K_d]:
        player.move_right()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                current_time = pygame.time.get_ticks()
                if current_time - player.last_attack_time >= 500:
                    player.hit()
                    player.last_attack_time = pygame.time.get_ticks()
                    for cat in cats:
                        if pygame.sprite.collide_rect(player, cat):
                            if player.direction == "right" and cat.rect.centerx > player.rect.centerx:
                                cat.damage()
                            elif player.direction == "left" and cat.rect.centerx < player.rect.centerx:
                                cat.damage()
                                
    for cat in cats:
        current_time2 = pygame.time.get_ticks()
        # if pygame.sprite.collide_rect(player, cat):
        if math.sqrt((player.rect.centerx - cat.rect.centerx)**2 + (player.rect.centery - cat.rect.centery)**2) <= 50:
            if current_time2 - cat.last_attack_time >= 500:
                cat.hit()
                player.hp -= 5
                cat.last_attack_time = pygame.time.get_ticks()
            if player.hp <= 0:
                cats.empty()
                player.dead()
        else:
            if player.rect.x > cat.rect.x and not cat.die:
                cat.move_right()
            elif player.rect.x < cat.rect.x and not cat.die:
                cat.move_left()
    handle_vertical_collision(player, objects, player.d_y)

def draw(background):
    for tile in background:
        display.blit(tile, (0,0))

    for block in blocks:
        block.draw(display)

    pygame.draw.rect(display, (255,0,0), (50,50, 100, 10))
    pygame.draw.rect(display, (0,255,0), (50,50, player.hp, 10))
    for cat in cats:
        pygame.draw.rect(display, (255,0,0), (cat.rect.centerx - 25, cat.rect.centery - 40, 50, 5))
        pygame.draw.rect(display, (0,255,0), (cat.rect.centerx - 25, cat.rect.centery - 40, cat.hp/2, 5))
        if cat.death_count == 80:
            cats.remove(cat)
        cat.draw(display)
    player.draw(display)

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))
       
class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 36)
    
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(display, self.hover_color, self.rect)
        else:
            pygame.draw.rect(display, self.color, self.rect)
        
        text_surface = self.font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        display.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    display.blit(text_surface, text_rect)

def show_menu():
    start_button = Button("Start Game", 325, 200, 150, 50, (0,255,0), (255,255,255))
    quit_button = Button("Quit Game", 325, 300, 150, 50, (0,255,0), (255,255,255))
    backgr = pygame.image.load("image/background/Overlay.png")

    buttons = [start_button, quit_button]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        
        for button in buttons:
            if button.is_clicked():
                if button.text == "Start Game":
                    running = False
                elif button.text == "Quit Game":
                    pygame.quit()
                    exit()

        display.blit(backgr, (0,0))
        draw_text("Main Menu", 48, (255, 255, 255), 400, 100)

        for button in buttons:
            button.draw()
        
        pygame.display.flip()

def end_game():
    # restart_button = Button("Restart Game", 325, 200, 150, 50, (0,255,0), (255,255,255))
    quit_button = Button("Quit Game", 325, 150, 150, 50, (255,255,0), (255,255,255))

    buttons = [quit_button]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        
        for button in buttons:
            if button.is_clicked():
                if button.text == "Restart Game":
                    running = False
                elif button.text == "Quit Game":
                    pygame.quit()
                    exit()

        # display.fill((0,0,0))
        draw_text("Game Over", 48, (255, 255, 255), 400, 100)

        for button in buttons:
            button.draw()
        
        pygame.display.flip()

player = Player()
cats = pygame.sprite.Group()
game_over = False
FPS = 60
PLAYER_VEL = 5

count = 0
def geniration_cat():
    return Cat(random.choice([-100, 900]), 350)

blocks = [Block(i * 32, 350, 32) for i in range(1200//32)]

# cats.add(Cat(600, 350))
# cats.add(Cat(300, 350))
show_menu()
while not game_over:
    if count >= 100:
        cats.add(geniration_cat())
        count = 0
    count += 1
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            # if event.key == pygame.K_h:
            #     player.hit()
    if player.die and player.animation_count >= 60:
        end_game()
            
    player.loop(FPS)
    for cat in cats:
        cat.loop(FPS)
    handle_move(blocks, events)
    draw(background)
    pygame.display.flip()

pygame.quit()
quit()