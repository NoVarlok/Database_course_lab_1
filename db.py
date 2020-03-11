from tkinter import *
from carddb import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import time
import os

database = None


def show(cards):
    text.delete(0.0, END)
    text.insert(END, Card.first_string)
    text.insert(END, "-" * 140 + '\n')
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
    Label(window, text='Добавьте карту').grid(row=0, column=4)

    Label(window, width=35, text='Name').grid(row=1, column=0)
    Label(window, width=25, text='Set').grid(row=1, column=1)
    Label(window, width=8, text='№ (int)').grid(row=1, column=2)
    Label(window, width=15, text='Language').grid(row=1, column=3)
    Label(window, width=21, text='Type').grid(row=1, column=4)
    Label(window, width=25, text='Artist').grid(row=1, column=5)
    Label(window, width=13, text='Rarity').grid(row=1, column=6)
    Label(window, width=15, text='Foil (Yes/No)').grid(row=1, column=7)
    Label(window, width=10, text='Price').grid(row=1, column=8)

    name = Entry(window, width=35, text='Name')
    name.delete(0, END)
    name.grid(row=2, column=0)
    set = Entry(window, width=25, text='Set')
    set.delete(0, END)
    set.grid(row=2, column=1)
    serial_number = Entry(window, width=8, text='№')
    serial_number.delete(0, END)
    serial_number.grid(row=2, column=2)
    language = Entry(window, width=15, text='Language')
    language.delete(0, END)
    language.grid(row=2, column=3)
    type = Entry(window, width=21, text='Type')
    type.delete(0, END)
    type.grid(row=2, column=4)
    artist = Entry(window, width=25, text='Artist')
    artist.delete(0, END)
    artist.grid(row=2, column=5)
    rarity = Entry(window, width=13, text='Rarity')
    rarity.delete(0, END)
    rarity.grid(row=2, column=6)
    foil = Entry(window, width=15, text='Foil')
    foil.delete(0, END)
    foil.grid(row=2, column=7)
    price = Entry(window, width=10, text='Price')
    price.delete(0, END)
    price.grid(row=2, column=8)
    button = Button(window, text='Добавить', command=fill)
    button.grid(row=3, column=4)


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
    Label(window, text='Найти карту').grid(row=0, column=1)

    Label(window, width=35, text='Name').grid(row=1, column=0)
    Label(window, width=25, text='Set').grid(row=1, column=1)
    Label(window, width=15, text='Language').grid(row=1, column=2)

    name = Entry(window, width=35, text='Name')
    name.delete(0, END)
    name.grid(row=2, column=0)
    set = Entry(window, width=25, text='Set')
    set.delete(0, END)
    set.grid(row=2, column=1)
    language = Entry(window, width=15, text='Language')
    language.delete(0, END)
    language.grid(row=2, column=2)
    button = Button(window, text='Найти', command=fill)
    button.grid(row=3, column=1)


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
    Label(window, text='Найдите карту').grid(row=0, column=4)

    Label(window, width=35, text='Name').grid(row=1, column=0)
    Label(window, width=25, text='Set').grid(row=1, column=1)
    Label(window, width=8, text='№ (int)').grid(row=1, column=2)
    Label(window, width=15, text='Language').grid(row=1, column=3)
    Label(window, width=21, text='Type').grid(row=1, column=4)
    Label(window, width=25, text='Artist').grid(row=1, column=5)
    Label(window, width=13, text='Rarity').grid(row=1, column=6)
    Label(window, width=15, text='Foil (Yes/No)').grid(row=1, column=7)
    Label(window, width=10, text='Price').grid(row=1, column=8)

    name = Entry(window, width=35, text='Name')
    name.delete(0, END)
    name.grid(row=2, column=0)
    set = Entry(window, width=25, text='Set')
    set.delete(0, END)
    set.grid(row=2, column=1)
    serial_number = Entry(window, width=8, text='№')
    serial_number.delete(0, END)
    serial_number.grid(row=2, column=2)
    language = Entry(window, width=15, text='Language')
    language.delete(0, END)
    language.grid(row=2, column=3)
    type = Entry(window, width=21, text='Type')
    type.delete(0, END)
    type.grid(row=2, column=4)
    artist = Entry(window, width=25, text='Artist')
    artist.delete(0, END)
    artist.grid(row=2, column=5)
    rarity = Entry(window, width=13, text='Rarity')
    rarity.delete(0, END)
    rarity.grid(row=2, column=6)
    foil = Entry(window, width=15, text='Foil')
    foil.delete(0, END)
    foil.grid(row=2, column=7)
    price = Entry(window, width=10, text='Price')
    price.delete(0, END)
    price.grid(row=2, column=8)
    button = Button(window, text='Найти', command=fill)
    button.grid(row=3, column=4)


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
    Label(window, text='Введите ключевые поля').grid(row=0, column=1)

    Label(window, width=35, text='Name').grid(row=1, column=0)
    Label(window, width=25, text='Set').grid(row=1, column=1)
    Label(window, width=15, text='Language').grid(row=1, column=2)

    name = Entry(window, width=35, text='Name')
    name.delete(0, END)
    name.grid(row=2, column=0)
    set = Entry(window, width=25, text='Set')
    set.delete(0, END)
    set.grid(row=2, column=1)
    language = Entry(window, width=15, text='Language')
    language.delete(0, END)
    language.grid(row=2, column=2)
    button = Button(window, text='Удалить', command=fill)
    button.grid(row=3, column=1)


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
    Label(window, text='Введите карту для удаления').grid(row=0, column=4)
    Label(window, width=35, text='Name').grid(row=1, column=0)
    Label(window, width=25, text='Set').grid(row=1, column=1)
    Label(window, width=8, text='№ (int)').grid(row=1, column=2)
    Label(window, width=15, text='Language').grid(row=1, column=3)
    Label(window, width=21, text='Type').grid(row=1, column=4)
    Label(window, width=25, text='Artist').grid(row=1, column=5)
    Label(window, width=13, text='Rarity').grid(row=1, column=6)
    Label(window, width=15, text='Foil (Yes/No)').grid(row=1, column=7)
    Label(window, width=10, text='Price').grid(row=1, column=8)

    name = Entry(window, width=35, text='Name')
    name.delete(0, END)
    name.grid(row=2, column=0)
    set = Entry(window, width=25, text='Set')
    set.delete(0, END)
    set.grid(row=2, column=1)
    serial_number = Entry(window, width=8, text='№')
    serial_number.delete(0, END)
    serial_number.grid(row=2, column=2)
    language = Entry(window, width=15, text='Language')
    language.delete(0, END)
    language.grid(row=2, column=3)
    type = Entry(window, width=21, text='Type')
    type.delete(0, END)
    type.grid(row=2, column=4)
    artist = Entry(window, width=25, text='Artist')
    artist.delete(0, END)
    artist.grid(row=2, column=5)
    rarity = Entry(window, width=13, text='Rarity')
    rarity.delete(0, END)
    rarity.grid(row=2, column=6)
    foil = Entry(window, width=15, text='Foil')
    foil.delete(0, END)
    foil.grid(row=2, column=7)
    price = Entry(window, width=10, text='Price')
    price.delete(0, END)
    price.grid(row=2, column=8)
    button = Button(window, text='Удалить', command=fill)
    button.grid(row=3, column=4)


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
                new_card = Card(_name=new_name.get(), _set=new_set.get(), _language=new_language.get(),
                            _serial_number=new_serial_number.get(), _type=new_type.get(), _artist=new_artist.get(),
                            _rarity=new_rarity.get(), _foil=new_foil.get(), _price=new_price.get())
                database.edit_record(old_query, new_card)
                show_all()
            except Exception as exep:
                mb.showerror("Ошибка", exep.args[0])

    window = Toplevel()
    window.resizable(False, False)
    Label(window, text='Введите ключевые поля').grid(row=0, column=4)
    Label(window, width=35, text='Name').grid(row=1, column=0)
    Label(window, width=25, text='Set').grid(row=1, column=1)
    Label(window, width=15, text='Language').grid(row=1, column=2)

    name = Entry(window, width=35, text='Name')
    name.delete(0, END)
    name.grid(row=2, column=0)
    set = Entry(window, width=25, text='Set')
    set.delete(0, END)
    set.grid(row=2, column=1)
    language = Entry(window, width=15, text='Language')
    language.delete(0, END)
    language.grid(row=2, column=2)

    Label(window, text='Введите измененные поля').grid(row=3, column=4)
    Label(window, width=35, text='Name').grid(row=4, column=0)
    Label(window, width=25, text='Set').grid(row=4, column=1)
    Label(window, width=8, text='№ (int)').grid(row=4, column=2)
    Label(window, width=15, text='Language').grid(row=4, column=3)
    Label(window, width=21, text='Type').grid(row=4, column=4)
    Label(window, width=25, text='Artist').grid(row=4, column=5)
    Label(window, width=13, text='Rarity').grid(row=4, column=6)
    Label(window, width=15, text='Foil (Yes/No)').grid(row=4, column=7)
    Label(window, width=10, text='Price').grid(row=4, column=8)

    new_name = Entry(window, width=35)
    new_name.delete(0, END)
    new_name.grid(row=5, column=0)
    new_set = Entry(window, width=25)
    new_set.delete(0, END)
    new_set.grid(row=5, column=1)
    new_serial_number = Entry(window, width=15)
    new_serial_number.delete(0, END)
    new_serial_number.grid(row=5, column=2)
    new_language = Entry(window, width=15)
    new_language.delete(0, END)
    new_language.grid(row=5, column=3)
    new_type = Entry(window, width=25)
    new_type.delete(0, END)
    new_type.grid(row=5, column=4)
    new_artist = Entry(window, width=25)
    new_artist.delete(0, END)
    new_artist.grid(row=5, column=5)
    new_rarity = Entry(window, width=13)
    new_rarity.delete(0, END)
    new_rarity.grid(row=5, column=6)
    new_foil = Entry(window, width=15)
    new_foil.delete(0, END)
    new_foil.grid(row=5, column=7)
    new_price = Entry(window, width=10)
    new_price.delete(0, END)
    new_price.grid(row=5, column=8)
    button = Button(window, text='Применить изменения', command=fill)
    button.grid(row=6, column=4)


