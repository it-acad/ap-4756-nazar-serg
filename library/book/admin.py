from django.contrib import admin
from .models import Book
from author.models import Author


class AuthorInline(admin.TabularInline):
    model = Author.books.through
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_authors', 'count')
    list_filter = ('authors__surname', 'count')
    search_fields = ('id', 'name', 'authors__name', 'authors__surname')
    inlines = [AuthorInline]

    fieldsets = (
        ('Book details', {
            'fields': ('name', 'description', 'count')
        }),
    )

    @admin.display(description='Authors')
    def get_authors(self, obj):
        return ", ".join([f"{a.name} {a.surname}" for a in obj.authors.all()])