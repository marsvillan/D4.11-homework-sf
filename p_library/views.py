from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from p_library.models import Author, Book, Publisher

# Create your views here.
def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
        "range": [x for x in range(1, 100) if not x%3],
    }
    return HttpResponse(template.render(biblio_data, request))

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def publisher(request):
    template = loader.get_template('publisher.html')
    publishers = Publisher.objects.all()
    for pub in publishers:
        pub.books = ", ".join([x.title for x in Book.objects.filter(publisher=pub.id)])
    data = {
        "publishers": publishers,
    }
    return HttpResponse(template.render(data))
