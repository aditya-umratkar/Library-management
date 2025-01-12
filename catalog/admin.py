# admin.py

from django.contrib import admin
from .models import Book,BorrowedBook

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'quantity')
    fields = ('title', 'author', 'description', 'quantity', 'book_cover', 'audio_file')

admin.site.register(Book, BookAdmin)

admin.site.register(BorrowedBook)