from django.shortcuts import render, redirect, get_object_or_404
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
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        user = request.user if request.user.is_authenticated else CustomUser.objects.first()

        if book.count > 0:
            # Планируемая дата возврата = текущее время + 14 дней
            planned_date = timezone.now() + timedelta(days=14)

            Order.objects.create(
                user=user,
                book=book,
                plated_end_at=planned_date  # Передаем обязательное поле
            )

            book.count -= 1
            book.save()

        return redirect('book_detail', book_id=book.id)


def close_order(request, order_id):
    if not request.user.is_authenticated or getattr(request.user, 'role', None) != 1:
        return redirect('book_list')

    if request.method == 'POST':
        order = Order.get_by_id(order_id)
        if order and order.end_at is None:
            order.update(end_at=timezone.now())

    return redirect('order_list')
