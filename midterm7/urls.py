"""
URL configuration for mblog0927 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from mysite import views as mv
from mysite.views import book_list, borrow_book, return_book, reserve_book, cancel_reservation, add_book, edit_book, delete_book
from mytest import views as testv
from mytest.views import register, login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",mv.homepage, name="homepage"),
    path("post/<slug:slug>/",mv.showpost,name="showpost"),
    path('book_list/', book_list, name='book_list'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('return/<int:book_id>/', return_book, name='return_book'),
    path('register/', testv.register),
    path('login/', testv.login, name='login'),
    path('logout/', testv.logout, name='logout'),
    path('search/', mv.search_books, name='search_books'),
    path('reserve/<int:book_id>/', reserve_book, name='reserve_book'),
    path('cancel/<int:book_id>/', cancel_reservation, name='cancel_reservation'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:book_id>/', edit_book, name='edit_book'),
    path('delete_book/<slug:slug>/', delete_book, name='delete_book'),
]
