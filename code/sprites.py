from setting import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self , pos, surf, groups, z = WORLD_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.z = z
        self.y_sort = self.rect.centery
        self.hitbox = self.rect.copy()

class BorderSprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()

class CollideSprites(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.inflate(-5, -self.rect.height * 0.6)

class MonsterPatchSprite(Sprite):
    def __init__(self, pos, surf, groups, biome):
        self.biome = biome
        super().__init__(pos, surf, groups, WORLD_LAYERS['main'] if biome != 'sand' else WORLD_LAYERS['bg'])
        self.y_sort -= 50

class AnimatedSprites(Sprite):
    def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
        self.frames , self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
    
    def update(self, dt):
        self.animate(dt)