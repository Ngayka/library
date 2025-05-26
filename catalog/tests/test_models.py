from django.contrib.auth import get_user_model
from django.test import TestCase

from catalog.models import LiteraryFormat, Book


class ModelTests(TestCase):
    def test_literary_format_str(self):
        literary_format = LiteraryFormat.objects.create(name="test")
        self.assertEqual(str(literary_format), literary_format.name)

    def test_author_name_str(self):
        author = get_user_model().objects.create(
            username="test",
            password="test1234",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(str(author), f"{author.username}: {author.first_name} {author.last_name}")

    def test_book_format(self):
        literary_format = LiteraryFormat.objects.create(name="test")
        book = Book.objects.create(
            title="Test Book",
            price=13,
            format=literary_format,
        )
        self.assertEqual(str(book), f"Title {book.title}: price: {book.price}, format: {book.format}")

    def test_create_author_with_pseudonym(self):
        username = "test"
        password = "<PASSWORD>"
        pseudonym = "test1234"
        author = get_user_model().objects.create_user(
            username=username,
            password=password,
            pseudonym=pseudonym,
        )
        self.assertEqual(author.username, username)
        self.assertEqual(author.pseudonym, pseudonym)
        self.assertTrue(author.check_password(password))