from django.contrib import admin
from .models import Category, Book, Loan

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'available', 'created')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category', 'available', 'created')
    fields = ('title', 'author', 'category', 'slug', 'summary', 'isbn', 'available', 'image')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrowed_at', 'due_date', 'is_returned')
    search_fields = ('book__title', 'user__username')
    list_filter = ('borrowed_at', 'due_date', 'returned_at')
    fields = ('book', 'user', 'due_date', 'returned_at')
    readonly_fields = ('borrowed_at',)
