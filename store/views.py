from django.shortcuts import render
from .models import Book


def home(request):
    books = Book.objects.all()
    return render(request, 'store/home.html', {'books': books})


def books(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query)

    if category:
        books = books.filter(category__iexact=category)

    return render(request, 'store/books.html', {
        'books': books,
        'query': query,
        'category': category
    })


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)

    return render(request, 'store/book_detail.html', {
        'book': book
    })