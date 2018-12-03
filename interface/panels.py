import pyglet
from .colors import Color
from . import processes

class InformationPanel():

    types  = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fight', 'fire',
                'flying', 'ghost', 'grass', 'ground', 'ice', 'normal', 'poison',
                'psychic', 'rock', 'steel', 'water']

    def __init__(self, data,):
        self.data = data
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
        self.label_abilities = pyglet.text.Label("Abilities: {}".format(', '.join(self.data.abilities)), font_name="Power Clear", x=30, y=420, font_size=12, batch=self.front)
        self.label_weight = pyglet.text.Label("WT: {} kg".format(self.data.weight), font_name="Power Clear", x=30, y=400, font_size=12, batch=self.front)
        self.label_height = pyglet.text.Label("HT: {} m".format(self.data.height), font_name="Power Clear", x=30, y=380, font_size=12, batch=self.front)

        self.width = self.background_1_image.width
        self.height = self.background_1_image.height

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
           pass
        self.pokemon_image.anchor_x = self.pokemon_image.width
        self.pokemon_sprite.image = self.pokemon_image

    def update_labels(self):
        self.label_name.text = "Name: {}".format(self.data.name)
        self.label_abilities.text = "Abilities: {}".format(' '.join(self.data.abilities))
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
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (self.background_1_sprite.width, self.background_1_sprite.y,
                                                   self.background_1_sprite.width, self.background_1_sprite.height,
                                                   640,             self.background_1_sprite.height,
                                                   640,             self.background_1_sprite.y)),
                                          ('c3B', Color.WHITE*4))

