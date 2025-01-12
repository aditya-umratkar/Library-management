from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index,name='index'),
    path('home', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup', views.signup_view,name='signup'),    
    path('logout/', views.logout_view, name='logout'),
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('user/account/', views.user_account, name='user_account'),
    path('return_book/<int:borrowed_book_id>/', views.return_book, name='return_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
