import pyglet
import math
from .colors import Color

class InformationPanel():

    types  = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fight', 'fire',
                'flying', 'ghost', 'grass', 'ground', 'ice', 'normal', 'poison',
                'psychic', 'rock', 'steel', 'water']

    def __init__(self, data, width=640, height=480):
        self.data = data
        self.width = width
        self.height = height
        self.front = pyglet.graphics.Batch()
        self.back = pyglet.graphics.Batch()
        self.initialize_components()

    def initialize_components(self):
        # Load pokemon data to display
        self.index = self.data.index
        self.name = self.data.name
        self.type_1 = self.data.type1
        self.type_2 = self.data.type2

        # Load type 1 and 2 background images and sprites
        self.background_1_image = pyglet.image.load('resources/backgrounds/{}.png'.format(self.type_1))
        self.background_1_sprite = pyglet.sprite.Sprite(self.background_1_image, batch=self.back)
        if not math.isnan(self.type_2):        
            self.background_2_image = pyglet.image.load('resources/backgrounds/{}.png'.format(self.type_2))
            self.background_2_sprite = pyglet.sprite.Sprite(self.background_2_image, batch=self.back)
        
        # Load initial pokemon image and sprite
        try:
            self.pokemon_image = pyglet.image.load('resources/pokemon/{}.jpg'.format(self.name.lower()))
        except(FileNotFoundError):
            pass
        try:
            self.pokemon_image = pyglet.image.load('resources/pokemon/{}.png'.format(self.name.lower()))
        except(FileNotFoundError):
            raise FileNotFoundError("Invalid pokemon name.")
        self.pokemon_sprite = pyglet.sprite.Sprite(self.pokemon_image, self.background_1_sprite.width, self.background_1_sprite.height, batch=self.front)

    def update_pokemon_sprite(self, name):
        try:
            self.pokemon_image = pyglet.image.load('resources/pokemon/{}.jpg'.format(name.lower()))
        except(FileNotFoundError):
            pass
        try:
            self.pokemon_image = pyglet.image.load('resources/pokemon/{}.png'.format(name.lower()))
        except(FileNotFoundError):
            raise FileNotFoundError("Invalid pokemon name.")
        self.pokemon = pyglet.sprite.Sprite(self.pokemon_image, self.background1.width, self.background2.height, batch=self.front)

    def update(self, data):
        self.data = data
        self.index = data.index
        self.name = data.name
        self.type_1 = data.type1
        self.type_2 = data.type2

        self.bg_image_1  = pyglet.image.load('resources/backgrounds/steel.png')
        self.bg_sprite_1 = pyglet.sprite.Sprite(self.bg_image_1, batch=self.front)

    def draw_self(self):
        self.back.draw()
        self.front.draw()