class Browser():

    def __init__(self, database, favorites, x, y):
        self.database = database
        self.favorites = favorites
        self.front = pyglet.graphics.Batch()
        self.back = pyglet.graphics.Batch()

        # Preload image tiles
        self.select_active_image = pyglet.image.load('resources/tiles/select_active.png')
        self.select_active_image.anchor_x = self.select_active_image.width//2
        self.select_active_image.anchor_y = self.select_active_image.height//2
        self.select_inactive_image = pyglet.image.load('resources/tiles/select_inactive.png')
        self.select_inactive_image.anchor_x = self.select_inactive_image.width//2
        self.select_inactive_image.anchor_y = self.select_inactive_image.height//2
        self.star_active_image = pyglet.image.load('resources/tiles/fav_active.png')
        self.star_active_image.anchor_x = self.star_active_image.width//2
        self.star_active_image.anchor_y = self.star_active_image.height//2
        self.star_inactive_image = pyglet.image.load('resources/tiles/fav_inactive.png')
        self.star_inactive_image.anchor_x = self.star_inactive_image.width//2
        self.star_inactive_image.anchor_y = self.star_inactive_image.height//2

        # Set states
        if len(database) >= 10:
            self.cycle_max = 10
        else:
            self.cycle_max = len(database)
        self.index = 0
        self.top = self.index
        self.selected = self.index
        self.bottom = self.index + self.cycle_max - 1
        self.offset = 40
        self.tiles = []
        self.tile_pos = (x + 2.5*self.offset, y, self.offset)
        self.texts    = []
        self.text_pos = (x + 30, y, self.offset)
        self.stars    = []
        self.star_pos = (x, y, self.offset)

        for i in range(self.cycle_max):
            self.tiles.append(pyglet.sprite.Sprite(self.select_inactive_image, batch=self.back, x=self.tile_pos[0], y=self.tile_pos[1]-self.tile_pos[2]*i))
            self.stars.append(pyglet.sprite.Sprite(self.star_inactive_image, batch=self.back, x=self.star_pos[0], y=self.star_pos[1]-self.star_pos[2]*i))
            self.stars[i].scale = self.tiles[i].height/self.stars[i].height
            if self.bottom < self.cycle_max-1:
                target_fav = i
            else:
                target_fav = self.top + i
            if self.database[target_fav].index in self.favorites:
                self.stars[i].color = Color.GREY
            else:
                self.stars[i].color = Color.WHITE
            self.texts.append(pyglet.text.Label('{} - {}'.format(processes.add0(self.database[i].index), self.database[i].name)
                            , batch=self.front, x=self.text_pos[0], font_size=15,
                              y=self.text_pos[1] - self.text_pos[2]*i, anchor_y='center', font_name='Power Clear',
                              color=Color.BLACK + tuple([255]) ) )

        #setting the first items as the "selector"
        self.tiles[0].image = self.select_active_image
        self.texts[0].color = Color.WHITE + tuple([255])

    def update_data(self, shift):
        if shift >= self.cycle_max or shift <= -self.cycle_max:
            # Shift entire list and selector
            self.top += shift
            self.index += shift
            self.bottom += shift
        elif self.index != self.bottom and shift > 0:
            self.index += shift
            self.selected += shift
        elif self.index != self.top and shift < 0:
            self.index += shift
            self.selected += shift
        elif self.index == self.top and shift < 0:
            self.top += shift
            self.index += shift
            self.bottom += shift
        elif self.index == self.bottom and shift > 0:
            self.top += shift
            self.index += shift
            self.bottom += shift

        if self.top < 0:
            self.top = len(self.database) + self.top
        if self.top > len(self.database) - 1:
            self.top = self.top - len(self.database)
        if self.bottom > len(self.database) - 1:
            self.bottom = self.bottom - len(self.database)
        if self.bottom < 0:
            self.bottom = len(self.database) + self.bottom
        if self.selected < 0:
            self.selected = 0
        if self.selected > self.cycle_max - 1:
            self.selected = self.cycle_max - 1
        if self.index > len(self.database) - 1:
            self.index = self.index - len(self.database)
        if self.index < 0:
            self.index = len(self.database) + self.index
 
        target_database = []
        if self.bottom < self.top:
            target_database = target_database + self.database[self.top:]
            target_database = target_database + self.database[0:self.bottom+1]
        elif self.top > self.bottom and self.bottom < self.cycle_max:
            target_database = target_database + self.database[self.bottom:]
            target_database = target_database + self.database[:self.top]
        else: 
            target_database = target_database + self.database[self.top:self.bottom+1]
        for i in range(len(target_database)):
            self.texts[i].text = "{} - {}".format(processes.add0(target_database[i].index), target_database[i].name)
            target_fav = self.top + i
            if target_fav > len(self.database) - 1:
                target_fav = target_fav - len(self.database)
            if self.database[target_fav].index in self.favorites:
                self.stars[i].color = Color.GREY
            else:
                self.stars[i].color = Color.WHITE
            if i == self.selected:
                self.tiles[i].image = self.select_active_image
                self.texts[i].color = Color.WHITE + tuple([255])
            else:
                self.tiles[i].image = self.select_inactive_image
                self.texts[i].color = Color.BLACK + tuple([255])
            self.tiles[i].visible = True
            self.stars[i].visible = True
        
        return self.index

    def clear_browser(self):
        for text in self.texts:
            text.text = ""
        for sprite in self.tiles:
            sprite.visible = False
        for star in self.stars:
            star.visible = False

    def update_favs(self):
        if self.index in self.favorites:
            self.favorites.remove(self.index)
            self.stars[self.selected].color = Color.WHITE
        else:
            self.favorites.append(self.index)
            self.stars[self.selected].color = Color.GREY
            
    def update_database(self, database):
        self.database = database

        if len(database) >= 10:
            self.cycle_max = 10
        else:
            self.cycle_max = len(self.database)
        self.index = 0
        self.top = self.index
        self.selected = self.index
        self.bottom = self.index + self.cycle_max - 1
        self.clear_browser()
        self.update_data(0)    

    def draw_self(self):
        self.back.draw()
        self.front.draw()

class SearchPanel():

    def __init__(self, database, x, y):
        self.front = pyglet.graphics.Batch()
        self.back = pyglet.graphics.Batch()
        self.database = database
        self.search_string = ""
        self.label = pyglet.text.Label(text="Search...", font_name="Power Clear", font_size=14, x=380, y=440, batch=self.front, color=Color.BLACK+tuple([255]), anchor_x="left", anchor_y="center")

    def draw_self(self):
        self.back.draw()
        self.front.draw()

    def handle_backspace(self):
        self.search_string = self.search_string[:-1]
        self.label.text = self.search_string

    def handle_char(self, key):
        self.search_string += key.lower()
        self.search_string = self.search_string.capitalize()
        self.label.text = self.search_string

    def handle_enter(self):
        types  = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fight', 'fire',
                       'flying', 'ghost', 'grass', 'ground', 'ice', 'normal', 'poison',
                       'psychic', 'rock', 'steel', 'water']

        if self.search_string == "":
            return self.database
        elif self.search_string.lower() == "legendary":
            self.query = self.database.filter_by_legendary(True)
        elif self.search_string.lower() == "common":
            self.query = self.database.filter_by_legendary(False)
        elif self.search_string.lower() in types:
            self.query = self.database.filter_by_type(self.search_string.lower())
        else:
            self.query = self.database.filter_by_name(self.search_string)
        if self.query != None and not self.query.isempty():
            return self.query
        else:
            self.label.text = "No results..."
            return self.database
        