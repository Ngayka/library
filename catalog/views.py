from django.views import generic
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from catalog.forms import AuthorCreationForm, LiteraryForm, BookForm, BookSearchForm
from catalog.models import Book, Author, LiteraryFormat



def index(request: HttpRequest) -> HttpResponse:
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    num_literary_formats = LiteraryFormat.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {"num_books": num_books,
               "num_authors": num_authors,
               "num_literary_formats": num_literary_formats,
               "num_visits": num_visits,}

    return render(request,
                  "catalog/index.html",
                  context=context)


class LiteraryFormatListView(LoginRequiredMixin, generic.ListView):
    model = LiteraryFormat
    template_name = "catalog/literary_formats_list.html"
    context_object_name = "literary_formats_list"
    #queryset = LiteraryFormat.objects.filter()


# def literary_format_list_view(request: HttpRequest) -> HttpResponse:
#     literary_formats_list = LiteraryFormat.objects.all()
#     context = {"literary_formats_list": literary_formats_list}
#     return render(request, "catalog/literary_formats_list.html", context=context)

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context['search_form'] = BookSearchForm(
            initial={"title": title},
        )
        return context

    # def get_queryset(self):
    #     title = self.request.GET.get("title")
    #     if title:
    #         return self.queryset.filter(title__icontains=title)
    #     else:
    #         return self.queryset
#OR
    def get_queryset(self):
        queryset = Book.objects.select_related("format")
        form = BookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains = form.cleaned_data['title'])
        else:
            return queryset

class AuthorListView(generic.ListView):
    model = Author


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


# def book_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
#     try:
#         book = Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exist")
#
#     context = {"book": book}
#     return render(request, "catalog/book_detail.html", context=context)
def test_session_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "<h1>Test Session View</h1>"
        f"<h4>Session data: {request.session['book']} </h4>"
    )


class AuthorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Author
    form_class = AuthorCreationForm
    # success_url = reverse_lazy("catalog:author-list")
    # template_name = "catalog/author_form.html"
# def person_create_view(request: HttpRequest) -> HttpResponse:
#     context = {}
#     form = AuthorForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         # Author.objects.create(**form.cleaned_data)
#         return HttpResponseRedirect(reverse("catalog:author-list"))
#     context["form"] = form
#     return render(request, "catalog/author_form.html", context=context)

    # if request.method == "GET":
    #     context = {
    #         "form": AuthorForm()
    #     }
    #     return render(request, "catalog/author_form.html", context=context)
    # elif request.method == "POST":
    #     form = AuthorForm(request.POST)
    #     if form.is_valid():
    #         Author.objects.create(**form.cleaned_data)
    #         return HttpResponseRedirect(reverse("catalog:author-list"))
    #     context ={
    #         "form": form
    #         }
    #     return render(request, "catalog/author_form.html", context=context)

class LiteraryFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = LiteraryFormat
    form_class = LiteraryForm
    success_url = reverse_lazy("catalog:literary-formats-list")
    template_name = "catalog/literary_format_form.html"

class LiteraryFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = LiteraryFormat
    form_class = LiteraryForm
    success_url = reverse_lazy("catalog:literary-formats-list")
    template_name = "catalog/literary_format_form.html"


class LiteraryFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = LiteraryFormat
    success_url = reverse_lazy("catalog:literary-formats-list")
    template_name = "catalog/literary_format_confirm_delete.html"


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = BookForm

class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    form_class = BookForm
