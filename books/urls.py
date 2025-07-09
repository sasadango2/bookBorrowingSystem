from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<slug:category_slug>/', views.book_list, name='book_list_by_category'),
    path('book/<int:id>/<slug:slug>/', views.book_detail, name="book_detail"),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:loan_id>/', views.return_book, name='return_book'),
    
    # 互換性のため
    path('products/', views.book_list, name='product_list'),
    path('product/<int:id>/<slug:slug>/', views.book_detail, name="product_detail"),
]