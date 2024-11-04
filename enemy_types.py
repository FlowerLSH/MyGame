from enemy import Enemy

class SmallEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp = 50, speed = 3, size_x = 20, size_y = 20, fire_rate = 1000)

class MediumEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp = 100, speed = 2, size_x = 30, size_y = 30, fire_rate = 1500)
        
class LargeEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, hp = 200, speed = 1, size_x = 40, size_y = 40, fire_rate = 2000)