from urllib.parse import urlencode

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import RequestContext
from django.urls import reverse

from BookRecSys_App.models import User, Book, Rating, Dislike
from BookRecSys_App.forms import RegisterUser, FavouriteBook, DislikeBook
from BookRecSys_App.svd import svdmodel
from BookRecSys_App.svd_disliked import svdmodel_dislike
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def loading(request):
    return render(request, 'BookRecSys_App/loading.html')


def homepage(request):
    userid = request.session.get('userid')
    users = User.objects

    for user in users.values('email', 'password', 'name', 'id'):
        if userid == user['id']:
            name = user['name']
            return render(request, 'BookRecSys_App/homepage.html', {'name': name})

    return render(request, 'BookRecSys_App/homepage.html')


def navbar(request):
    return render(request, 'BookRecSys_App/navbar.html')


def profile(request):
    userid = request.session.get('userid')
    users = User.objects.filter(pk=userid)

    for user in users.values('email', 'password', 'name', 'id'):
        name = user['name']
        email = user['email']
        password = user['password']
        return render(request, 'BookRecSys_App/profile.html', {'name': name, 'email': email, 'password': password})


def designtest(request):
    return render(request, 'BookRecSys_App/designtest.html')


def testdb(request):
    return render(request, 'BookRecSys_App/test.html')


