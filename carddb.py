import os
import os.path
from tkinter import messagebox as mb


class Card:
    possible_types = set(["Creature", "Artifact", "Artifact Creature", "Planeswalker", "Land", "Sorcery", "Instant",
                         "Enchantment", "Token", "Emblem"])
    possible_rarity = set(["Common", "Uncommon", "Rare", "Mythic"])
    possible_foil = set(['Yes', 'No'])
    types_string = "Creature, Artifact, Artifact Creature, Planeswalker, Land, Sorcery, Instant, Enchantment, Token, Emblem"
    rarity_string = "Common, Uncommon, Rare, Mythic"
    foil_string = "Yes, No"
    first_string = '{:<3.3}|{:<30.30}|{:<20.20}|{:<3.3}|{:<10.10}|{:<17.17}|{:<20.20}|{:<8.8}|{:<5.5}|{:<5.5}\n'.format(
            'id', 'Name', 'Set', '№', 'Language', 'Type', 'Artist', 'Rarity', 'Foil', 'Price '+'$')

    def check_name(self):
        if not self.name.isalpha():
            raise Exception("Wrong NAME format")

    def check_serial_number(self):
        if not self.serial_number.isnumeric():
            raise Exception("Wrong SERIAL NUMBER format (int)")

    def check_set(self):
        if not self.set.isalpha():
            raise Exception("Wrong SET format")

    def check_type(self):
        if self.type not in Card.possible_types:
            raise Exception("Wrong TYPE format.\nPossible TYPES:\n" + self.types_string)

    def check_artist(self):
        if not self.artist.replace(" ", "").isalpha():
            raise Exception("Wrong ARTIST format")

    def check_language(self):
        if not self.language.isalpha():
            raise Exception("Wrong LANGUAGE format")

    def check_rarity(self):
        if self.rarity not in Card.possible_rarity:
            raise Exception("Wrong RARITY format.\nPossible RARITY:\n" + self.rarity_string)

    def check_foil(self):
        if self.foil not in self.possible_foil:
            raise Exception("Wrong FOIL format.\nPossible RARITY:\n" + self.foil_string)

    def check_price(self):
        if not self.price.replace('.', '').isnumeric():
            raise Exception("Wrong PRICE format (float)")

    def __init__(self, _name, _serial_number, _set, _language, _type, _artist, _rarity, _foil, _price):
        self.name = _name # key field
        self.serial_number = _serial_number
        self.set = _set # key field
        self.type = _type
        self.artist = _artist
        self.language = _language # key field
        self.rarity = _rarity
        self.foil = _foil
        self.price = _price
        # try:
        # self.check_name()
        self.check_serial_number()
        # self.check_set()
        self.check_type()
        # self.check_artist()
        # self.check_language()
        self.check_rarity()
        self.check_foil()
        # self.check_price()
        # except Exception as exep:
        #    print(exep.args[0])

    def get_string(self):
        string = '{:<3.3}|{:<30.30}|{:<20.20}|{:<3.3}|{:<10.10}|{:<17.17}|{:<20.20}|{:<8.8}|{:<5.5}|{:<5.5}\n'.format(
            str(self.id), self.name, self.set, str(self.serial_number), self.language, self.type, self.artist, self.rarity,
            self.foil, str(self.price)+'$') # len == 130
        return string


class Query:
    def __init__(self, _name='', _serial_number='', _set='', _language='', _type='', _artist='', _rarity='', _foil='', _price=''):
        self.name = _name
        if _serial_number == '':
            self.serial_number = _serial_number
        else:
            self.serial_number = int(_serial_number)
        self.set = _set
        self.type = _type
        self.artist = _artist
        self.language = _language
        self.rarity = _rarity
        self.foil = _foil
        if _price == "":
            self.price = _price
        else:
            self.price = float(_price)


