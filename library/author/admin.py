from django.contrib import admin
from .models import Author
from book.models import Book

class BookInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'total_books')
    inlines = [BookInline]

    def total_books(self, obj):
        return obj.books.count() if hasattr(obj, 'books') else obj.book_set.count()

    total_books.short_description = 'TOTAL BOOKS'