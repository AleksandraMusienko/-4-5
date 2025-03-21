import sqlite3
import os

# Путь к файлу базы данных SQLite
db_file = 'library.db'

# ****************************
# эта команда нужна для отладки (для повторных запусков)
# Если файл БД уже существует, то удалить существующий файл БД, 
# чтобы предотвратить повторную запись тех же самых данных
if os.path.isfile(db_file):
    os.remove(db_file)
# **************************** 

# Проверка существования файла базы данных
if not os.path.isfile(db_file):
    # Если файл базы данных не существует, создаем его и подключаемся
    conn = sqlite3.connect(db_file)

    # Создание объекта курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Создание таблиц и внесение данных в базу данных

    # Создание таблицы Genre
    cursor.execute('''CREATE TABLE IF NOT EXISTS Genre (
        GenreID INTEGER PRIMARY KEY,
        GenreName TEXT NOT NULL UNIQUE,
        Description TEXT
    )''')

    # Создание таблицы Author
    cursor.execute('''CREATE TABLE IF NOT EXISTS Author (
        AuthorID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        BirthYear INTEGER CHECK (BirthYear <= 2010),
        Nationality TEXT
    )''')

    # Создание таблицы Book
    cursor.execute('''CREATE TABLE IF NOT EXISTS Book (
        BookID INTEGER PRIMARY KEY,
        Genre INTEGER NOT NULL,
        Title TEXT NOT NULL,
        PublicationYear INTEGER NOT NULL,
        ISBN TEXT UNIQUE,
        FOREIGN KEY (Genre) REFERENCES Genre(GenreID)
    )''')

    # Создание связующей таблицы BookAuthor
    cursor.execute('''CREATE TABLE IF NOT EXISTS BookAuthor (
        BookAuthorID INTEGER PRIMARY KEY AUTOINCREMENT,  -- автоинкрементный ID
        Author INTEGER NOT NULL,                         -- внешний ключ на таблицу Author
        Book INTEGER NOT NULL,                           -- внешний ключ на таблицу Book
        FOREIGN KEY (Author) REFERENCES Author(AuthorID),  -- ссылка на таблицу Author
        FOREIGN KEY (Book) REFERENCES Book(BookID)        -- ссылка на таблицу Book
    )''')
    # Создание таблицы BookInstance 
    cursor.execute('''CREATE TABLE IF NOT EXISTS BookInstance (
        BookInstanceID INTEGER PRIMARY KEY,
        Book INTEGER NOT NULL,
        InstanceNumber INTEGER NOT NULL DEFAULT 1,
        InstanceStatus TEXT,
        Condition TEXT,
        FOREIGN KEY (Book) REFERENCES Book(BookID)
    )''')

    # Сохранение изменений 
    conn.commit()

else:
    # Если файл базы данных существует, просто подключаемся к нему
    conn = sqlite3.connect(db_file)
    # и создаем объект курсор для выполнения SQL-запросов
    cursor = conn.cursor()

# Внесение множества данных в таблицу Author
authors_data = [
    ("М. Горький", 1868, "русский"),
    ("А. Чехов", 1860, "русский"), 
    ("Т. Шевченко", 1814, "украинец"),
    ("Л. Толстой", 1828, "русский"),
    ("И. Ильф", 1897, "еврей"),
    ("Е. Петров", 1903, "русский")
]
cursor.executemany("INSERT INTO Author (Name, BirthYear, Nationality) VALUES (?, ?, ?)", authors_data)

# Добавление жанров
genres_data = [
    ("роман", "Произведение прозаического жанра, длинное по объему"),
    ("драма", "Произведение, предназначенное для театрального исполнения"),
    ("повесть", "Произведение прозаического жанра, короткое по объему"),
    ("поэма", "Произведение лиро-эпической или эпической формы, чаще всего в стихотворной форме")
]
cursor.executemany("INSERT INTO Genre (GenreName, Description) VALUES (?, ?)", genres_data)

# Добавление книг
books_data = [
    (1, "Мать", 1996, "978-1234567890"),
    (2, "На дне", 1992, "978-0987654321"),
    (3, "Каштанка", 2017, "978-5432167890"),
    (3, "Вишневый сад", 2017, "978-6432167890"),
    (4, "Гайдамаки", 1930, "978-2345678901"),
    (1, "Война и мир", 2025, "978-3456789012"),
    (1, "Двенадцать стульев", 1828, "978-22334455"),
    (1, "Золотой теленок", 1833, "978-33445522")
]
cursor.executemany("INSERT INTO Book (Genre, Title, PublicationYear, ISBN) VALUES (?, ?, ?, ?)", books_data)