def login_register(request):
    if request.method == 'POST' and 'hideregister' in request.POST:
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, "Register Success, You Can Login Now!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, "Register Failed, E-mail is already exist!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST' and 'hidelogin' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        users = User.objects

        notexist = False
        for user in users.values('email', 'password', 'name', 'id'):
            if email == user['email'] and password == user['password']:
                request.session['userid'] = user['id']
                name = user['name']
                messages.success(request, "Login Success, Welcome Back!")
                return render(request, 'BookRecSys_App/homepage.html', {'name': name})

            else:
                notexist = True

        if notexist is True:
            messages.error(request, "Login Failed, Please Check Email & Password!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request, 'BookRecSys_App/login.html')


def test(request):
    return render(request, 'bookRecSys_App/test.html')


def logout(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return redirect('login_register')


def booklist(request):
    userid = request.session.get('userid')
    favourite_book = Rating.objects.filter(user=userid)
    disliked_book = Dislike.objects.filter(user=userid)

    object_list = Book.objects.all().order_by('title')
    paginator = Paginator(object_list, 8)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        keyword = request.POST['keyword']

        if keyword is not None and keyword != '':
            keyword = request.POST['keyword']
            base_url = reverse('search')
            query_string = urlencode({'key': keyword})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)

        elif keyword == '':
            messages.error(request, 'Alert: Please enter any keyword in the search box')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif request.method == 'GET' and request.GET.get('type') == 'fav':
        form = FavouriteBook(request.GET)
        title = request.GET.get('title')

        if form.is_valid():
            iscreated = False
            # check if duplicate title for user don't save
            for i in favourite_book.values('title'):
                if request.GET['title'] == i['title']:
                    iscreated = True
                    break
                else:
                    iscreated = False

            iscreated_dislike = False
            for j in disliked_book.values('title'):
                if request.GET['title'] == j['title']:
                    iscreated_dislike = True
                    break
                else:
                    iscreated_dislike = False

            if iscreated is False and iscreated_dislike is False:
                form.save(commit=True)
                updatebookrating = Book.objects.get(title=title)
                updatebookrating.rating_count = updatebookrating.rating_count + 1
                updatebookrating.save()
                messages.success(request, 'Success: "' + request.GET['title'] + '" Added!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Alert: You Already Added This Book!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif request.method == 'GET' and request.GET.get('type') == 'dislike':
        form = DislikeBook(request.GET)
        title = request.GET.get('title')

        if form.is_valid():
            iscreated = False
            # check if duplicate title for user don't save
            for i in favourite_book.values('title'):
                if request.GET['title'] == i['title']:
                    iscreated = True
                    break
                else:
                    iscreated = False

            iscreated_dislike = False
            for j in disliked_book.values('title'):
                if request.GET['title'] == j['title']:
                    iscreated_dislike = True
                    break
                else:
                    iscreated_dislike = False

            if iscreated is False and iscreated_dislike is False:
                form.save(commit=True)
                updatebookrating = Book.objects.get(title=title)
                updatebookrating.rating_count = updatebookrating.rating_count + 1
                updatebookrating.save()
                messages.success(request, 'Success: "' + request.GET['title'] + '" Added!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Alert: You Already Added This Book!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request, 'BookRecSys_App/bookdb.html', {'page': page, 'post_list': post_list})


def searchbook(request):
    key = request.GET.get('key')
    keyword = request.GET.get('keyword')

    if keyword is not None and keyword != '':

        book_info = Book.objects.filter(
            Q(title__icontains=keyword) | Q(isbn__icontains=keyword) | Q(author__icontains=keyword))[:16]
        context = {
            'item': book_info,
            'key': keyword,
        }
        return render(request, 'BookRecSys_App/searchbook.html', context)

    elif key is not None and key != '':
        book_info = Book.objects.filter(
            Q(title__icontains=key) | Q(isbn__icontains=key) | Q(author__icontains=key))[:16]
        context = {
            'item': book_info,
            'key': key,
        }
        return render(request, 'BookRecSys_App/searchbook.html', context)

    elif keyword == '':
        messages.error(request, 'Alert: Please enter any keyword in the search box')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'GET' and request.GET.get('type') == 'fav':
        form = FavouriteBook(request.GET)
        title = request.GET.get('title')
        userid = request.session.get('userid')
        favourite_book = Rating.objects.filter(user=userid)
        disliked_book = Dislike.objects.filter(user=userid)

        if form.is_valid():
            iscreated = False
            # check if duplicate title for user don't save
            for i in favourite_book.values('title'):
                if request.GET['title'] == i['title']:
                    iscreated = True
                    break
                else:
                    iscreated = False

            iscreated_dislike = False
            for j in disliked_book.values('title'):
                if request.GET['title'] == j['title']:
                    iscreated_dislike = True
                    break
                else:
                    iscreated_dislike = False

            if iscreated is False and iscreated_dislike is False:
                form.save(commit=True)
                updatebookrating = Book.objects.get(title=title)
                updatebookrating.rating_count = updatebookrating.rating_count + 1
                updatebookrating.save()
                messages.success(request, 'Success: "' + request.GET['title'] + '" Added!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Alert: You Already Added This Book!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif request.method == 'GET' and request.GET.get('type') == 'dislike':
        form = DislikeBook(request.GET)
        userid = request.session.get('userid')
        title = request.GET.get('title')
        favourite_book = Rating.objects.filter(user=userid)
        disliked_book = Dislike.objects.filter(user=userid)

        if form.is_valid():
            iscreated = False
            # check if duplicate title for user don't save
            for i in favourite_book.values('title'):
                if request.GET['title'] == i['title']:
                    iscreated = True
                    break
                else:
                    iscreated = False

            iscreated_dislike = False
            for j in disliked_book.values('title'):
                if request.GET['title'] == j['title']:
                    iscreated_dislike = True
                    break
                else:
                    iscreated_dislike = False

            if iscreated is False and iscreated_dislike is False:
                form.save(commit=True)
                updatebookrating = Book.objects.get(title=title)
                updatebookrating.rating_count = updatebookrating.rating_count + 1
                updatebookrating.save()
                messages.success(request, 'Success: "' + request.GET['title'] + '" Added!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Alert: You Already Added This Book!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'bookRecSys_App/updateprofile.html')


def updateprofile(request):
    if request.method == 'POST':
        userid = request.session.get('userid')
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        userdetails = User.objects.get(pk=userid)

        userdetails.name = name
        userdetails.email = email
        userdetails.password = password

        try:
            userdetails.save()
            messages.success(request, "Update Profile Success!")
            return redirect('profile')
        except IntegrityError:
            messages.error(request, "Alert : Email entered used by other user!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        userid = request.session.get('userid')
        users = User.objects.filter(pk=userid)

        for user in users.values('email', 'password', 'name', 'id'):
            name = user['name']
            email = user['email']
            password = user['password']
            return render(request, 'BookRecSys_App/updateprofile.html',
                          {'name': name, 'email': email, 'password': password})


def myshelf(request):
    if request.method == 'GET' and request.GET.get('type') == 'fav':
        user = request.GET.get('user')
        title = request.GET.get('title')

        Rating.objects.filter(user=user, title=title).delete()
        updatebookrating = Book.objects.get(title=title)
        updatebookrating.rating_count = updatebookrating.rating_count - 1
        updatebookrating.save()
        messages.success(request, title + ", Successfully Deleted from Favourite Book!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif request.method == 'GET' and request.GET.get('type') == 'dislike':
        user = request.GET.get('user')
        title = request.GET.get('title')

        Dislike.objects.filter(user=user, title=title).delete()
        updatebookrating = Book.objects.get(title=title)
        updatebookrating.rating_count = updatebookrating.rating_count - 1
        updatebookrating.save()
        messages.success(request, title + ", Successfully Deleted from Disliked Book!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        userid = request.session.get('userid')

        favourite_book = Rating.objects.filter(user=userid)
        dislike_book = Dislike.objects.filter(user=userid)

        book_info_fav = Book.objects.filter(title__in=favourite_book.values('title'))
        book_info_dis = Book.objects.filter(title__in=dislike_book.values('title'))
        context = {
            'ratedbook': book_info_fav,
            'dislikedbook': book_info_dis,
        }
        return render(request, 'BookRecSys_App/myshelf.html', context)


def recommender(request):
    userid = request.session.get('userid')
    favourite_book = Rating.objects.filter(user=userid)
    disliked_book = Dislike.objects.filter(user=userid)

    # if request.method == 'GET' and request.GET.get('type') == 'fav':
    #     form = FavouriteBook(request.GET)
    #
    #     if form.is_valid():
    #         form.save(commit=True)
    #         messages.success(request, 'Success: "' + request.GET['title'] + '" Added!')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #     else:
    #         messages.error(request, 'Add Book As Favourite Failed!')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #
    # elif request.method == 'GET' and request.GET.get('type') == 'dislike':
    #     form = DislikeBook(request.GET)
    #
    #     if form.is_valid():
    #         form.save(commit=True)
    #         messages.success(request, 'Success: "' + request.GET['title'] + '" Added!')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #     else:
    #         messages.error(request, 'Add Book As Dislike Failed!')
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if favourite_book:
        listfav = []
        for fav in favourite_book.values('title'):
            listfav.append(fav['title'])

        listdislike = []
        for dis in disliked_book.values('title'):
            listdislike.append(dis['title'])

        rec = svdmodel(listfav)
        notrec = svdmodel_dislike(listdislike)

        latestrec_fav = []
        latestrec_dis = []

        for i in rec:
            for j in i:
                latestrec_fav.append(j)

        for j in notrec:
            for k in j:
                latestrec_dis.append(k)

        latestrec = [fruit for fruit in latestrec_fav if fruit not in latestrec_dis]

        # for a in range(len(latestrec_fav)):
        #     flush = False
        #     for b in range(len(latestrec_dis)):
        #         if latestrec_fav[a] == latestrec_dis[b]:
        #             flush = True
        #             break
        #         elif latestrec_fav[a] != latestrec_dis[b]:
        #             flush = False
        #
        #     if flush is False:
        #         latestrec.append(latestrec_dis[a])
        #
        #     latestrec.append(latestrec_fav[a])

        print(latestrec_fav)
        print(latestrec_dis)
        print(latestrec)

        finalrec = list(dict.fromkeys(latestrec))

        book_list = Book.objects.filter(title__in=finalrec).order_by('title')

        context = {
            'rec': book_list,
        }
        return render(request, 'bookRecSys_App/recommender.html', context)

    else:
        messages.error(request, 'Please add any books from the books section!')
        return render(request, 'bookRecSys_App/recommender.html')
