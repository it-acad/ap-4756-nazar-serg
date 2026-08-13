from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Book
from order.models import Order
from authentication.models import CustomUser


def book_list(request):
    query = request.GET.get('q', '').strip()
    books = Book.get_all()

    if query:
        books = Book.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(authors__name__icontains=query) |
            Q(authors__surname__icontains=query)
        ).distinct()

    return render(request, 'book/book_list.html', {'books': books, 'query': query})


def book_detail(request, book_id):
    book = Book.get_by_id(book_id)
    if not book:
        return redirect('book_list')
    return render(request, 'book/book_detail.html', {'book': book})


def user_books(request, user_id):
    if not request.user.is_authenticated or getattr(request.user, 'role', None) != 1:
        return redirect('book_list')

    target_user = CustomUser.get_by_id(user_id) if hasattr(CustomUser, 'get_by_id') else CustomUser.objects.filter(id=user_id).first()
    if not target_user:
        return redirect('book_list')

    active_orders = Order.objects.filter(user=target_user, end_at__isnull=True)

    return render(request, 'book/user_books.html', {
        'target_user': target_user,
        'orders': active_orders
    })