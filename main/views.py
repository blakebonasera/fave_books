from django.shortcuts import render , HttpResponse, redirect
from django.contrib import messages
from .models import User, Book
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    # password = request.POST['pw']
    pw_hash = bcrypt.hashpw(request.POST['pw'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    new_user = User.objects.create(
        first = request.POST['first'],
        last= request.POST['last'],
        email= request.POST['email'],
        password= pw_hash
        )
    request.session['user_id'] = new_user.id
    messages.success(request, 'Thats it!')
    return redirect('/book')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    list_of_users = User.objects.filter(email=request.POST['email'])
    if len(list_of_users) > 0:
        user = list_of_users[0]
        print(user)
        if bcrypt.checkpw(request.POST['pw'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/book')
        else:
            errors['incorrect'] = 'Your email or password is incorrect'
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'logged_in_user': logged_in_user,
        'all_books': Book.objects.all(),
    }
    return render(request, 'success.html', context)

def newBook(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    new_book = Book.objects.create(
        title= request.POST['title'],
        desc= request.POST['desc'],
        uploaded_by= logged_in_user
    )
    new_book.users_who_like.add(logged_in_user)
    print(new_book.__dict__)
    return redirect("/book")

def book(request, num):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    if 'user_id' not in request.session:
        return redirect('/')
    context ={
        'logged_in_user': logged_in_user,
        'selected_book': Book.objects.get(id=num),
        'all_books': Book.objects.all(),
    }
    return render(request, 'book.html', context)

def update(request, num):
    errors = Book.objects.book_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book')
    updated_book = Book.objects.get(id=num)
    updated_book.title = request.POST['title']
    updated_book.desc = request.POST['desc']
    updated_book.save()
    return redirect('/book')

def delete(request, num):
    book_to_delete = Book.objects.get(id=num)
    book_to_delete.delete()
    return redirect('/book')

def favorite(request, num):
    book = Book.objects.get(id=num)
    logged_in_user = User.objects.get(id=request.session['user_id'])
    logged_in_user.liked_by.add(book)
    return redirect('/book')

def unfavorite(request, num):
    book = Book.objects.get(id=num)
    logged_in_user = User.objects.get(id=request.session['user_id'])
    logged_in_user.liked_by.remove(book)
    return redirect('/book')


def logout(request):
    request.session.clear()
    return redirect('/')