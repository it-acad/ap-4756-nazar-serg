from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Order
from book.models import Book
from authentication.models import CustomUser


def order_list(request):
    # if not request.user.is_authenticated or getattr(request.user, 'role', None) != 1:
    #     return redirect('book_list')

    orders = Order.get_all()
    return render(request, 'order/order_list.html', {'orders': orders})


def user_orders(request):
    dummy_user = CustomUser.objects.first()

    orders = Order.objects.filter(user=dummy_user).order_by('-created_at') if dummy_user else []
    return render(request, 'order/user_orders.html', {'orders': orders})


def create_order(request, book_id):
    # if not request.user.is_authenticated:
    #     return redirect('book_list')

    if request.method == 'POST':
        book = Book.get_by_id(book_id)
        dummy_user = CustomUser.objects.first()

        if book and dummy_user:
            plated_end_at = timezone.now() + timedelta(days=14)
            Order.create(user=dummy_user, book=book, plated_end_at=plated_end_at)

    return redirect('user_orders')


def close_order(request, order_id):
    # if not request.user.is_authenticated or getattr(request.user, 'role', None) != 1:
    #     return redirect('book_list')

    if request.method == 'POST':
        order = Order.get_by_id(order_id)
        if order and order.end_at is None:
            order.update(end_at=timezone.now())

    return redirect('order_list')