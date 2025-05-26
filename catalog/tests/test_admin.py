from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestAdminSite(TestCase):
    def setUp(self):
        client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="<PASSWORD>",
        )
        self.client.force_login(self.admin_user)
        self.author = get_user_model().objects.create_user(
            username="author",
            password="<AUTHOR_PASSWORD>",
            pseudonym="author pseudonym",
        )
    def test_author_pseudonym_listed(self):
        """Test that author's pseudonym is listed on author admin page
        return:"""
        url = reverse("admin:catalog_author_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.author.pseudonym)

    def test_author_detail_pseudonym_listed(self):
        """Test that author's pseudonym is on author detail admin page
        return:"""
        url = reverse("admin:catalog_author_change", args=[self.author.id])
        res = self.client.get(url)
        self.assertContains(res, self.author.pseudonym)

