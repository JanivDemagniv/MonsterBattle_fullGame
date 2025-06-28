from setting import *
from os.path import join
from pytmx.util_pygame import load_pygame
from sprites import *
from entites import *
from groups import AllSprites
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()

        #groups
        self.all_sprites = AllSprites()

        self.impot_assest()
        self.setup(self.tmx_map['world'], 'house')

    def impot_assest(self):
        self.tmx_map = {'world': load_pygame(join('data','maps','world.tmx')),
                        'arena': load_pygame(join('data','maps','arena.tmx')),
                        'fire': load_pygame(join('data','maps','fire.tmx')),
                        'hospital': load_pygame(join('data','maps','hospital.tmx')),
                        'hospital2': load_pygame(join('data','maps','hospital2.tmx')),
                        'house': load_pygame(join('data','maps','house.tmx')),
                        'plant': load_pygame(join('data','maps','plant.tmx')),
                        'water': load_pygame(join('data','maps','water.tmx')),
                        }

        self.overworld_frames = {
            'water': import_folder(join('graphics','tilesets','water')),
            'coast': coast_importer(24 ,12 ,join('graphics','tilesets','coast')),
            'characters': import_all_character(join('graphics','characters'))
            }
        
    def setup(self, tmx_map, player_start_pos):
        #Terrain
        for layer in ['Terrain', 'Terrain Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        #Water
        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x),int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprites((x,y), self.overworld_frames['water'],self.all_sprites)
        
        #Coast
        for obj in tmx_map.get_layer_by_name('Coast'):
            terrain = obj.properties['terrain']
            side = obj.properties['side']
            AnimatedSprites((obj.x,obj.y),self.overworld_frames['coast'][terrain][side],self.all_sprites)

        #Object
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x,obj.y), obj.image, self.all_sprites)

        #Monsters
        for obj in tmx_map.get_layer_by_name('Monsters'):
            Sprite((obj.x,obj.y), obj.image, self.all_sprites)

        #Entitis
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                self.player = Player(
                    pos = (obj.x,obj.y),
                    frames = self.overworld_frames['characters']['player'],
                    initial_state = obj.properties['direction'],
                    groups = self.all_sprites)
            if obj.name == 'Character':
                graphic = obj.properties['graphic']
                init_state = obj.properties['direction']
                Character(
                    pos = (obj.x,obj.y),
                    frames = self.overworld_frames['characters'][graphic],
                    init_state= init_state,
                    groups = self.all_sprites)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            #game logic
            self.all_sprites.update(dt)
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()