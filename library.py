class Book:

    def __init__(self, id_book, title_book, author_book, year_book, status_book='В наличии'):

        self.id = id_book
        self.title = title_book.strip()
        self.author = author_book.strip()
        self.year = year_book
        self.status = status_book

    def __str__(self):
        return f'ID: {self.id}; Название: {self.title}; Автор: {self.author}; Год: {self.year}; Статус: {self.status}'

    def set_status(self, new_status):
        """ Установка нового статуса книги """
        self.status = new_status


class Library:

    def __init__(self):
        self.count = 1

    @staticmethod
    def greet():
        """ Приветствие """

        print('Добро пожаловать в нашу библиотеку!\n'
              '1. Введите 1 для добавления новой книги\n'
              '2. Введите 2 для удаления книги\n'
              '3. Введите 3 для поиска книг\n'
              '4. Введите 4 для отображения всех книг\n'
              '5. Введите 5 для изменения статуса книги\n'
              '>> Введите 0 для выхода из библиотеки\n')

    def start(self):
        """ Интерфейс для пользователя """

        with open('count.txt', 'a+'):
            pass

        with open('count.txt', 'r') as count_file:
            f_lines = count_file.readlines()
            if f_lines:
                self.count = int(f_lines[0])

        removed_books = set()
        ids_list = set()
        with open('Library.txt', 'a+'):
            pass

        with open('Library.txt', 'r') as lib_file:
            book_list = []

            for book in lib_file.readlines():
                split_data = book.split("; ")
                id_book = int(split_data[0][3:])
                name_ = split_data[1][10:].strip()
                author_ = split_data[2][7:].strip()
                year_ = int(split_data[3][5:].strip())
                status_ = split_data[4][7:].strip()

                new_book = Book(id_book, name_, author_, year_, status_)
                book_list.append(new_book)
                ids_list.add(new_book.id)

        while True:
            try:
                input_data = input('Команда: ')
            except KeyboardInterrupt:
                input_data = '0'

            if input_data == '0':
                self.save(book_list, removed_books)
                print('Досвидания!')
                exit(0)

            if input_data not in ['1', '2', '3', '4', '5']:
                print(f'>> Введите корректную команду.')
                continue

            if input_data == '1':
                title, author, year = self.get_user_data()
                self.add(title, author, year, book_list, ids_list, removed_books)

            elif input_data == '2':
                book_id = self.get_remove_id(ids_list, removed_books)
                if book_id != 0:
                    self.delete(book_id, book_list, removed_books)

            elif input_data == '3':
                book_name, book_author, book_year = self.get_user_data(search=True)
                self.search(book_name, book_author, book_year, book_list, removed_books)

            elif input_data == '4':
                self.list(book_list, removed_books)

            elif input_data == '5':
                id_book, book_status = self.get_new_status(ids_list, removed_books)
                if id_book is not None:
                    self.change_status(id_book, book_status, book_list, removed_books)

            if input_data == '1' or input_data == '2':
                with open('count.txt', 'w') as count_file:
                    count_file.write(str(self.count))

    def add(self, title_book, author_book, year_book, b_list, id_list, remove_list):
        """ Добавление новой книги """

        new_id = self.count
        new_book = Book(new_id, title_book, author_book, year_book)
        b_list.append(new_book)
        id_list.add(new_book.id)

        self.count += 1

        print(f'>> Добавлена новая книга: {new_book}')
        self.save(b_list, remove_list)

    def delete(self, id_, b_list, remove_list):
        """ Удаление книги """

        remove_list.add(id_)
        print('>> Книга удалена.')
        self.save(b_list, remove_list)

    def search(self, b_name, b_author, b_year, b_list, remove_list):
        """ Поиск книг """

        if not b_list:
            print('По вашему запросу ничего не найдено.')
            return

        b_name = b_name.strip().lower()
        b_author = b_author.strip().lower()
        result_exist = 0
        if b_name == '' and b_author == '' and b_year == 0:
            result_exist = 1
            self.list(b_list, remove_list)
        else:
            for book_line in b_list:
                if book_line.id in remove_list:
                    continue

                name_match = True if b_name != '' and b_name in book_line.title.lower() else False
                author_match = True if b_author != '' and b_author in book_line.author.lower() else False
                year_match = True if b_year == book_line.year else False

                if b_name != '' and b_author == '' and b_year == 0:
                    match = name_match
                elif b_author != '' and b_name == '' and b_year == 0:
                    match = author_match
                elif b_year != 0 and b_name == '' and b_author == '':
                    match = year_match
                elif b_name != '' and b_author != '' and b_year == 0:
                    match = name_match and author_match
                elif b_name != '' and b_year != 0 and b_author == '':
                    match = name_match and year_match
                elif b_author != '' and b_year != 0 and b_name == '':
                    match = author_match and year_match
                else:
                    match = name_match and author_match and year_match

                if match:
                    print(book_line)
                    result_exist = 1

        if result_exist == 0:
            print('По вашему запросу ничего не найдено.')

    @staticmethod
    def list(b_list, remove_list):
        """ Вывод списка всех книг """

        if not b_list:
            print('Список книг пуст.')
            return

        for book_line in b_list:
            if book_line.id not in remove_list:
                print(book_line)

    def change_status(self, id_, new_status, b_list, remove_list):
        """ Изменение статуса книги """

        for book_line in b_list:
            if book_line.id == id_:
                book_line.set_status(new_status)
                print('Статус изменен')
                self.save(b_list, remove_list)
                return

    @staticmethod
    def save(b_list, remove_list):
        """ Сохранение данных """

        with open('Library.txt', 'w') as lib_file:
            for book_line in b_list:
                if book_line.id in remove_list:
                    continue

                lib_file.write(book_line.__str__())
                if book_line.__str__().find('\n') == -1:
                    lib_file.write('\n')

    @staticmethod
    def get_user_data(search=False):
        """ Получение данных от пользователя """

        while True:
            if not search:
                user_data = input('>> Введите через ";" Название, Автора и Год: ').split(';')
                if len(user_data) != 3:
                    print('>> Введите корректные данные.')
                    continue

                title, author, year = user_data
                title.strip()
                author.strip()
                year.strip()
                digit_in_str = any(char.isdigit() for char in author)
                if digit_in_str:
                    print('>> Некорректно введен автор.')
                    continue

                try:
                    year = int(year)
                except ValueError:
                    print('>> Некорректно введен год.')
                    continue
                break

            else:
                while True:
                    title = input('>> Введите название книги: ')
                    author = input('>> Введите автора книги: ')
                    year = input('>> Введите год книги: ')
                    break

                try:
                    year = int(year)
                except ValueError:
                    year = 0
                break

        return title, author, year

    @staticmethod
    def get_remove_id(ids_list, removed_books):
        """ Получение ID от пользователя """

        id_book = 0
        while True:
            try:
                id_book = int(input('>> Введите ID книги для удаления: ').replace(" ", ""))
            except ValueError:
                print('ID должен быть числом.')
                break
            break

        if id_book not in ids_list or id_book in removed_books:
            print('Книга с данным ID отсутствует.')
            return 0

        return id_book

    @staticmethod
    def get_new_status(ids_list, removed_books):
        """ Получение нового статуса от пользователя """

        while True:
            id_book = input('>> Введите ID книги: ').replace(" ", "")
            try:
                id_book = int(id_book)
            except ValueError:
                print('ID должен быть числом.')
                continue

            if id_book not in ids_list or id_book in removed_books:
                print('Книга с данным ID отсутствует.')
                return None, ''

            book_status = input('>> Введите новый статус (В наличии/Выдана): ').strip()
            if book_status.strip() not in ['В наличии', 'Выдана']:
                print('Введите корректный статус.')
                continue

            return id_book, book_status


if __name__ == "__main__":
    new_lib = Library()
    new_lib.greet()
    new_lib.start()
