from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE, verbose_name="ジャンル")
    title = models.CharField("タイトル", max_length=250)
    author = models.CharField("著者", max_length=100)
    slug = models.SlugField(max_length=250)
    summary = models.TextField("概要", blank=True)
    isbn = models.CharField("ISBN", max_length=13, unique=True, blank=True)
    available = models.BooleanField("貸出可", default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='books', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('products:book_detail', kwargs={'id':self.id, 'slug':self.slug})


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="書籍")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="借用者")
    borrowed_at = models.DateTimeField("借用日", auto_now_add=True)
    due_date = models.DateField("返却予定日")
    returned_at = models.DateTimeField("返却日", null=True, blank=True)
    
    def __str__(self):
        return f"{self.book.title} - {self.user.username}"
    
    @property
    def is_returned(self):
        return self.returned_at is not None


# 旧Productモデルは削除または名前変更
Product = Book  # 互換性のため



