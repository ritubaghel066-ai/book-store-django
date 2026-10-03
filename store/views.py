from django.shortcuts import render, redirect
from .models import Book


def home(request):
    books = Book.objects.all()
    categories = Book.objects.values_list('category', flat=True).distinct()

    return render(request, 'store/home.html', {
        'books': books,
        'categories': categories
    })


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


def add_to_cart(request, book_id):
    cart = request.session.get('cart', {})

    book_id = str(book_id)

    if book_id in cart:
        cart[book_id] += 1
    else:
        cart[book_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart_data = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for book_id, quantity in cart_data.items():
        book = Book.objects.get(id=book_id)

        item_total = book.price * quantity
        total_price += item_total

        cart_items.append({
            'book': book,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def increase_quantity(request, book_id):
    cart = request.session.get('cart', {})

    book_id = str(book_id)

    if book_id in cart:
        cart[book_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request, book_id):
    cart = request.session.get('cart', {})

    book_id = str(book_id)

    if book_id in cart:
        if cart[book_id] > 1:
            cart[book_id] -= 1
        else:
            del cart[book_id]

    request.session['cart'] = cart

    return redirect('cart')


def remove_from_cart(request, book_id):
    cart = request.session.get('cart', {})

    book_id = str(book_id)

    if book_id in cart:
        del cart[book_id]

    request.session['cart'] = cart

    return redirect('cart')

def about(request):
    return render(request, 'store/about.html')


def contact(request):
    return render(request, 'store/contact.html')

def checkout(request):
    return render(request, 'store/checkout.html')