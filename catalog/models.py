from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    book_cover = models.ImageField(upload_to='book_covers/')
    pdf = models.FileField(upload_to='book_pdfs/', null=True, blank=True)
    audio_file = models.FileField(upload_to='book_audios/', blank=True, null=True)  # Add this line
    
    def __str__(self):
        return self.title

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    late_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def calculate_late_fee(self):
        if self.returned_date:
            days_borrowed = (self.returned_date - self.borrowed_date).days
            if days_borrowed > 10:
                self.late_fee = (days_borrowed - 10) * 10
                self.save()