def performance_check():
    global database

    if database is None:
        mb.showerror("Ошибка", "Ни одна база данных не загруженна")
        return
    repeat = 7500
    records = []
    add_record_time = 0
    name = 'name'
    set = 0
    serial_number = '1'
    type = 'Creature'
    artist = 'artist'
    language = 'language'
    rarity = 'Common'
    foil = 'No'
    price = '300.0'
    for i in range(repeat):
        set = str(i)
        card = Card(_name=name, _set=set, _serial_number=serial_number, _type=type, _artist=artist, _language=language,
                    _rarity=rarity, _foil=foil, _price=price)
        start_time = time.time()
        database.add_record(card)
        finish_time = time.time()
        add_record_time += finish_time - start_time
        records.append(0)
    fast_search_time = 0
    card_key = database._positions[0]
    card = database._database[card_key][0]
    query = Query(_name=card.name, _set=card.set, _language=card.language)
    for i in range(repeat):
        start_time = time.time()
        database.fast_search(query)
        finish_time = time.time()
        fast_search_time += finish_time - start_time
    advanced_search_time = 0
    query = Query()
    for i in range(repeat):
        start_time = time.time()
        database.advanced_search(query)
        finish_time = time.time()
        advanced_search_time += finish_time - start_time
    fast_delete_time = 0
    start_time = time.time()
    database.delete_records(records)
    finish_time = time.time()
    fast_delete_time = finish_time - start_time
    print("{0} - repeated {1} times - time: {2}".format('Add_record', str(repeat), add_record_time))
    print("{0} - repeated {1} times - time: {2}".format('Fast_delete', str(repeat), fast_delete_time))
    print("{0} - repeated {1} times - time: {2}".format('Fast_search_time', str(repeat), fast_search_time))
    # advanced_search_time = None
    print("{0} - repeated {1} times - time: {2}".format('Advanced_search_time', str(repeat), advanced_search_time))


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

performance_menu = Menu(main_menu, tearoff=0)
performance_menu.add_command(label='Проверка производительности', command=performance_check)
# performance_menu.add_command(label='Удаление записи', command=)

main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Действия', menu=options_menu)
main_menu.add_cascade(label='Производительность', menu=performance_menu)

text = Text(width=145, height=30, wrap=WORD) #state=DISABLED
text.pack(side=LEFT)
scroll = Scrollbar(command=text.yview)
scroll.pack(side=LEFT, fill=Y)
text.config(yscrollcommand=scroll.set)

root.mainloop()
