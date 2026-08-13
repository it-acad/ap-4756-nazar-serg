from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Order
from book.models import Book


def order_list(request):
    if not request.user.is_authenticated or getattr(request.user, 'role', None) != 1:
        return redirect('book_list')

    orders = Order.get_all()
    return render(request, 'order/order_list.html', {'orders': orders})


def user_orders(request):
    if not request.user.is_authenticated:
        return redirect('book_list')

    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order/user_orders.html', {'orders': orders})


def create_order(request, book_id):
    if not request.user.is_authenticated:
        return redirect('book_list')

    if request.method == 'POST':
        book = Book.get_by_id(book_id)
        if book:
            plated_end_at = timezone.now() + timedelta(days=14)
            Order.create(user=request.user, book=book, plated_end_at=plated_end_at)

    return redirect('user_orders')


def close_order(request, order_id):
    if not request.user.is_authenticated or getattr(request.user, 'role', None) != 1:
        return redirect('book_list')

    if request.method == 'POST':
        order = Order.get_by_id(order_id)
        if order and order.end_at is None:
            order.update(end_at=timezone.now())

    return redirect('order_list')