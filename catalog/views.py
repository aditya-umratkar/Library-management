from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

# Create your views here.




def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password_confirm = request.POST['password2']
        
        if password == password_confirm:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                # Username already exists, handle appropriately (e.g., show error message)
                pass
            else:
                # Create new user
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('login')  # Redirect to login page after successful signup
        else:
            # Handle password mismatch error
            pass
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            # Handle invalid login credentials
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('index')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book


def home_view(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Book

from django.shortcuts import render, redirect
from .models import Book

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Book, BorrowedBook

@login_required
def borrow_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)
        if book.quantity > 0:
            book.quantity -= 1
            book.save()
            BorrowedBook.objects.create(user=request.user, book=book)
            return redirect('user_account')
    return redirect('home')

@login_required
def return_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id, user=request.user)
    if borrowed_book.returned_date is None:
        borrowed_book.returned_date = timezone.now()
        borrowed_book.calculate_late_fee()
        borrowed_book.save()
        borrowed_book.book.quantity += 1
        borrowed_book.book.save()
    return redirect('user_account')

@login_required
def user_account(request):
    # Fetch borrowed books ordered by returned date (None first) and borrowed date
    borrowed_books = BorrowedBook.objects.filter(user=request.user).order_by('returned_date', 'borrowed_date')
    return render(request, 'user_account.html', {'borrowed_books': borrowed_books})

from django.shortcuts import render, get_object_or_404
from .models import Book

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})

from django.shortcuts import render, get_object_or_404
from .models import Book

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})

# views.py

from django.shortcuts import render
from .models import Book

def index(request):
    # Fetch some example books (you can modify this query as per your actual needs)
    books = Book.objects.all()  # Example: fetch the first 6 books

    return render(request, 'index.html', {'books': books})


# views.py

from django.shortcuts import render, get_object_or_404
from .models import Book

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book})
