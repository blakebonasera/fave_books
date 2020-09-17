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
    return redirect('/success')

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
            return redirect('/success')

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
        return redirect('/success')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    new_book = Book.objects.create(
        title= request.POST['title'],
        desc= request.POST['desc'],
        uploaded_by= logged_in_user
    )
    new_book.users_who_like.add(logged_in_user)
    print(new_book.__dict__)
    return redirect("/success")

def book(request, num):
    context ={
        'selected_book': Book.objects.get(id=num),
        'all_books': Book.objects.all(),
    }
    return redirect(request, 'book.html', context)
def logout(request):
    request.session.clear()
    return redirect('/')