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


def show_all():
    global  database
    if database is None:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")
        return
    query = Query()
    show(database.advanced_search(query))


def create():
    global database
    if database is not None:
        database.save()
    filename = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"), ("All files", "*.*")),
                                    title='Введите название базы данных',
                                    initialfile='Default.txt')
    if filename != "":
        filename = filename.strip()
        if filename[-4:] == '.txt':
            filename = filename[:-4]
        database = DataBase(filename, 'create')


def save():
    global database
    if database is not None:
        database.save()
        # database.close()
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
        filename = filename.strip()
        if filename[-4:] == '.txt':
            filename = filename[:-4]
        database = DataBase(filename, 'load')


def load_backup():
    global database
    if database is not None:
        database.save()
        database.close()
    filename = fd.askopenfilename(filetypes=(("BACKUP files", "*.backup"), ("All files", "*.*")),
                                    title='Введите название базы данных')
    if filename != "":
        filename = filename.strip()
        if filename[-7:] == '.backup':
            filename = filename[:-7]
        database = DataBase(filename, 'backup')


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
            database.add_record(card)
            show_all()
        except Exception as exep:
            mb.showerror("Ошибка", exep.args[0])


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
    foil.insert(0, 'Foil Yes/No')
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
        return

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
    foil.insert(0, 'Foil Yes/No')
    foil.pack(side=LEFT)
    price = Entry(l2, width=10, text='Price')
    price.delete(0, END)
    price.insert(0, 'Price float')
    price.pack(side=LEFT)
    l2.pack()
    button = Button(window, text='Найти', command=fill).pack()


def fast_delete():
    global database

    if database is None:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")
        return

    def fill():
        try:
            query = Query(_name=name.get(), _set=set.get(), _language=language.get(), )
            database.fast_delete(query)
            show_all()
        except Exception as exep:
            mb.showerror("Ошибка", exep.args[0])
            return

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
    button = Button(window, text='Удалить', command=fill).pack()


def advanced_delete():
    global database

    if database is None:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")
        return

    def fill():
        try:
            query = Query(_name=name.get(), _serial_number=serial_number.get(), _set=set.get(),
                          _language=language.get(),
                          _type=type.get(), _artist=artist.get(), _rarity=rarity.get(), _foil=foil.get(),
                          _price=price.get())
            database.advanced_delete(query)
            show_all()
        except Exception as exep:
            mb.showerror("Ошибка", exep.args[0])
            return

    window = Toplevel()
    window.resizable(False, False)
    Label(window, text='Введите карту для удаления карту').pack(side=TOP)
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
    foil.insert(0, 'Foil Yes/No')
    foil.pack(side=LEFT)
    price = Entry(l2, width=10, text='Price')
    price.delete(0, END)
    price.insert(0, 'Price float')
    price.pack(side=LEFT)
    l2.pack()
    button = Button(window, text='Удалить', command=fill).pack()


def edit_record():
    global database

    if database is None:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")
        return

    def fill():
        old_query = Query(_name=name.get(), _set=set.get(), _language=language.get())
        if database._database.get((old_query.name, old_query.set, old_query.language), 0) == 0:
            mb.showwarning(title='Предупреждение', message='В Базе Данных нет записи с такими ключевыми полями!')
        else:
            try:
                new_card = Card(_name=old_query.name, _set=old_query.set, _language=old_query.language,
                            _serial_number=serial_number.get(), _type=type.get(), _artist=artist.get(),
                            _rarity=rarity.get(), _foil=foil.get(), _price=price.get())
                database.edit_record(old_query, new_card)
                show_all()
            except Exception as exep:
                mb.showerror("Ошибка", exep.args[0])

    window = Toplevel()
    window.resizable(False, False)
    Label(window, text='Введите ключевые поля').pack(side=TOP)
    l1 = Frame(window)
    name = Entry(l1, width=35, text='Name')
    name.delete(0, END)
    name.insert(0, 'Name')
    name.pack(side=LEFT)
    set = Entry(l1, width=25, text='Set')
    set.delete(0, END)
    set.insert(0, 'Set')
    set.pack(side=LEFT)
    language = Entry(l1, width=15, text='Language')
    language.delete(0, END)
    language.insert(0, 'Language')
    language.pack(side=LEFT)
    l1.pack()
    Label(window, text='Введите измененные неключевые поля').pack(side=TOP)
    l2 = Frame(window)
    serial_number = Entry(l2, width=8, text='№')
    serial_number.delete(0, END)
    serial_number.insert(0, '№ int')
    serial_number.pack(side=LEFT)
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
    foil.insert(0, 'Foil Yes/No')
    foil.pack(side=LEFT)
    price = Entry(l2, width=10, text='Price')
    price.delete(0, END)
    price.insert(0, 'Price float')
    price.pack(side=LEFT)
    l2.pack()
    button = Button(window, text='Найти', command=fill).pack()


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
options_menu.add_command(label='Отобразить Базу Данных', command=show_all)
options_menu.add_command(label='Добавить запись', command=add_record)
options_menu.add_command(label='Быстрый поиск', command=fast_search)
options_menu.add_command(label='Расширенный поиск', command=advanced_search)
options_menu.add_command(label='Быстрое удаление', command=fast_delete)
options_menu.add_command(label='Расширенное удаление', command=advanced_delete)
options_menu.add_command(label='Редактировать запись', command=edit_record)

main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Действия', menu=options_menu)

text = Text(width=145, height=30, wrap=WORD) #state=DISABLED
text.pack(side=LEFT)
scroll = Scrollbar(command=text.yview)
scroll.pack(side=LEFT, fill=Y)
text.config(yscrollcommand=scroll.set)

root.mainloop()
