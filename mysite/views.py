from django.shortcuts import render
from mysite.models import Post
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditBookForm, PostForm



# Create your views here.
def homepage(request):
    posts=Post.objects.all()
    now=datetime.now()
    return render(request,"index.html",locals())

def showpost(request,slug):
    post =Post.objects.get(slug=slug)
    if post !=None:
        return render(request, "post.html",locals())
    else:
        redirect("/")
    
def book_list(request):
    books = Post.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Post, id=book_id)

    if not book.isBorrow:
        # 檢查書籍是否已經被借出給其他人
        if book.borrower is not None:
            messages.error(request, '此書籍已經被借閱。')
        else:
            # 移除預約者清單中的使用者
            if request.user in book.reservations.all():
                book.reservations.remove(request.user)
            book.isBorrow = True
            book.borrower = request.user.username
            book.save()
            messages.success(request, '書籍成功借閱。')
    else:
        messages.error(request, '此書籍已經被借閱。')

    return HttpResponseRedirect(reverse('showpost', kwargs={'slug': book.slug}))



@login_required
def return_book(request, book_id):
    book = get_object_or_404(Post, id=book_id)

    # 檢查是否是借書的人才能還書
    if book.isBorrow and book.borrower == request.user.username:
        book.isBorrow = False
        book.borrower = None
        book.save()
        
        messages.success(request, '書籍成功歸還。')
    elif not book.isBorrow:
        messages.error(request, '書籍尚未被借閱。')
    else:
        messages.error(request, '您沒有借閱此書。')

    return HttpResponseRedirect(reverse('showpost', kwargs={'slug': book.slug}))

@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Post, id=book_id)

    if not book.is_reserved or request.user not in book.reservations.all():
        book.reservations.add(request.user)
        book.save()
        messages.success(request, '書籍成功預約。')
    else:
        messages.error(request, '您已經預約過此書籍。')

    return redirect('showpost', slug=book.slug)

@login_required
def cancel_reservation(request, book_id):
    book = get_object_or_404(Post, id=book_id)

    if book.is_reserved and request.user in book.reservations.all():
        book.reservations.remove(request.user)
        book.save()
        messages.success(request, '預約已取消。')
    elif not book.is_reserved:
        messages.error(request, '此書籍尚未被預約。')
    else:
        messages.error(request, '您沒有預約此書。')

    return redirect('showpost', slug=book.slug)

def search_books(request):
    if 'q' in request.GET:
        query = request.GET['q']
        # 在 title, write, intro, body 中進行搜尋
        results = Post.objects.filter(title__icontains=query) | \
                  Post.objects.filter(write__icontains=query) | \
                  Post.objects.filter(intro__icontains=query) | \
                  Post.objects.filter(body__icontains=query)
        return render(request, 'search_results.html', {'results': results, 'query': query})
    else:
        return render(request, 'search_results.html')
    
    
@login_required
def add_book(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            return redirect("/")
    else:
        form = PostForm()

    return render(request, 'add_book.html', {'form': form})

    
@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Post, id=book_id)

    if request.method == 'POST':
        form = EditBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('showpost', kwargs={'slug': book.slug}))
    else:
        form = EditBookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})

@login_required
def delete_book(request, slug):
    book = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        # 在確認刪除之前，可以添加一些額外的檢查或確認
        book.delete()
        return redirect('/')

    return render(request, 'delete_book.html', {'book': book})

