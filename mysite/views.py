from django.shortcuts import render
from mysite.models import Post
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.utils.text import slugify




# Create your views here.
def homepage(request):
    posts=Post.objects.all()
    now=datetime.now()
    return render(request,"index.html",locals())

def showpost(request,slug):
    try:
        post =Post.objects.get(slug=slug)
        if post !=None:
            return render(request, "post.html",locals())
        else:
            return redirect("/")
    except:
        return redirect("/")
    
def book_list(request):
    books = Post.objects.all()
    return render(request, 'book_list.html', {'books': books})

def borrow_book(request, book_id):
    book = get_object_or_404(Post, id=book_id)

    if not book.isBorrow:
        book.isBorrow = True
        book.save()

    return HttpResponseRedirect(reverse('book_list'))

def return_book(request, book_id):
    book = get_object_or_404(Post, id=book_id)

    if book.isBorrow:
        book.isBorrow = False
        book.save()

    return HttpResponseRedirect(reverse('book_list'))