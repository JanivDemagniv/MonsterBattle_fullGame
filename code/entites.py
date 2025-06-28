from setting import *

class Entitie(pygame.sprite.Sprite):
    def __init__(self, pos, frames, initial_state, groups):
        super().__init__(groups)
        self.z = WORLD_LAYERS['main']
        self.frames , self.frame_index = frames , 0

        #sprite setup
        self.image = self.frames[initial_state][self.frame_index]
        self.rect = self.image.get_frect(center = pos)

        #movement
        self.direction = vector(100,100)
        self.speed = 250
        self.facing_direction = 'down'

        self.y_sort = self.rect.centery

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

    def get_state(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x != 0:
                self.facing_direction = 'right' if self.direction.x > 0 else 'left'
            elif self.direction.y != 0:
                self.facing_direction = 'down' if self.direction.y > 0 else 'up'
        return f'{self.facing_direction}{'' if moving else '_idle'}'
    
    


class Player(Entitie):
    def __init__(self, pos,frames, initial_state , groups):
        super().__init__(pos, frames, initial_state, groups)

    def input(self):
        keys = pygame.key.get_pressed()

        input_vector = vector()

        if keys[pygame.K_UP]:
            input_vector.x = 0
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.x = 0
            input_vector.y += 1
        if keys[pygame.K_RIGHT]:
            input_vector.y = 0
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.y = 0
            input_vector.x -= 1
        
        self.direction = input_vector

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.y_sort = self.rect.centery
        self.input()
        self.move(dt)
        self.animate(dt)


class Character(Entitie):
    def __init__(self, pos, frames, init_state , groups):
        super().__init__(pos, frames, init_state, groups)