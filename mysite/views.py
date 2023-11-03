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

    # 檢查書籍是否已經被借閱
    if not book.isBorrow:
        # 更新 isBorrow 欄位
        book.isBorrow = True
        book.save()

    # 重定向到書籍清單頁面
    return HttpResponseRedirect(reverse('book_list'))

def return_book(request, book_id):
    book = get_object_or_404(Post, id=book_id)

    # 檢查書籍是否已經被借閱
    if book.isBorrow:
        # 更新 isBorrow 欄位
        book.isBorrow = False
        book.save()

    # 重定向到書籍清單頁面
    return HttpResponseRedirect(reverse('book_list'))

def book_category(request, category):
    category_slug = slugify(category)
    books = Post.objects.filter(category=category_slug)
    return render(request, 'basetest.html', {'books': books, 'category': category})



'''
def homepage(request):
    posts=Post.objects.all() #select*from post
    post_lists=list()
    for counter, post in enumerate(posts):
        post_lists.append(f"No. {counter}-{post}<br>")
    return HttpResponse(post_lists)
'''