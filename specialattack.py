import pygame
import random
import settings as s

class SpecialLine:
    def __init__(self, speed = 15, width = 3):
        self.start_x = 0
        self.y = s.SCREEN_HEIGHT
        self.speed = speed
        self.width = width
        self.length = s.SCREEN_HEIGHT
        self.active = False
        self.trail = []
        self.sound_rate = 80
        self.last_sound_time = 0

    def activate(self):
        self.start_x = 0
        self.trail = []
        self.active = True

    def update(self):
        self.start_x += self.speed
        
        self.trail.append(self.start_x)

        if len(self.trail) > 10:
            self.trail.pop(0)

        if self.start_x > s.SCREEN_WIDTH + 100:
            self.active = False

    def get_line(self):
        if len(self.trail) == 0:
            return ((0, 0), (0, s.SCREEN_HEIGHT))
        else:
            return ((self.trail[-1], 0), (self.trail[-1], s.SCREEN_HEIGHT))

    def draw(self, screen):
        sound = pygame.mixer.Sound("asset/sound/laser.wav")
        sound.set_volume(0.7)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_sound_time > self.sound_rate and self.active:
            sound.play()
            self.last_sound_time = current_time
        for i, (start) in enumerate(self.trail):
            alpha = int(255 * (i + 1) / len(self.trail))
            color = (alpha, alpha, alpha)
            pygame.draw.line(screen, color, (start, 0), (start, self.y), self.width)