import datetime
import os
import json
import sys

class message: # Рабочий класс сообщения
    def __init__(self, id, title, msg, date) -> None:
        self.id = id
        self.title = title
        self.msg = msg
        self.date = date
        pass

base_of_messages={} #Словарь сообщений

def read_file_to_base_of_message(): #Функция чтения JSON файла, возвращает словарь сообщений(класс messege)
    new_dict_of_msg = {}
    try:
        file = open('messsegDateBase.json','r', encoding='utf-8')
        count = 0
        for line in file: #построчное чтение данных из файла
            count+=1
            dict_of_message = json.loads(line)  #преобразование JSON строки в словарь
            msg = message(dict_of_message.get('id'),dict_of_message.get('title'),dict_of_message.get('msg'),dict_of_message.get('date'))
            new_dict_of_msg[count] = msg
        file.close()
    except FileNotFoundError as e: # Фаил с базой заметок не найден(первый запуск программы)
        return None
    # if len(new_dict_of_msg) == 0:   #обработка ошибок при прочтении файла(если фаил с побитыми данными)
    #     return None
    return new_dict_of_msg


def read_of_base_of_message(): #Функция выводит данные базы заметок на экранy
    for number in base_of_messages:
        print('\033[34mЗаголовок\033[0m = {}  \033[33mТекст заметки\033[0m = {}  \033[35mДата создания заметки\033[0m = {}'.format(base_of_messages[number].title,base_of_messages[number].msg,base_of_messages[number].date))


def write_base_of_message_in_file():   # Функция записывает данные базы в JSON файл построчно
    with open('messsegDateBase.json', 'w') as file:
        for key in base_of_messages:
            #{"id": 1, "title": "Заголовок", "msg": "Заметка", "date": "27-02-2023-22.09"} - пример записи в JSON файле
            mesg = {"id": base_of_messages[key].id, "title": base_of_messages[key].title, "msg": base_of_messages[key].msg, "date": base_of_messages[key].date}
            file.write(json.dumps(mesg) + '\n')


def editing_of_string(line):
    sys.stdout.write(f"\r{' '*100}\r")
    sys.stdout.flush()
    print(f"{line}\r",end="")
    sys.stdout.flush()
    line = input()
    return line


def editing_message_of_base_of_message(title_of_message):       # Функция изменяет данные заметки
    if not title_of_message:
        title_of_message = input("Введите заголовок \033[3mредактируемой\033[0m заметки : ")
    error_of_title = True  # флаг искомой заметки
    number_of_base = 0
    for key in base_of_messages: #перебираем базу в поиске заметки скорость O(n)
        if title_of_message == base_of_messages[key].title:
            number_of_base = key
            error_of_title = False  # Заметка найдена 

    if error_of_title == False: # Заметка найдена
        print('\033[1mЗаметка найдена.\033[0m')
        id = base_of_messages[number_of_base].id
        title = base_of_messages[number_of_base].title
        msg = base_of_messages[number_of_base].msg
        editing = True
        changes = False
        while editing:
            print('Выберите режим редактирования')
            choice = input('Редактировать заголовок - 1 Редактировать саму заметку - 2 Выйти из редактирования - 3  ')
            if choice == '1':
                #Редактируем заголовок заметки
                changes = True   #Появилось изменение заметки
                title = editing_of_string(title)
                
            else: 
                if choice == '2':
                    #Редактирем заметку
                    changes = True      #Появилось изменение заметки
                    msg = editing_of_string(msg)
                else:
                    if choice =='3':
                        # Прекращаем редактирование
                        if changes: # Проверяем наличие изменений
                            confim = True
                            while confim:
                                serche = input('Сохранить введеные данные: y-да/n-нет  ')
                                if serche == 'y':
                                    #Сохраняем изменения при этом старая запись удаляется, а новая добавляется в конец базы 
                                    # так поддерживается учет изменения по времени и 
                                    # вывод на экран базы всегда отсортирован по дате изменения
                                    new_number_of_base = int(base_of_messages[len(base_of_messages)].id) + 1
                                    base_of_messages.pop(number_of_base)
                                    mess= message(id, title, msg, datetime.datetime.today().strftime("%d-%m-%Y-%H.%M"))
                                    base_of_messages[new_number_of_base] = mess
                                    write_base_of_message_in_file()
                                    confim = False
                                else: 
                                    if serche == 'n':
                                        confim = False
                                    else:
                                        print('Выберите y или n')
                                        confim = True
                        editing = False
                    else:
                        print('Пожалуйста выберите один из трех вариантов')
            
    else: print('\033[31mЗаметка не найдена\033[0m')


