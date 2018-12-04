"""
Module to save and load favorites for python-pokedex

:Author:    Jose Enrico Salinas
:Version:   20181204
"""

import csv

class Favorites():
    """
    Handles fav saving and reading
    """

    def __init__(self):
        """
        Reads resources/data/fav.csv and loads a set object from it
        """
        with open("resources/data/fav.csv") as fav_file:
            csv_reader = csv.reader(fav_file)
            self.favs = {int(x[0]) for x in csv_reader if x[0] != ''}

    def __iter__(self):
        return iter(self.favs)

    def append(self, key):
        """
        Adds an item to favorites and saves it

        Args:
            key(str): Index of pokemon to be saved
        """
        self.favs = self.favs.union({key})
        with open("resources/data/fav.csv", "w", newline='') as fav_file:
            csv_writer = csv.writer(fav_file, )
            for item in self.favs:
                csv_writer.writerow([item])

    def remove(self, key):
        """
        Removes an item from the favorites if it exists and saves the favorites

        Args:
            key(str): Index of pokemon to be removed
        """
        self.favs = self.favs.difference({key})
        with open("resources/data/fav.csv", "w", newline='') as fav_file:
            csv_writer = csv.writer(fav_file)
            for item in self.favs:
                csv_writer.writerow([item])
