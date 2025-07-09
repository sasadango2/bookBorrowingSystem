from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Book, Loan
from datetime import date, timedelta

def book_list(request, category_slug=None):
    category = None
    books = Book.objects.filter(available=True)
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)
    
    return render(request, 'products/book/list.html', {
        'category': category,
        'books': books,
        'categories': categories,
    })
    
def book_detail(request, id, slug):
    book = get_object_or_404(Book, id=id, slug=slug)
    return render(request, 'products/book/detail.html', {'book': book})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, available=True)
    
    # すでに借りているかチェック
    existing_loan = Loan.objects.filter(book=book, user=request.user, returned_at__isnull=True).exists()
    if existing_loan:
        messages.error(request, 'この本はすでに借りています。')
        return redirect('products:book_detail', id=book.id, slug=book.slug)
    
    # 貸出処理
    due_date = date.today() + timedelta(days=14)  # 2週間後
    Loan.objects.create(book=book, user=request.user, due_date=due_date)
    book.available = False
    book.save()
    
    messages.success(request, f'「{book.title}」を借りました。返却予定日: {due_date}')
    return redirect('products:book_detail', id=book.id, slug=book.slug)

@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, user=request.user, returned_at__isnull=True)
    
    # 返却処理
    loan.returned_at = timezone.now()
    loan.save()
    loan.book.available = True
    loan.book.save()
    
    messages.success(request, f'「{loan.book.title}」を返却しました。')
    return redirect('products:book_list')

# 互換性のため
product_list = book_list
product_detail = book_detail