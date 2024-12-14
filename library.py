COUNT = 1


class Book:

    def __init__(self, title_book, author_book, year_book):

        global COUNT
        new_id = COUNT

        self.id = new_id
        self.title = title_book.strip()
        self.author = author_book.strip()
        self.year = year_book
        self.status = 'В наличии'

    def __str__(self):
        return f'ID: {self.id}, Название: <<{self.title}>>, Автор: {self.author}, Год: {self.year}, Статус: {self.status}'


class Library:

    @staticmethod
    def greet():
        print(f'Добро пожаловать в нашу библиотеку!\n'
              f'1. Введите 1 для добавления новой книги\n'
              f'2. Введите 2 для удаления книги\n'
              f'3. Введите 3 для поиска книг\n'
              f'4. Введите 4 для отображения всех книг\n'
              f'5. Введите 5 для изменения статуса книги\n'
              f'>> Введите 0 для выхода из библиотеки\n')

    def start(self):
        global COUNT

        with open('count.txt', 'a+') as file:
            pass

        with open('count.txt', 'r') as count_file:
            f_lines = count_file.readlines()
            if f_lines:
                COUNT = int(f_lines[0])

        removed_books = []
        ids_list = []
        with open('Library.txt', 'a+') as new_file:
            pass

        with open('Library.txt', 'r') as lib_file:
            book_list = lib_file.readlines()
            for book in book_list:
                id_book = book.split(", ")[0][3:]
                ids_list.append(int(id_book))

        with open('Library.txt', 'w') as lib_file:
            while True:
                try:
                    input_data = input('Команда: ')
                except KeyboardInterrupt:
                    input_data = '0'

                if input_data == '0':
                    self.quit(lib_file, book_list, removed_books)
                    exit(0)

                if input_data not in ['1', '2', '3', '4', '5']:
                    print(f'>> Введите корректную команду.')
                    continue

                if input_data == '1':
                    while True:
                        try:
                            user_data = input('>> Введите через запятую Название, Автора и Год: ').split(',')
                        except KeyboardInterrupt:
                            self.quit(lib_file, book_list, removed_books)

                        if len(user_data) != 3:
                            print(f'>> Введите корректные данные.')
                            continue
                        elif len(user_data) == 3:
                            title, author, year = user_data
                            title.strip()
                            author.strip()
                            year.strip()
                            digit_in_str = any(char.isdigit() for char in author)
                            if digit_in_str:
                                print(f'>> Некорректно введен автор.')
                                continue

                            try:
                                year = int(year)
                            except ValueError:
                                print(f'>> Некорректно введен год.')
                                continue
                            break

                    self.add(title, author, year, book_list, ids_list)

                elif input_data == '2':
                    id_book = 0
                    while True:
                        try:
                            id_book = int(input('>> Введите ID книги для удаления: ').replace(" ", ""))
                        except ValueError:
                            print('ID должен быть числом.')
                            break
                        break

                    if id_book == 0:
                        continue
                    elif id_book in ids_list:
                        self.delete(id_book, removed_books)
                    else:
                        print('Книга с данным ID отсутствует.')

                elif input_data == '3':
                    book_name = ''
                    book_author = ''
                    book_year = ''
                    while True:
                        try:
                            book_name = input('>> Введите название книги: ')
                            book_author = input('>> Введите автора книги: ')
                            book_year = input('>> Введите год книги: ')
                        except KeyboardInterrupt:
                            self.quit(lib_file, book_list, removed_books)
                        break

                    try:
                        book_year = int(book_year)
                    except ValueError:
                        book_year = 0

                    self.search(book_name, book_author, book_year, book_list)

                elif input_data == '4':
                    self.list(book_list)

                elif input_data == '5':
                    id_book = ''
                    book_status = ''
                    while True:
                        try:
                            id_book = input('>> Введите ID книги: ').strip().replace(" ", "")
                            book_status = input('>> Введите новый статус (В наличии/Выдана): ').strip()
                        except KeyboardInterrupt:
                            self.quit(lib_file, book_list, removed_books)

                        try:
                            id_book = int(id_book)
                        except ValueError:
                            print('ID должен быть числом.')
                            continue

                        if book_status.strip() not in ['В наличии', 'Выдана']:
                            print('Введите корректный статус.')
                            continue
                        if id_book not in ids_list:
                            print('Книга с данным ID отсутствует.')
                        break

                    self.change_status(id_book, book_status, book_list)

                if input_data == '1' or input_data == '2':
                    with open('count.txt', 'w') as count_file:
                        count_file.write(str(COUNT))

    @staticmethod
    def add(title_book, author_book, year_book, b_list, id_list):

        global COUNT
        new_book = Book(title_book, author_book, year_book)
        b_list.append(new_book.__str__())
        id_list.append(new_book.id)

        COUNT += 1

        print(f'>> Добавлена новая книга.')
        print(new_book)

    @staticmethod
    def delete(id_, remove_list):
        remove_list.append(id_)
        print(f'>> Книга удалена.')

    @staticmethod
    def search(b_name, b_author, b_year, b_list):
        b_name.strip()
        b_author.strip()
        result_exist = 0
        if b_name == '' and b_author == '' and b_year == 0:
            for book_line in b_list:
                print(book_line)
        else:
            for book_line in b_list:
                book_split = book_line.split(',')
                name_ = book_split[1][11:].strip()
                author_ = book_split[2][8:].strip()
                year_ = int(book_split[3][6:].strip())

                name_match = True if b_name.lower() in name_.lower() and b_name != '' else False
                author_match = True if b_author.lower() in author_.lower() and b_author != '' else False
                year_match = True if year_ == b_year else False

                if name_match or author_match or year_match:
                    print(book_line[:-1])
                    result_exist = 1

        if result_exist == 0:
            print('По вашему запросу ничего не найдено.')

    @staticmethod
    def list(b_list):
        for book_line in b_list:
            print(book_line[:-1])

    @staticmethod
    def change_status(id_, new_status, b_list):
        for book_line in b_list:
            b_split = book_line.split(", ")
            b_id = int(b_split[0][3:].replace(" ", ""))
            b_status = b_split[4][8:].strip()
            if b_id == id_:
                book_line.replace(f'Статус: {b_status}', f'Статус: {new_status}')
        print('Статус изменен')

    @staticmethod
    def quit(file_, b_list, remove_list):
        for book_line in b_list:
            id_ = book_line.split(", ")[0][3:].replace(" ", "")
            if int(id_) not in remove_list:
                file_.write(book_line)
                if book_line.find('\n') == -1:
                    file_.write('\n')
        file_.truncate()


if __name__ == "__main__":
    new_lib = Library()
    new_lib.greet()
    new_lib.start()


