from tkinter import *
from carddb import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os

database = None


def show(cards):
    text.delete(0.0, END)
    text.insert(END, Card.first_string)
    for card in cards:
        text.insert(END, card.get_string())


def create():
    global database
    if database is not None:
        database.save()
        database.save()
    filename = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"), ("All files", "*.*")),
                                    title='Введите название базы данных',
                                    initialfile='Default.txt')
    if filename != "":
        filename = filename.strip()
        if filename[-4:] == '.txt':
            filename = filename[:-4]
        open(filename + '.txt', 'w').close()
        open(filename + '.backup', 'w').close()
        database = DataBase(filename, 'create')


def save():
    global database
    if database is not None:
        database.save()
        database.close()
    else:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")


def delete():
    global database
    if database is None:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")
    else:
        database.delete_database()
        database = None


def load():
    global database
    if database is not None:
        database.save()
        database.close()
    filename = fd.askopenfilename(filetypes=(("TXT files", "*.txt"), ("All files", "*.*")),
                                    title='Введите название базы данных для загрузки')
    if filename != "":
        database = DataBase(filename, 'load')


def load_backup():
    global database
    if database is not None:
        database.save()
        database.close()
    filename = fd.askopenfilename(filetypes=(("BACKUP files", "*.backup"), ("All files", "*.*")),
                                    title='Введите название базы данных')
    if filename != "":
        database = DataBase(filename, 'load_from_backup')


def import_csv():
    global database
    if database is not None:
        database.import_csv()


def add_record():
    global database

    if database is None:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")
        return

    def fill():
        try:
            card = Card(_name=name.get(), _set=set.get(), _serial_number=serial_number.get(), _language=language.get(),
                        _type=type.get(), _artist=artist.get(), _rarity=rarity.get(), _foil=foil.get(),
                        _price=price.get())
        except Exception as exep:
            mb.showerror("Ошибка", exep.args[0])
            return
        database.add_record(card)

    window = Toplevel()
    window.resizable(False, False)
    Label(window, text='Добавьте карту').pack(side=TOP)
    l2 = Frame(window)
    name = Entry(l2, width=35, text='Name')
    name.delete(0, END)
    name.insert(0, 'Name')
    name.pack(side=LEFT)
    set = Entry(l2, width=25, text='Set')
    set.delete(0, END)
    set.insert(0, 'Set')
    set.pack(side=LEFT)
    serial_number = Entry(l2, width=8, text='№')
    serial_number.delete(0, END)
    serial_number.insert(0, '№ int')
    serial_number.pack(side=LEFT)
    language = Entry(l2, width=15, text='Language')
    language.delete(0, END)
    language.insert(0, 'Language')
    language.pack(side=LEFT)
    type = Entry(l2, width=21, text='Type')
    type.delete(0, END)
    type.insert(0, 'Type')
    type.pack(side=LEFT)
    artist = Entry(l2, width=25, text='Artist')
    artist.delete(0, END)
    artist.insert(0, 'Artist')
    artist.pack(side=LEFT)
    rarity = Entry(l2, width=13, text='Rarity')
    rarity.delete(0, END)
    rarity.insert(0, 'Rarity')
    rarity.pack(side=LEFT)
    foil = Entry(l2, width=15, text='Foil')
    foil.delete(0, END)
    foil.insert(0, 'Foil True/False')
    foil.pack(side=LEFT)
    price = Entry(l2, width=10, text='Price')
    price.delete(0, END)
    price.insert(0, 'Price float')
    price.pack(side=LEFT)
    l2.pack()
    button = Button(window, text='Добавить', command=fill).pack()


