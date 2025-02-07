import pytest
from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

# пример теста:
# в тестах обязательно указываю префикс test_
# дальше идет название метода, который тестирую add_new_book_
# затем, что тестирую, например, add_two_books - добавление двух книг

    def test_add_new_book(self,collector):  # проверяю добавление одной книги в словарь без указания жанра
        collector.add_new_book("Хоббит")  # присвоила книге название
        assert "Хоббит" in collector.books_genre  # убедилась, что моя книга есть в словаре
        assert collector.books_genre["Хоббит"] == ""  # убедилась, что жанр книги не указан

    def test_add_new_book_duplicate(self,collector):
        collector.add_new_book("Король Лев")  # проверяю добавление дубликата книги в словарь
        collector.add_new_book("Король Лев")
        assert len(collector.books_genre) == 1  # убедилась, что такое название в словаре одно

    def test_add_new_book_add_two_books(self,collector):
        collector.add_new_book("Макбет")   # добавляю две разные книги
        collector.add_new_book("Над пропастью во ржи")
        # проверяем, что добавилось именно две
        assert len(collector.books_genre) == 2

    @pytest.mark.parametrize(  # добавила параметризацию для проверки количества символов в названии книги
        "name, expected_result",
        [
            ("Властелин колец", True),  # название содержит не более 40-ка символов
            ("Бу!", True),  # название содержит три символа
            ("Никогда не ешь один, потому что тебя украдут Злые Духи", False),
            # название книги содержит более 40-ка символов
            ("", False),  # книга без названия
        ],
    )
    def test_add_new_book_parametrized(self,collector, name, expected_result):
        collector.add_new_book(name)  # пробую добавить книгу
        assert (name in collector.books_genre) == expected_result  # убедилась, что количество символов
    # в названиях книг соответствуют ожидаемому результату

    @pytest.mark.parametrize("genre", ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"])
    # добавила параметризацию для проверки жанра книги
    def test_set_book_genre(self, collector, genre): # установить жанр книги
        collector.add_new_book("Финансист")  # создала книгу
        collector.set_book_genre("Финансист", genre)  # установила жанр
        assert collector.get_book_genre("Финансист") == genre  # метод правильно устанавливает жанр книг

    def test_set_book_genre_invalid(self, collector): # установить посторонний жанр (не из списка доступных жанров)
        collector.add_new_book("Титан")  # создала книгу
        collector.set_book_genre("Титан", "InvalidGenre") # установила несуществующий в списке жанр
        assert collector.get_book_genre("Титан") == "" # невозможно назначать книгам посторонние жанры

    def test_get_book_genre(self, collector):  # проверить жанр книги по имени
        collector.add_new_book("Стоик")  # создала книгу
        collector.set_book_genre("Стоик", "Фантастика")  # назначила жанр из списка
        assert collector.get_book_genre("Стоик") == "Фантастика"  # жанр соответствует названию книги

    def test_get_books_with_specific_genre(self, collector):  # получить книги определённого жанра
        collector.add_new_book("Вини Пух") # создала первую книгу
        collector.set_book_genre("Вини Пух", "Мультфильмы") # назначила жанр из списка
        collector.add_new_book("Трое в лодке") # создала вторую книгу
        collector.set_book_genre("Трое в лодке", "Комедии") # назначила жанр из списка
        result = collector.get_books_with_specific_genre("Мультфильмы") # попросила вывести книгу жанра "Фантастика"
        assert result == ["Вини Пух"] # получила название нужной книги

    def test_get_books_genre(self, collector):  # вывести текущий словарь
        collector.add_new_book("Нет больше идей") # создала книгу
        collector.set_book_genre("Нет больше идей", "Ужасы") # назначила жанр из списка
        books = collector.get_books_genre() # книги находятся в словаре
        assert "Нет больше идей" in books # моя назначенная книга находится в словаре среди других книг
        assert books["Нет больше идей"] == "Ужасы" # моя назначенная книга в словаре соответствует назначенному ей жанру

    def test_get_books_for_children(self, collector):  # получить книги без возрастного ограничения
        collector.add_new_book("Красная Шапочка") # создала книгу
        collector.set_book_genre("Красная Шапочка", "Мультфильмы")  # установила жанр без возрастного ограничения
        collector.add_new_book("Что-то из Агаты Кристи") # создала ещё одну книгу
        collector.set_book_genre("Что-то из Агаты Кристи", "Детективы") # установила жанр 18+
        result = collector.get_books_for_children() # хочу получить детские книги
        assert result == ["Красная Шапочка"] # получаю книги без возрастного ограничения

    def test_add_book_in_favorites_success(self, collector): # успешное добавление книги в избранное
        collector.add_new_book("Война и мир") # создала книгу
        collector.set_book_genre("Война и мир", "Фантастика")  # назначила жанр из списка
        collector.add_book_in_favorites("Война и мир") # добавила книгу в избранное
        assert "Война и мир" in collector.favorites # книга успешно добавлена в избранное

    def test_add_book_in_favorites_not_in_books_genre(self, collector): # проверка добавления книги в список пользователя
        # прежде, чем он её добавит в избранное
        collector.add_book_in_favorites("Пиши, сокращай")
        assert "Пиши, сокращай" not in collector.favorites # книга добавлена в список пользователя

    def test_add_book_in_favorites_duplicate(self, collector): # невозможно повторно добавить книгу в избранное
        collector.add_new_book("Кради как художник")  # создала книгу
        collector.set_book_genre("Кради как художник", "Комедии")  # назначила жанр из списка
        collector.add_book_in_favorites("Кради как художник") # добавила книгу в избранное
        collector.add_book_in_favorites("Кради как художник") # добавила книгу в избранное повторно
        assert collector.favorites.count("Кради как художник") == 1 # книга добавляется только один раз

    def test_delete_book_from_favorites(self, collector):  # удаляю книгу из избранного
        collector.add_new_book("Ясно, понятно") # создала книгу
        collector.set_book_genre("Ясно, понятно", "Фантастика") # назначила жанр из списка
        collector.add_book_in_favorites("Ясно, понятно") # добавила книгу в избранное
        collector.delete_book_from_favorites("Ясно, понятно") # удалила книгу из избранног
        assert "Ясно, понятно" not in collector.favorites # книга больше не в избранных

    def test_get_list_of_favorites_books(self, collector):  # получить список избранных книг
        collector.add_new_book("Мужские правила") # создала книгу
        collector.set_book_genre("Мужские правила", "Ужасы") # назначила жанр из списка
        collector.add_book_in_favorites("Мужские правила") # добавила книгу в избранное
        assert collector.get_list_of_favorites_books() == ["Мужские правила"] # проверила список избранного и нашла свою книгу в нём
