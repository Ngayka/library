from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class LiteraryFormat(models.Model):
    objects = None
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Author(AbstractUser):
    pseudonym = models.CharField(max_length=63, null=True, blank=True)
    class Meta:
        ordering = ("username", )

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    format = models.ForeignKey(LiteraryFormat, on_delete=models.CASCADE, related_name="books")
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="books")

    class Meta:
        ordering = ("title", )

    def __str__(self):
        return f"Title {self.title}: price: {self.price}, format: {self.format}"

    def get_absolute_url(self):
        return reverse("catalog:book_detail", args=[str(self.id)])