def fast_search():
    global database

    if database is None:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")
        return

    def fill():
        try:
            query = Query(_name=name.get(), _set=set.get(), _language=language.get(),)
        except Exception as exep:
            mb.showerror("Ошибка", exep.args[0])
            return
        show(database.fast_search(query))

    window = Toplevel()
    window.resizable(False, False)
    Label(window, text='Введите ключевые поля').pack(side=TOP)
    l2 = Frame(window)
    name = Entry(l2, width=35, text='Name')
    name.delete(0, END)
    name.insert(0, 'Name')
    name.pack(side=LEFT)
    set = Entry(l2, width=25, text='Set')
    set.delete(0, END)
    set.insert(0, 'Set')
    set.pack(side=LEFT)
    language = Entry(l2, width=15, text='Language')
    language.delete(0, END)
    language.insert(0, 'Language')
    language.pack(side=LEFT)
    l2.pack()
    button = Button(window, text='Найти', command=fill).pack()


def advanced_search():
    global database

    if database is None:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")

    def fill():
        try:
            query = Query(_name=name.get(), _serial_number=serial_number.get(), _set=set.get(), _language=language.get(),
                          _type=type.get(), _artist=artist.get(), _rarity=rarity.get(), _foil=foil.get(), _price=price.get())
        except Exception as exep:
            mb.showerror("Ошибка", exep.args[0])
            return
        show(database.advanced_search(query))

    window = Toplevel()
    window.resizable(False, False)
    Label(window, text='Найдите карту').pack(side=TOP)
    l2 = Frame(window)
    name = Entry(l2, width=35, text='Name')
    name.delete(0, END)
    name.insert(0, 'Name')
    name.pack(side=LEFT)
    set = Entry(l2, width=25, text='Set')
    set.delete(0, END)
    set.insert(0, 'Set')
    set.pack(side=LEFT)
    serial_number = Entry(l2, width=8, text='№')
    serial_number.delete(0, END)
    serial_number.insert(0, '№ int')
    serial_number.pack(side=LEFT)
    language = Entry(l2, width=15, text='Language')
    language.delete(0, END)
    language.insert(0, 'Language')
    language.pack(side=LEFT)
    type = Entry(l2, width=21, text='Type')
    type.delete(0, END)
    type.insert(0, 'Type')
    type.pack(side=LEFT)
    artist = Entry(l2, width=25, text='Artist')
    artist.delete(0, END)
    artist.insert(0, 'Artist')
    artist.pack(side=LEFT)
    rarity = Entry(l2, width=13, text='Rarity')
    rarity.delete(0, END)
    rarity.insert(0, 'Rarity')
    rarity.pack(side=LEFT)
    foil = Entry(l2, width=15, text='Foil')
    foil.delete(0, END)
    foil.insert(0, 'Foil True/False')
    foil.pack(side=LEFT)
    price = Entry(l2, width=10, text='Price')
    price.delete(0, END)
    price.insert(0, 'Price float')
    price.pack(side=LEFT)
    l2.pack()
    button = Button(window, text='Найти', command=fill).pack()


def fast_delete():
    pass


def advanced_delete():
    pass


def edit_record():
    pass


root = Tk()
root.title('DataBase')
root.resizable(False, False)
main_menu = Menu(root)
root.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Создать', command=create)
file_menu.add_command(label='Сохранить', command=save)
file_menu.add_command(label='Удалить', command=delete)
file_menu.add_command(label='Загрузить', command=load)
file_menu.add_command(label='Загрузить backup', command=load_backup)
file_menu.add_command(label='Импорт в csv', command=import_csv)

options_menu = Menu(main_menu, tearoff=0)
options_menu.add_command(label='Добавить запись', command=add_record)
options_menu.add_command(label='Быстрый поиск', command=fast_search)
options_menu.add_command(label='Расширенный поиск', command=advanced_search)
options_menu.add_command(label='Быстрое удаление', command=fast_delete)
options_menu.add_command(label='Расширенное удаление', command=advanced_delete)
options_menu.add_command(label='Редактировать запись', command=edit_record)

main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Действия', menu=options_menu)

text = Text(width=140, height=30, wrap=WORD) #state=DISABLED
text.pack(side=LEFT)
scroll = Scrollbar(command=text.yview)
scroll.pack(side=LEFT, fill=Y)
text.config(yscrollcommand=scroll.set)

root.mainloop()