# Добавление экземпляров
instances_data = [
    (1, 1, "Доступен", "Хорошее"),
    (1, 2, "Доступен", "Хорошее"),
    (2, 1, "Доступен", "Хорошее"),
    (2, 2, "Доступен", "Хорошее"),
    (3, 1, "Доступен", "Отличное"),
    (3, 2, "Доступен", "Отличное"),
    (4, 1, "Доступен", "Хорошее"),
    (5, 1, "Доступен", "Удовлетворительное"),
    (7, 1, "Доступен", "Отличное"),
    (8, 1, "Доступен", "Отличное")
]
cursor.executemany("INSERT INTO BookInstance (Book, InstanceNumber, InstanceStatus, Condition) VALUES (?, ?, ?, ?)", instances_data)

# Заполнение связующей таблицы BookAuthor 
book_authors_data = [
    (1, 1),  # "М. Горький"(AuthorID = 1) - "Мать"(AuthorID = 1)
    (1, 2),  # "М. Горький"(AuthorID = 1) - "На дне"(AuthorID = 2)
    (2, 3),  # "А. Чехов"(AuthorID = 2) - "Каштанка"(AuthorID = 3)
    (2, 4),  # "А. Чехов"(AuthorID = 2) - "Вишневый сад"(AuthorID = 4)
    (3, 5),  # "Т. Шевченко"(AuthorID = 3) - "Гайдамаки"(AuthorID = 5)
    (4, 6),  # "Л. Толстой"(AuthorID = 4) - "Война и мир"(AuthorID = 6)
    (5, 7),  # "И. Ильф"(AuthorID = 5) - "Двенадцать стульев"(AuthorID = 7)
    (6, 7),  # "Е. Петров"(AuthorID = 6) - "Двенадцать стульев"(AuthorID = 7)
    (5, 8),  # "И. Ильф"(AuthorID = 4) - "Золотой теленок"(AuthorID = 8)
    (6, 8)   # "Е. Петров"(AuthorID = 6) - "Золотой теленок"(AuthorID = 8)
]
# Вставляем данные в таблицу BookAuthor
cursor.executemany("INSERT INTO BookAuthor (Author, Book) VALUES (?, ?)", book_authors_data)

# Сохранение изменений 
conn.commit()

# *******************************
# Запросы на извлечение данных
# *******************************

# Запрос для получения списка книг с их авторами
cursor.execute('''
SELECT Book.Title, Author.Name
FROM Book
JOIN BookAuthor ON Book.BookID = BookAuthor.Book
JOIN Author ON BookAuthor.Author = Author.AuthorID
''')
results = cursor.fetchall()
print("*** Полный список, 2 столбца: ")
if results:
    for row in results:
        print(f"Книга: {row[0]}, Автор: {row[1]}")
else:
    print("Нет данных для вывода.")
print()

# !!! ЗАДАНИЕ ВЫПОЛНЕНО
# Изменить запрос и выдать по 2 поля из таблицы Autor и из таблицы Book
cursor.execute('''
SELECT Author.Name, Author.Nationality, Book.Title, Book.PublicationYear
FROM Book
JOIN BookAuthor ON Book.BookID = BookAuthor.Book
JOIN Author ON BookAuthor.Author = Author.AuthorID
''')
results = cursor.fetchall()
print("*** Полный список, 4 столбца: ")
if results:
    for row in results:
        print(f"Автор: {row[0]}, Национальность: {row[1]}, Книга: {row[2]}, Год публикации: {row[3]}")
else:
    print("Нет данных для вывода.")
print()

# !!! ЗАДАНИЕ ВЫПОЛНЕНО
# Написать запрос, который выводит всех авторов и список их книг в одной строке
cursor.execute('''
SELECT Author.Name, GROUP_CONCAT(Book.Title, ', ') AS Books
FROM Author
JOIN BookAuthor ON Author.AuthorID = BookAuthor.Author
JOIN Book ON BookAuthor.Book = Book.BookID
GROUP BY Author.AuthorID
ORDER BY Author.Name
''')
results = cursor.fetchall()
print("*** Авторы и их книги: ")
if results:
    for row in results:
        print(f"Автор: {row[0]}, Книги: {row[1]}")
else:
    print("Нет данных для вывода.")
print()

# !!! ЗАДАНИЕ ВЫПОЛНЕНО
# Написать запрос, который получает число книг и выводит авторов, которые написали заданное количество книг
num_books = 2  # Пример: ищем авторов, написавших 2 книги
cursor.execute('''
SELECT Author.Name, GROUP_CONCAT(Book.Title, ', ') AS Books, COUNT(Book.BookID) AS BookCount
FROM Author
JOIN BookAuthor ON Author.AuthorID = BookAuthor.Author
JOIN Book ON BookAuthor.Book = Book.BookID
GROUP BY Author.AuthorID
HAVING BookCount = ?
''', (num_books,))
results = cursor.fetchall()
print(f"*** Авторы, написавшие {num_books} книги: ")
if results:
    for row in results:
        print(f"Автор: {row[0]}, Книги: {row[1]}")
else:
    print("Нет данных для вывода.")
print()

# Закрытие соединения с базой данных
conn.close()