class DataBase:
    def __init__(self, filename: str, option: str):
        self._database = {} # key=(card.name, card.set, card.language) value=(card, id)
        self._positions = {} # key=id, value=(card.name, card.set, card.language)
        filename = filename.strip()
        self._filename = filename + '.txt'
        self._backup_filename = filename + '.backup'
        self._csv_filename = filename + 'csv'
        self._size = 0
        self._line_len = 130 + 2
        if not os.path.exists(self._filename):
            open(self._filename, 'w').close()
        self._backup_stream = open(self._filename, 'r+')
        if not os.path.exists(self._backup_filename):
            open(self._backup_filename, 'w').close()
        self._save_stream = open(self._filename, 'r+')
        self._backup_stream = open(self._backup_filename, 'r+')
        if option == 'load':
            self.load()
        elif option == 'backup':
            self.load_from_backup()
        elif option == 'csv':
            self.import_csv()
        else:
            self.create()

    def load_from_backup(self):
        self._backup_stream.seek(0)
        self._save_stream.seek(0)
        for line in self._backup_stream:
            if line != '' and line[0] != ' ':
                self._save_stream.write(line)
        self._save_stream.flush()
        self._save_stream.seek(0)
        # self._backup_stream.close()
        # open(self._backup_filename, 'w').close()
        # self._backup_stream = open(self._backup_filename, 'rt+')
        self.load()


    def load(self):
        self._backup_stream.close()
        self._backup_stream = open(self._backup_filename, 'rt+')
        for line in self._save_stream:
            if line != '' and line[0]!= '':
                id, name, set, serial_number, language, type, artist, rarity, foil, price = map(str.strip, line.split('|'))
                price = price.replace('$', '')
                card = Card(_name=name, _set=set, _serial_number=serial_number, _language=language, _type=type,
                            _artist=artist, _rarity=rarity, _foil=foil, _price=price)
                self.add_record(card)

    def import_csv(self):
        pass

    def create(self):
        pass

    def close(self):
        self._backup_stream.close()
        self._save_stream.close()

    def save(self):
        self._backup_stream.seek(0)
        self._save_stream.seek(0)
        self._save_stream = open(self._filename, 'w')
        for line in self._backup_stream:
            line = line.strip()
            if line == '':
                break
            self._save_stream.write(line + '\n')
        self._save_stream.flush()

    def delete_database(self):
        pass

    def add_record(self, card: Card):
        if (card.name, card.set, card.language) in self._database:
            mb.showerror("Ошибка", "Запись с такими ключевыми словами уже существует") # запись уже существует
        else:
            card.id = self._size
            # card = Card(query.name, query.serial_number, query.set, query.language, query.type, query.artist,
            #             query.rarity, query.foil, query.price)
            self._database[(card.name, card.set, card.language)] = (card, self._size)
            self._positions[self._size] = (card.name, card.set, card.language)
            self._backup_stream.seek(self._size * self._line_len)
            self._backup_stream.write(card.get_string())
            self._backup_stream.flush()
            self._size += 1
        self._backup_stream.flush()

    def fast_search(self, query: Query):
        if self._database.get((query.name, query.set, query.language), 0) == 0:
            return []
        else:
            return [self._database[(query.name, query.set, query.language)][0]]

    def advanced_search(self, query: Query):
        result = []
        for key, (card, id) in self._database.items():
            if query.name != "" and query.name != card.name:
                continue
            if query.serial_number != "" and query.serial_number != card.serial_number:
                continue
            if query.set != "" and query.set != card.set:
                continue
            if query.language != "" and query.language != card.language:
                continue
            if query.type != "" and query.type != card.type:
                continue
            if query.artist != "" and query.artist != card.artist:
                continue
            if query.rarity != "" and query.rarity != card.rarity:
                continue
            if query.foil != "" and query.foil != card.foil:
                continue
            if query.price != "" and query.price != card.price:
                continue
            result.append(card)
        return result

    def delete_records(self, array): # get array of records ids to delete
        for record_id in array:
            self._size -= 1
            key = self._positions[record_id]
            self._positions.pop(record_id)
            self._database.pop(key)
            self._backup_stream.seek(self._size * self._line_len)
            self._backup_stream.write(" " * (self._line_len - 2) + '\n')
            if record_id != self._size:
                key = self._positions[self._size]
                card, card_id = self._database[key]
                card.id = record_id
                # rewriting file
                self._backup_stream.seek(card_id * self._line_len)
                self._backup_stream.write(" " * (self._line_len - 2) + '\n')
                self._backup_stream.seek(record_id * self._line_len)
                self._backup_stream.write(card.get_string())
                # changing database
                self._database.pop((card.name, card.set, card.language))
                self._positions.pop(card_id)
                self._database[(card.name, card.set, card.language)] = (card, record_id)
                self._positions[record_id] = (card.name, card.set, card.language)
        self._backup_stream.flush()

    def fast_delete(self, query: Query):
        if self._database.get((query.name, query.set, query.language), 0) != 0:
            self.delete_records([self._database[(query.name, query.set, query.language)][1]])

    def advanced_delete(self, query: Query):
        result = []
        for key, (card, id) in self._database.items():
            if query.name != "" and query.name != card.name:
                continue
            if query.serial_number != "" and query.serial_number != card.serial_number:
                continue
            if query.set != "" and query.set != card.set:
                continue
            if query.language != "" and query.language != card.language:
                continue
            if query.type != "" and query.type != card.type:
                continue
            if query.artist != "" and query.artist != card.artist:
                continue
            if query.rarity != "" and query.rarity != card.rarity:
                continue
            if query.foil != "" and query.foil != card.foil:
                continue
            if query.price != "" and query.price != card.price:
                continue
            result.append(id)
        self.delete_records(result)

    def edit_record(self, old_query: Query, new_card: Card):
        if self._database.get((old_query.name, old_query.set, old_query.language), 0) != 0:
            old_card = Card(_name=old_query.name, _set=old_query.set, _language=old_query.language,
                            _serial_number=new_card.serial_number, _type=new_card.type, _artist=new_card.artist,
                            _rarity=new_card.rarity, _foil=new_card.foil, _price=new_card.price)
            self.fast_delete(old_card)
            self.add_record(new_card)
        else:
            pass
