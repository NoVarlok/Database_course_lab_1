from tkinter import *
from carddb import *
import os

database = None


def create():
    global database
    filename = ''
    if database is not None:
        database.save()
    database = DataBase(filename, 'create')


def delete():
    global database
    filename = ''
    if database is None:
        # error message
        pass
    else:
        database.delete_database()
        database = None


def load():
    global database
    filename = ''
    if database is not None:
        database.save()
    database = DataBase(filename, 'load')


def load_backup():
    global database
    filename = ''
    if database is not None:
        database.save()
    database = DataBase(filename, 'load_from_backup')


def import_csv():
    global database
    filename = ''
    database.import_csv()


def add_record():
    pass


def fast_search():
    pass


def advanced_search():
    pass


def fast_delete():
    pass


def advanced_delete():
    pass


def edit_record():
    pass


root = Tk()
main_menu = Menu(root)
root.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Создать', command=create())
file_menu.add_command(label='Сохранить', command=create())
file_menu.add_command(label='Удалить', command=delete())
file_menu.add_command(label='Загрузить', command=load())
file_menu.add_command(label='Загрузить backup', command=load_backup())
file_menu.add_command(label='Импорт в csv', command=import_csv())

options_menu = Menu(main_menu, tearoff=0)
options_menu.add_command(label='Добавить запись', command=add_record())
options_menu.add_command(label='Быстрый поиск', command=fast_search())
options_menu.add_command(label='Расширенный поиск', command=advanced_search())
options_menu.add_command(label='Быстрое удаление', command=fast_delete())
options_menu.add_command(label='Расширенное удаление', command=advanced_delete())
options_menu.add_command(label='Редактировать запись', command=edit_record())

main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Действия', menu=options_menu)

text = Text(width=130, height=30, wrap=WORD) #state=DISABLED
text.pack()
scroll = Scrollbar(command=text.yview)
scroll.pack(side=LEFT, fill=Y)
text.config(yscrollcommand=scroll.set)

root.mainloop()
