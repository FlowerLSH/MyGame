import pygame
from stage_ui import StageUI
from collections import deque

class UIManager:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.stage_ui = None
        self.ui_active = False
        self.ui_queue = deque()

    def display_stage_ui(self, text, duration = 2000):
        self.ui_queue.append((text, duration))
        if not self.ui_active:
            self.display_next_ui()

    def display_next_ui(self):
        if self.ui_queue:
            text, duration = self.ui_queue.popleft()
            self.stage_ui = StageUI(self.screen, text, self.font, duration=duration)
            self.ui_active = True

    def update(self):
        if self.ui_active and self.stage_ui:
            self.screen.fill((0, 0, 0))
            self.stage_ui.update()
            if self.stage_ui.is_finished():
                self.ui_active = False
                self.stage_ui = None
                self.display_next_ui()
            pygame.display.flip()
            pygame.time.delay(10)
            return True
        return False