def remove_message_of_base_of_message(title_of_message):    #Функция удаляет заметку по заголовку
    if not title_of_message:
        title_of_message = input("Введите заголовок \033[31mудаляемой\033[0m заметки :   ")
    error_of_title = True
    number_of_base = 0
    for key in base_of_messages:
        if title_of_message == base_of_messages[key].title:
            number_of_base = key
            error_of_title = False
    if not error_of_title: 
        confirmation = input('Заметка найдена. Подтвердите \033[31mудаление\033[0m данной заметки  y-да/n-нет  ')
        confim = True
        while confim:
            if confirmation == 'y':
                print('Заметка с заголовком: {} \033[31mудалена\033[0m'.format(title_of_message))
                if len(base_of_messages) == 1: # в базе одна заметка, а в файле одна строка удаление приведет к обнулению базы и удалению файла
                    if os.path.isfile('messsegDateBase.json'):
                        os.remove('messsegDateBase.json') # удаляем фаил базы
                        base_of_messages.pop(number_of_base) # удаляем заметку из базы по ключу
                else:
                    base_of_messages.pop(number_of_base)  # удаляем заметку из базы по ключу
                    write_base_of_message_in_file() # Сохраняем изменения в фаил
                confim = False
            else: 
                if confirmation == 'n':
                    print('\033[34mВнесенные изменения отменены\033[0m')
                    confim = False
                else:
                    print('Выберите y или n')
                    confim = True
    else: print('Заметка не найдена')

def create_new_message(title,msg):
    if len(base_of_messages) == 0: 
        id = 1 # Если база пута то это первая заметка
    else: 
        id = int(base_of_messages[len(base_of_messages)].id) + 1 #В базе имеются заметки создается заметка с большим id
    
    if not title: # Заметка может не иметь тела но обазана иметь заголовок(инече с ней невозможно будет работать)
        title = input('Введите заголовок заметки: ')
        msg = input('Введите текст заметки: ')
    mess = message(id, title, msg, datetime.datetime.today().strftime("%d-%m-%Y-%H.%M"))
    confirmation = input('Сохранить новую заметку? y-да/n-нет ')
    confim = True
    while confim:
        if confirmation == 'y':
            base_of_messages[len(base_of_messages) + 1] = mess # добавляем заметку в конец базы
            write_base_of_message_in_file() # Сохраняем изменения в фаил
            confim = False
        elif confirmation == 'n':
                if id == 1:
                    confirmation1 = input('\033[31mЭто первая заметка в базе, её отмена приведет в выходу из программы?\033[0m Сохранить заметку y-да/n-нет ')
                    confim1 = True
                    while confim1:
                        if confirmation1 == 'y':
                            base_of_messages[len(base_of_messages) + 1] = mess # добавляем заметку в конец базы
                            write_base_of_message_in_file() # Сохраняем изменения в фаил
                            confim = False
                            confim1 = False
                        elif confirmation == 'n':
                            exit(1)
                        else:
                            print('Выберите y или n')
                            confim1 = True
                else:
                   print('\033[31mНовая заметка не сохранена.\033[0m')
                   confim = False 
        else:
            print('Выберите y или n')
            confim = True


