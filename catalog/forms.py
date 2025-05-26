from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from catalog.models import Author, LiteraryFormat, Book


class AuthorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Author
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "pseudonym")


class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta(forms.ModelForm):
        model = Book
        fields = "__all__"


class LiteraryForm(forms.ModelForm):
    class Meta:
        model = LiteraryFormat
        fields = ["name"]


class BookSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by Title"}),
        label="",
    )
