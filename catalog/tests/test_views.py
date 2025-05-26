from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from catalog.models import LiteraryFormat

LITERARY_FORMAT_URL = reverse("catalog:literary-formats-list")

class PublicLiteraryFormatTests(TestCase):
    def test_login_required(self):
        response = self.client.get(LITERARY_FORMAT_URL)
        self.assertNotEqual(response.status_code, 200)

class PrivateLiteraryFormatTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_literary_format(self):
        LiteraryFormat.objects.create(name="drama")
        LiteraryFormat.objects.create(name="comedy")
        response = self.client.get(LITERARY_FORMAT_URL)
        self.assertEqual(response.status_code, 200)
        literary_formats = LiteraryFormat.objects.all()
        self.assertEqual(list(response.context['literary_formats_list']), list(literary_formats))
        self.assertTemplateUsed(response, "catalog/literary_formats_list.html")

