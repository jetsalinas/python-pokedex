import csv

class Favorites():

    def __init__(self):
        with open("resources/data/fav.csv") as fav_file:
            csv_reader = csv.reader(fav_file)
            self.favs = {int(x[0]) for x in csv_reader}

    def __iter__(self):
        return iter(self.favs)

    def append(self, key):
        self.favs = self.favs.union({key})
        with open("resources/data/fav.csv", "w") as fav_file:
            csv_writer = csv.writer(fav_file)
            for item in self.favs:
                csv_writer.writerow([item])

    def remove(self, key):
        self.favs = self.favs.difference({key})
        with open("resources/data/fav.csv", "w") as fav_file:
            csv_writer = csv.writer(fav_file)
            for item in self.favs:
                csv_writer.writerow([item])
