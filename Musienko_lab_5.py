import sqlite3
import os

# Путь к файлу базы данных SQLite
db_file = 'library.db'

# Удаление файла базы данных, если он существует (для отладки)
if os.path.isfile(db_file):
    os.remove(db_file)

# Подключение к базе данных и создание таблиц
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''CREATE TABLE IF NOT EXISTS Genre (
    GenreID INTEGER PRIMARY KEY,
    GenreName TEXT NOT NULL UNIQUE,
    Description TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Author (
    AuthorID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    BirthYear INTEGER CHECK (BirthYear <= 2010),
    Nationality TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Book (
    BookID INTEGER PRIMARY KEY,
    Genre INTEGER NOT NULL,
    Title TEXT NOT NULL,
    PublicationYear INTEGER NOT NULL,
    ISBN TEXT UNIQUE,
    FOREIGN KEY (Genre) REFERENCES Genre(GenreID)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS BookAuthor (
    BookAuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
    Author INTEGER NOT NULL,
    Book INTEGER NOT NULL,
    FOREIGN KEY (Author) REFERENCES Author(AuthorID),
    FOREIGN KEY (Book) REFERENCES Book(BookID)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS BookInstance (
    BookInstanceID INTEGER PRIMARY KEY,
    Book INTEGER NOT NULL,
    InstanceNumber INTEGER NOT NULL DEFAULT 1,
    InstanceStatus TEXT,
    Condition TEXT,
    FOREIGN KEY (Book) REFERENCES Book(BookID)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Reader (
    ReaderID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL,
    ReaderStatus INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Rental (
    RentalID INTEGER PRIMARY KEY,
    Reader INTEGER NOT NULL,
    Instance INTEGER NOT NULL,
    DateRented TEXT NOT NULL,
    DateReturned TEXT,
    FOREIGN KEY (Reader) REFERENCES Reader(ReaderID),
    FOREIGN KEY (Instance) REFERENCES BookInstance(BookInstanceID)
)''')

# Внесение данных
authors_data = [
    ("М. Горький", 1868, "русский"),
    ("А. Чехов", 1860, "русский"),
    ("Т. Шевченко", 1814, "украинец"),
    ("Л. Толстой", 1828, "русский"),
    ("И. Ильф", 1897, "еврей"),
    ("Е. Петров", 1903, "русский")
]
cursor.executemany("INSERT INTO Author (Name, BirthYear, Nationality) VALUES (?, ?, ?)", authors_data)

genres_data = [
    ("роман", "Произведение прозаического жанра, длинное по объему"),
    ("драма", "Произведение, предназначенное для театрального исполнения"),
    ("повесть", "Произведение прозаического жанра, короткое по объему"),
    ("поэма", "Произведение лиро-эпической или эпической формы, чаще всего в стихотворной форме")
]
cursor.executemany("INSERT INTO Genre (GenreName, Description) VALUES (?, ?)", genres_data)

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

instances_data = [
    (1, 1, "Выдан", "Хорошее"),
    (1, 2, "Доступен", "Хорошее"),
    (2, 1, "Доступен", "Хорошее"),
    (2, 2, "Доступен", "Хорошее"),
    (3, 1, "Доступен", "Отличное"),
    (3, 2, "Доступен", "Отличное"),
    (4, 1, "Доступен", "Хорошее"),
    (5, 1, "Доступен", "Удовлетворительное"),
    (6, 1, "Выдан", "Отличное"),
    (7, 1, "Доступен", "Отличное"),
    (8, 1, "Доступен", "Отличное")
]
cursor.executemany("INSERT INTO BookInstance (Book, InstanceNumber, InstanceStatus, Condition) VALUES (?, ?, ?, ?)", instances_data)

book_authors_data = [
    (1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 7), (5, 8), (6, 8)
]
cursor.executemany("INSERT INTO BookAuthor (Author, Book) VALUES (?, ?)", book_authors_data)

readers_data = [
    ("Иванов", "ivanov@example.com", 1),
    ("Петров", "petrov@example.com", 1)
]
cursor.executemany("INSERT INTO Reader (Name, Email, ReaderStatus) VALUES (?, ?, ?)", readers_data)

rental_data = [
    (2, 1, '2023-03-15', '2023-05-15'),
    (1, 1, '2024-02-01', None),
    (2, 9, '2024-02-01', None)
]
cursor.executemany("INSERT INTO Rental (Reader, Instance, DateRented, DateReturned) VALUES (?, ?, ?, ?)", rental_data)

# Сохранение изменений
conn.commit()

# Задание 1: Книги, которые выданы (не возвращены)
cursor.execute('''
    SELECT b.Title, bi.InstanceNumber, r.Name, ra.DateRented
    FROM Rental ra
    JOIN BookInstance bi ON ra.Instance = bi.BookInstanceID
    JOIN Book b ON bi.Book = b.BookID
    JOIN Reader r ON ra.Reader = r.ReaderID
    WHERE ra.DateReturned IS NULL
''')

issued_books = cursor.fetchall()

if issued_books:
    print("Книги, которые выданы (не возвращены):")
    for book in issued_books:
        title, instance, reader_name, date_rented = book
        print(f"Книга: {title}, Экземпляр: {instance}, Читатель: {reader_name}, Дата аренды: {date_rented}")
else:
    print("Нет книг, которые выданы (не возвращены).")
print()

# Задание 2: Книги, которые взяли и вернули
cursor.execute('''
    SELECT b.Title, bi.InstanceNumber, r.Name, ra.DateRented, ra.DateReturned
    FROM Rental ra
    JOIN BookInstance bi ON ra.Instance = bi.BookInstanceID
    JOIN Book b ON bi.Book = b.BookID
    JOIN Reader r ON ra.Reader = r.ReaderID
    WHERE ra.DateReturned IS NOT NULL
''')

returned_books = cursor.fetchall()

if returned_books:
    print("Книги, которые взяли и вернули:")
    for book in returned_books:
        title, instance, reader_name, date_rented, date_returned = book
        print(f"Книга: {title}, Экземпляр: {instance}, Читатель: {reader_name}, Дата аренды: {date_rented}, Дата возврата: {date_returned}")
else:
    print("Нет книг, которые взяли и вернули.")
print()

# Задание 3: Кто арендовал книгу и когда
book_title = 'Мать'
instance_number = 1

cursor.execute('''
    SELECT rd.Name, ra.DateRented, ra.DateReturned
    FROM Rental ra
    JOIN BookInstance bi ON ra.Instance = bi.BookInstanceID
    JOIN Book b ON bi.Book = b.BookID
    JOIN Reader rd ON ra.Reader = rd.ReaderID
    WHERE b.Title = ? AND bi.InstanceNumber = ?
''', (book_title, instance_number))

rented_info = cursor.fetchall()

if rented_info:
    print(f"Читатели, которые арендовали книгу '{book_title}' (Экземпляр {instance_number}):")
    for reader in rented_info:
        reader_name, date_rented, date_returned = reader
        print(f"Читатель: {reader_name}, Дата аренды: {date_rented}, Дата возврата: {date_returned}")
else:
    print(f"Нет читателей, которые арендовали книгу '{book_title}' (Экземпляр {instance_number}).")
print()

# Транзакция для возврата книги
reader_id = 1  # ID читателя
book_instance_id = 1  # ID экземпляра книги
return_date = '2024-02-10'  # Дата возврата

try:
    # Начинаем транзакцию
    conn.execute('BEGIN TRANSACTION')

    # Проверка, существует ли аренда для данного читателя и экземпляра книги
    cursor.execute(''' 
        SELECT r.RentalID 
        FROM Rental r 
        WHERE r.Reader = ? AND r.Instance = ? AND r.DateReturned IS NULL
    ''', (reader_id, book_instance_id))
    rental_record = cursor.fetchone()

    # Если аренда не найдена, откатываем транзакцию
    if not rental_record:
        print(f"Читатель с ID {reader_id} не арендовал этот экземпляр книги.")
        conn.rollback()
    else:
        # 1. Обновление записи о возврате книги
        cursor.execute(''' 
            UPDATE Rental 
            SET DateReturned = ? 
            WHERE RentalID = ?
        ''', (return_date, rental_record[0]))

        # 2. Проверка, арендовал ли читатель другие книги
        cursor.execute(''' 
            SELECT COUNT(*) 
            FROM Rental 
            WHERE Reader = ? AND DateReturned IS NULL
        ''', (reader_id,))
        active_rentals = cursor.fetchone()[0]

        # 3. Если у читателя нет других арендованных книг, обновляем его статус на "неактивный"
        if active_rentals == 0:
            cursor.execute(''' 
                UPDATE Reader 
                SET ReaderStatus = 2 
                WHERE ReaderID = ?
            ''', (reader_id,))

        # Завершаем транзакцию
        conn.commit()
        print(f"Читатель {reader_id} успешно вернул книгу с экземпляром {book_instance_id}.")

except Exception as e:
    # Если произошла ошибка, откатываем изменения
    print(f"Произошла ошибка: {e}")
    conn.rollback()

# Закрытие соединения
conn.close()
