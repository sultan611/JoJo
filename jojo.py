import pygame
import sys
import math
import random

pygame.init()


width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("🎂 Birthday Celebration 🎉")
clock = pygame.time.Clock()


WHITE = (255, 255, 255)
BRIGHT_WHITE = (255, 255, 255)
GOLD = (255, 223, 100)
PINK = (255, 182, 193)
RED = (255, 80, 80)
DARK_RED = (180, 30, 30)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)
DARK_GREEN = (0,100,0)
BALLOON_COLORS = [(255, 100, 100), (100, 200, 255), (255, 200, 100), (200, 100, 255)]

font = pygame.font.SysFont("comicsansms", 60, bold=True)
small_font = pygame.font.SysFont("comicsansms", 30, bold=True)

def draw_text(text, font, color, x, y, shadow=True):
    if shadow:
        shadow_surface = font.render(text, True, BLACK)
        screen.blit(shadow_surface, (x+3, y+3))
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_cake():
    pygame.draw.rect(screen, PINK, (300, 350, 300, 150), border_radius=20)
    pygame.draw.rect(screen, RED, (300, 350, 300, 20), border_radius=10)
    
    start_x = 320
    end_x = 580
    center_y = 425
    num_pearls = 15
    spacing = (end_x - start_x) / (num_pearls - 1)
    for i in range(num_pearls):
        x = start_x + i * spacing
        pygame.draw.circle(screen, BRIGHT_WHITE, (int(x), center_y), 8)


class Candle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flame_offset = random.uniform(0, 2*math.pi)
    def draw(self, frame):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 15, 40))
        flame_x = self.x + 7 + math.sin(frame*0.08 + self.flame_offset)*1.5
        flame_y = self.y - 5 + math.sin(frame*0.12 + self.flame_offset)*1.5
        pygame.draw.circle(screen, (255, 220, 100), (int(flame_x), int(flame_y)), 10)
        pygame.draw.circle(screen, (255, 160, 50), (int(flame_x), int(flame_y)), 6)
        pygame.draw.circle(screen, (255, 100, 0), (int(flame_x), int(flame_y)), 3)


class Rose:
    def __init__(self, x, y, size=40, angle_shift=0):
        self.x = x
        self.y = y
        self.size = size
        self.angle = random.uniform(0, 2*math.pi)
        self.speed = random.uniform(0.0015, 0.003)
        self.angle_shift = angle_shift
    def draw(self, frame):
        offset = math.sin(frame*self.speed + self.angle) * 2
        center_x = self.x
        center_y = self.y + offset
        pygame.draw.rect(screen, DARK_GREEN, (center_x-2, center_y, 4, self.size//2))
        top_y = center_y - self.size//2
        for i in range(6):
            angle = i * 2*math.pi/6 + self.angle_shift
            dx = int(self.size/3 * math.cos(angle))
            dy = int(self.size/3 * math.sin(angle))
            pygame.draw.circle(screen, DARK_RED, (center_x+dx, top_y+dy), int(self.size/6))


def draw_decorations(frame):
    for i in range(0, width, 60):
        r = (200 + 55 * math.sin(frame*0.1 + i)) % 255
        g = (100 + 155 * math.sin(frame*0.15 + i*0.5)) % 255
        b = (200 + 55 * math.cos(frame*0.12 + i)) % 255
        pygame.draw.circle(screen, (int(r), int(g), int(b)), (i, 80), 15)

def draw_ribbons(frame):
    RIBBON_COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]
    for i, color in enumerate(RIBBON_COLORS):
        x = 100 + i*120
        y_top = 0
        y_bottom = 150 + math.sin(frame*0.05 + i) * 20
        pygame.draw.line(screen, color, (x, y_top), (x, y_bottom), 4)


def glowing_text(text, y_pos, frame):
    glow = int(128 + 127 * math.sin(frame * 0.1))
    color = (glow, 100 + glow//2, 255 - glow//2)
    draw_text(text, font, color, width//2 - font.size(text)[0]//2, y_pos)


candles = [Candle(340 + i*60, 320) for i in range(5)]


roses = [Rose(230, 380, 50, angle_shift=-0.2),
         Rose(260, 370, 50, angle_shift=0.2),
         Rose(640, 370, 50, angle_shift=-0.2),
         Rose(670, 380, 50, angle_shift=0.2)]


class Balloon:
    def __init__(self):
        self.x = random.randint(100, 800)
        self.y = height + random.randint(20, 200)
        self.color = random.choice(BALLOON_COLORS)
        self.speed = random.uniform(0.7, 1.3)
        self.size = random.randint(25, 35)
    def update(self):
        self.y -= self.speed
        if self.y < -50:
            self.y = height + random.randint(20, 200)
            self.x = random.randint(100, 800)
            self.color = random.choice(BALLOON_COLORS)
            self.speed = random.uniform(0.7, 1.3)
            self.size = random.randint(25, 35)
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.x, int(self.y), self.size, self.size*1.3))
        pygame.draw.line(screen, WHITE, (self.x + self.size//2, self.y + self.size*1.3),
                         (self.x + self.size//2, self.y + self.size*1.3 + 15), 2)

balloons = [Balloon() for _ in range(12)]

frame = 0
running = True
while running:
    screen.fill((20,20,40))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_decorations(frame)
    draw_ribbons(frame)  
    glowing_text("Happy Birthday", 150, frame)
    draw_text("Jumanah 31/December", small_font, GOLD, width//2 - 160, 230)
    draw_cake()
    for candle in candles:
        candle.draw(frame)
    for rose in roses:
        rose.draw(frame)
    for balloon in balloons:
        balloon.update()
        balloon.draw(screen)

    pygame.display.flip()
    frame += 1
    clock.tick(60)

pygame.quit()
sys.exit()
