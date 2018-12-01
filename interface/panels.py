import pyglet
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

        # Load initial type 1 and 2 background images and sprites
        self.background_1_image = pyglet.image.load('resources/backgrounds/{}.png'.format(self.type_1))
        self.background_1_sprite = pyglet.sprite.Sprite(self.background_1_image, batch=self.back)
        
        # Check if type_2 is a string or a NaN float
        # Made as an artifact of using pandas for data loading
        if isinstance(self.type_2, str):        
            self.background_2_image = pyglet.image.load('resources/backgrounds/{}.png'.format(self.type_2))
            self.background_2_sprite = pyglet.sprite.Sprite(self.background_2_image, batch=self.back)
            self.background_2_sprite.opacity = 150

        # Load initial pokemon image and sprite
        # Attempt to load jpg version if it exists
        # else, load png version
        try:
            self.pokemon_image = pyglet.image.load('resources/pokemon/{}.jpg'.format(self.name.lower()))
        except(FileNotFoundError):
            pass
        try:
            self.pokemon_image = pyglet.image.load('resources/pokemon/{}.png'.format(self.name.lower()))
        except(FileNotFoundError):
            raise FileNotFoundError("Invalid pokemon name.")
        self.pokemon_image.anchor_x = self.pokemon_image.width
        self.pokemon_sprite = pyglet.sprite.Sprite(self.pokemon_image, self.background_1_sprite.width, self.background_1_sprite.width, batch=self.front)

        # Load labels
        self.label_name = pyglet.text.Label("Name: {}".format(self.data.name), font_name="Power Clear", x=30, y=440, font_size=15, batch=self.front)
        self.label_abilities = pyglet.text.Label("Abilities: {}".format(self.data.abilities), font_name="Power Clear", x=30, y=420, font_size=12, batch=self.front)
        self.label_weight = pyglet.text.Label("WT: {} kg".format(self.data.weight), font_name="Power Clear", x=30, y=400, font_size=12, batch=self.front)
        self.label_height = pyglet.text.Label("HT: {} m".format(self.data.height), font_name="Power Clear", x=30, y=380, font_size=12, batch=self.front)

    def update_background_sprite(self):

        # Replace type_1 sprite background image
        self.background_1_sprite.image = pyglet.image.load('resources/backgrounds/{}.png'.format(self.type_1))
     
        # Check if type_2 is a string or a NaN float
        # Made as an artifact of using pandas for data loading
        if isinstance(self.type_2, str):        
            self.background_2_sprite.image = pyglet.image.load('resources/backgrounds/{}.png'.format(self.type_2))

    def update_pokemon_sprite(self):
        try:
            self.pokemon_image = pyglet.image.load('resources/pokemon/{}.jpg'.format(self.data.name.lower()))
        except(FileNotFoundError):
            pass
        try:
            self.pokemon_image = pyglet.image.load('resources/pokemon/{}.png'.format(self.data.name.lower()))
        except(FileNotFoundError):
            raise FileNotFoundError("Invalid pokemon name.")
        self.pokemon_image.anchor_x = self.pokemon_image.width
        self.pokemon_sprite.image = self.pokemon_image

    def update_labels(self):
        self.label_name.text = "Name: {}".format(self.data.name)
        self.label_abilities.text = "Abilities: {}".format(self.data.abilities)
        self.label_weight.text = "WT: {} kg".format(self.data.weight)
        self.label_height.text = "HT: {} m".format(self.data.height)

    def update(self, data):
        self.data = data
        self.index = data.index
        self.name = data.name
        self.type_1 = data.type1
        self.type_2 = data.type2

        self.update_background_sprite()
        self.update_pokemon_sprite()
        self.update_labels()

    def draw_self(self):
        self.back.draw()
        self.front.draw()