def help(conf):
    if conf == 1:
        print('1 - Вывести список всех заметок')
        print('2 - Создать новую заметку')
        print('3 - Редактировать заметку')
        print('4 - Удалить заметку заметку')
        print('5 - О редекторе')
        print('6 - Выйти из редактора')
    elif conf == 2:
        print('Данный редактор поддерживает работу с базой личных заметок пользователя')
        print('с использованием атрибутов командной строки при запуске программы')
        print('-а - данный атрибут добавляет новую заметку в базу')
        print('Пример: RinMessageEditor.py -a title=Заголовок заметки msg=Текст заметки')
        print('-p - данный атрибут выводит на экран все заметки имеющиеся в базе')
        print('Пример: RinMessageEditor.py -p')
        print('-e - данный атрибут редактирует заметку имеющуюся в базе с заданным заголовком')
        print('Пример: RinMessageEditor.py -e title=Заголовок редактируемой заметки')
        print('-r - данный атрибут удаляет заметку имеющуюся в базе с заданным заголовком')
        print('Пример: RinMessageEditor.py -r title=Заголовок удаляемой заметки')
    else:
        print('\033[4m\033[33m\033[44m\033[3mВас приветствует редактор личных заметок RinMessageEditor\033[0m]')
        print('')
        print('Данная программа предназначена для учета личных заметок пользователя')
        print('Она обеспечивает добавление новых заметок с дальнейшим сохранением их в базе заметок')
        print('Заметка имеет следующий формат Заголовок = Моя заметка Текст заметки = текст Дата создания заметки = дата')
        print('Их последующее редактирование')
        print('Удаление заметки с нужным заголовком')
        print('Вывод всех заметок хранящихся в базе заметок')
        print('')
        print('Так же данный редактор обеспечивает работу с использованием атрибутов командной строки при запуске программы')
        print('')
        print('-а - данный атрибут добавляет новую заметку в базу')
        print('Пример: RinMessageEditor.py -a title=Заголовок заметки msg=Текст заметки')
        print('-p - данный атрибут выводит на экран все заметки имеющиеся в базе')
        print('Пример: RinMessageEditor.py -p')
        print('-e - данный атрибут редактирует заметку имеющуюся в базе с заданным заголовком')
        print('Пример: RinMessageEditor.py -e title=Заголовок редактируемой заметки')
        print('-r - данный атрибут удаляет заметку имеющуюся в базе с заданным заголовком')
        print('Пример: RinMessageEditor.py -r title=Заголовок удаляемой заметки')
        print()
        print('Данный редактор разработан Илькиным Р.Ф.')

# MAIN OF PROGRAMM

