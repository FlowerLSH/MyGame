# stage_ui.py

import pygame

class StageUI:
    def __init__(self, screen, text, font, duration=2000):
        self.screen = screen
        self.text = text
        self.font = font
        self.duration = duration
        self.alpha = 0
        self.fade_out = True
        self.start_time = pygame.time.get_ticks()
        self.finished = False

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if self.fade_out:
            self.alpha = min(255, (elapsed_time / 500) * 255)
            if elapsed_time >= 500: 
                self.fade_out = False
                self.start_time = current_time
        
        elif not self.fade_out and elapsed_time < self.duration:
            self.alpha = 255

        
        elif elapsed_time >= self.duration:
            self.alpha = max(0, 255 - ((elapsed_time - self.duration) / 500) * 255)
            if self.alpha == 0:
                self.finished = True  

        
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_surface.set_alpha(int(self.alpha))
        text_rect = text_surface.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text_surface, text_rect)

    def is_finished(self):
        return self.finished
