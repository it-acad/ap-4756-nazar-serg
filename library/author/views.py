from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Author
from .forms import AuthorForm


def author_detail(request, pk):
    author = get_object_or_404(Author.objects.prefetch_related('books'), pk=pk)
    return render(request, 'author/author_detail.html', {'author': author})


def author_list(request):
    authors = Author.get_all()
    return render(request, 'author/author_list.html', {'authors': authors})


def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The author has been successfully added!')
            return redirect('author_list')
    else:
        form = AuthorForm()

    return render(request, 'author/author_form.html', {'form': form, 'title': 'Add author'})


def author_delete(request, author_id):
    if request.method == 'POST':
        success = Author.delete_by_id(author_id)
        if success:
            messages.success(request, 'The author has been successfully removed.')
        else:
            messages.error(request, 'Error deleting author.')
    return redirect('author_list')