if len(sys.argv) > 1:   # командная строка имеет более 1 атрибута 
    # При обработке консольных комманд программа работает только на выполнение данной команды и завершает работу
    # При неверно введенном командно атрибуте выводится ошибка с командой СПРАВКА(HELP) 
    if read_file_to_base_of_message() != None: # фаил с базой имеется то:
        base_of_messages.update(read_file_to_base_of_message()) # обновляем базу после чтения её из JSON файла
    if sys.argv[1] == '-a':  # добавление заметки
        print('-a')
        if len(sys.argv) < 4:  # Проверяем наличие необходимых атрибутов
            print('\033[31mНеобходимые атрибуты не заданы!\033[0m Проверьте синтаксис ввода командной строки.')
            exit(1)
        error_of_arg = True
        for num in range(2,len(sys.argv)): # Перебираем все аргументы 
            if sys.argv[num].find('title=',0,len(sys.argv[num])) != -1: #Ищем аргумент title=
                error_of_arg = False
                title_num = num
            if sys.argv[num].find('msg=',0,len(sys.argv[num])) != -1: #Ищем аргумент msg= 
                error_of_arg = False
                msg_of_arg = num
        if error_of_arg == True: # Ошибки в синтаксисе командной строки
            print('\033[31mНеобходимые атрибуты не заданы!\033[0m Проверьте синтаксис ввода командной строки.')
            exit(1)
        if title_num > msg_of_arg:
            print('\033[31mНарушен синтаксис ввода командной строки!\033[0m title= идет раньше msg=')
            exit(1)
        title = sys.argv[title_num].strip(' ')[6:len(sys.argv[title_num])]
        for num in range(title_num + 1, msg_of_arg):
            title += ' ' + sys.argv[num]
        msg = sys.argv[msg_of_arg].strip(' ')[6:len(sys.argv[msg_of_arg])]
        for num in range(msg_of_arg + 1, len(sys.argv)):
            msg += ' ' + sys.argv[num]
        print(msg)    
        create_new_message(title,msg)
        exit(1) # завершение программы
    elif sys.argv[1] == '-p':  # Вывод заметок на экран
        read_of_base_of_message()
        exit(1) # завершение программы
    elif sys.argv[1] == '-e':  # редактирование заметки
        if len(sys.argv) < 3:  # Проверяем наличие необходимых атрибутов
            print('\033[31mНеобходимые атрибуты не заданы!\033[0m Проверьте синтаксис ввода командной строки.')
            exit(1)
        error_of_arg = True
        for num in range(2,len(sys.argv)): # Перебираем все аргументы 
            if sys.argv[num].find('title=',0,len(sys.argv[num])) != -1: #Ищем аргумент title=
                error_of_arg = False
                title_num = num
        if error_of_arg == True: # Ошибки в синтаксисе командной строки
            print('\033[31mНеобходимые атрибуты не заданы!\033[0m Проверьте синтаксис ввода командной строки.')
            exit(1)
        title = sys.argv[title_num].strip(' ')[6:len(sys.argv[title_num])]
        for num in range(title_num + 1, len(sys.argv)):
            title += ' ' + sys.argv[num]
        editing_message_of_base_of_message(title)
        exit(1) # завершение программы
    elif sys.argv[1] == '-r':  # удаление заметки 
        if len(sys.argv) < 3:  # Проверяем наличие необходимых атрибутов
            print('\033[31mНеобходимые атрибуты не заданы!\033[0m Проверьте синтаксис ввода командной строки.')
            exit(1)
        error_of_arg = True
        for num in range(2,len(sys.argv)): # Перебираем все аргументы 
            if sys.argv[num].find('title=',0,len(sys.argv[num])) != -1: #Ищем аргумент title=
                error_of_arg = False
                title_num = num
        if error_of_arg == True: # Ошибки в синтаксисе командной строки
            print('\033[31mНеобходимые атрибуты не заданы!\033[0m Проверьте синтаксис ввода командной строки.')
            exit(1)
        title = sys.argv[title_num].strip(' ')[6:len(sys.argv[title_num])]
        for num in range(title_num + 1, len(sys.argv)):
            title += ' ' + sys.argv[num]
        remove_message_of_base_of_message(title)
        exit(1) # завершение программы
    elif sys.argv[1] == '-h':  # Вызов справки 
        help(2)
        exit(1) # завершение программы
    else:   # Команда нераспознана 
        print('\033[31mКоманда нераспознана! Kоманда -h вызовет справку по программе\033[0m')
        exit(1) # завершение программы
    


os.system('cls' if os.name == 'nt' else 'clear') #очистка экрана
print('\033[4m\033[46m\033[3m\033[37mВас приветствует редактор заметок RinMessageEditor V \033[33m1.0\033[0m')
print()
programm_end = False # флаг окончания работы обработчика интерфейса
while not programm_end: # тело обработчика интерфейса
    # При хзапуске програмы скачиваем базу заметок из JSON файла
    if not base_of_messages:   # проверка на наличие данных в оперативной базе, при отсутствии таковых читаем данные из файла
        if read_file_to_base_of_message() != None:
            base_of_messages.update(read_file_to_base_of_message()) # обновляем базу после чтения её из файла
        else:
            confirmation = input('\033[32mБаза пуста.\033[0m Создать новую заметку? y-да/n-нет ')
            confim = True
            while confim:
                if confirmation == 'y':
                    create_new_message(None,None)
                    confim = False
                else: 
                    if confirmation == 'n':
                        print('\033[31mРабота программы прекращена, новых заметок нет\033[0m')
                        exit(1)
                    else:
                        print('Выберите y или n')
                        confim = True

    command = input('\033[34mВведите команду (help - список команд):\033[0m')
    if command == 'help':
        help(1)
    elif command == '1':
        read_of_base_of_message()
    elif command == '2':
        create_new_message(None,None)
    elif command == '3':
        editing_message_of_base_of_message(None)
    elif command == '4':
        remove_message_of_base_of_message(None)
    elif command == '5':
        help(0)
    elif command == '6':
        programm_end = True
    else:
        print('Введите команду от 1 до 5')
    print()










