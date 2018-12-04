"""
Database engine for python-pokedex

:Author:    Jose Enrico Salinas
:Version:   20181204
"""

import csv
import pandas as pd

class DatabaseQuery():
    """
    A database query for python-pokedex
    Uses pandas library to filter and sort data
    """

    def __init__(self, dataframe):
        """
        Creates a new dictionary query from a pandas dataframe

        Args:
            dataframe (pandas.DataFrame): a pandas dataframe containing pokemon information
        """

        self.query = []
        self.dataframe = dataframe
        for index, row in dataframe.iterrows():
            data = []
            for col in row:
                data.append(col)
            self.query.append(DataRow(data))

    def __getitem__(self, key):
        return self.query[key]

    def __setitem__(self, key, value):
        self.query[key] = value

    def __iter__(self):
        return iter(self.query)

    def __len__(self):
        return len(self.query)

    def filter_by_name(self, name):
        """
        Finds a pokemon with specified name

        Args:
            name(str): The name of the pokemon
        Returns:
            DatabaseQuery: contains the pokemon row if it exists
        """
        data_query = self.dataframe.loc[self.dataframe.name == name]
        return DatabaseQuery(data_query)

    def filter_by_type(self, pokemon_type):
        """
        Finds all pokemon with specified type

        Args:
            pokemon_type(str): The lowercase type query
        Returns:
            DatabaseQuery: contains all pokemon with specified type if they exist
        """
        data_query = self.dataframe.loc[(self.dataframe.type1 == pokemon_type.lower()) | (self.dataframe.type2 == pokemon_type.lower())]
        return DatabaseQuery(data_query)

    def filter_by_legendary(self, value):
        """
        Finds all pokemon by either legendary or common

        Args:
            value(bool): Get legendary pokemon if true, else get common pokemon
        Returns:
            DatabaseQuery: contains all pokemon that are either legendary or common 
        """
        if value == True:
            query = 1
        else:
            query = 0
        data_query = self.dataframe.loc[(self.dataframe.is_legendary == query)]
        return DatabaseQuery(data_query)

    def sort_by_hp(self):
        """
        Sorts all pokemon by hp in descending order

        Returns:
            DatabaseQuery: contains all pokemon sorted by hp in descending order
        """
        data_query = self.dataframe.sort_values(by=["hp"], ascending=False)
        return data_query

    def sort_by_attack(self):
        """
        Sorts all pokemon by attack in descending order

        Returns:
            DatabaseQuery: contains all pokemon sorted by attack in descending order
        """
        data_query = self.dataframe.sort_values(by=["attack"], ascending=False)
        return data_query

    def sort_by_defense(self):
        """
        Sorts all pokemon by defense in descending order

        Returns:
            DatabaseQuery: contains all pokemon sorted by defense in descending order
        """
        data_query = self.dataframe.sort_values(by=["defense"], ascending=False)
        return data_query

    def sort_by_speed(self):
        """
        Sorts all pokemon by speed in descending order

        Returns:
            DatabaseQuery: contains all pokemon sorted by speed in descending order
        """
        data_query = self.dataframe.sort_values(by=["speed"], ascending=False)
        return data_query
    
    def sort_by_sp_defense(self):
        """
        Sorts all pokemon by special defense in descending order

        Returns:
            DatabaseQuery: contains all pokemon sorted by special defense in descending order
        """
        data_query = self.dataframe.sort_values(by=["sp_defense"], ascending=False)
        return data_query

    def sort_by_sp_attack(self):
        """
        Sorts all pokemon by special attack in descending order

        Returns:
            DatabaseQuery: contains all pokemon sorted by special attack in descending order
        """
        data_query = self.dataframe.sort_values(by=["sp_attack"], ascending=False)
        return data_query

    def sort_by_stat(self, stat):
        """
        Sorts all pokemon by specified stat in descending order

        Args:
            stat(str): the stat to sort by
        Returns:
            DatabaseQuery: contains all pokemon sorted by specifeid stat in descending order
        """
        if stat == "hp":
            data_query = self.sort_by_hp()
        elif stat == "attack":
            data_query = self.sort_by_sp_attack()
        elif stat == "defense":
            data_query = self.sort_by_defense()
        elif stat == "speed":
            data_query = self.sort_by_speed()
        elif stat == "spattack":
            data_query = self.sort_by_sp_attack()
        elif stat == "spdefense":
            data_query = self.sort_by_sp_defense()
        return DatabaseQuery(data_query)

    def index(self, key):
        """
        Get the DataRow at the specified index
        Alias for bracket index lookup

        Args:
            key(int): The index to be searched for
        Returns
            DataRow: contains the pokemon data at the index
        """
        return self.query[key]

    def first(self):
        """
        Gets the first item in the database

        Returns:
            DataRow: contains the pokemon data at the top of the database
        """
        return self.query[0]

    def isempty(self):
        """
        Checks if the database is empty

        Returns:
            bool: True if the database is empty, else False
        """
        if len(self.query) == 0:
            return True
        else:
            return False

class DataRow():
    """
    Data container for pokemon data
    """

    def __init__(self, serial):
        self.index = serial[0]
        self.abilities = [i.strip("\'") for i in serial[1].strip('[').strip(']').split(',')]
        self.against_bug = serial[2]
        self.against_dark = serial[3]
        self.against_dragon = serial[4]
        self.against_electric = serial[5]
        self.against_fairy = serial[6]
        self.against_fight = serial[7]
        self.gainst_fire = serial[8]
        self.against_flying = serial[9]
        self.against_ghost = serial[10]
        self.against_grass = serial[11]
        self.against_ground = serial[12]
        self.against_ice = serial[13]
        self.against_normal = serial[14]
        self.against_poison = serial[15]
        self.against_psychic = serial[16]
        self.against_rock = serial[17]
        self.against_steel = serial[18]
        self.against_water = serial[19]
        self.attack = serial[20]
        self.base_egg_steps = serial[21]
        self.base_happiness = serial[22]
        self.base_total = serial[23]
        self.capture_rate = serial[24]
        self.classfication = serial[25]
        self.defense = serial[26]
        self.experience_growth = serial[27]
        self.height = serial[28]
        self.hp = serial[29]
        self.japanese_name = serial[30]
        self.name = serial[31]
        self.percentage_male = serial[32]
        self.pokedex_number = serial[33]
        self.sp_attack = serial[34]
        self.sp_defense = serial[35]
        self.speed = serial[36]
        self.type1 = serial[37]
        self.type2 = serial[38]
        self.weight = serial[39]
        self.generation = serial[40]
        self.is_legendary = serial[41]

class Database(DatabaseQuery):

    def __init__(self, database="resources/data/data.csv"):
        """
        Loads pokemon data from a csv
        Uses "resources/data/data.csv" as default database

        Args:
            database(str): Address of the csv to be used
        """
        self.database_address = database
        self.dataframe = pd.read_csv(self.database_address)
        super().__init__(self.dataframe)
