from django.http import HttpResponse
from django.shortcuts import redirect


def create_session(request):
    request.session['userid'] = id
    request.session['password'] = 'password123'
    return HttpResponse("<h1>dataflair<br> the session is set</h1>")


def access_session(request):
    response = "<h1>Welcome to Sessions of dataflair</h1><br>"
    if request.session.get('name'):
        response += "Name : {0} <br>".format(request.session.get('userid'))
        return HttpResponse(response)
    else:
        return HttpResponse("<h1>dataflair<br> the session does not have any data</h1>")


def delete_session(request):
    try:
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass
    return HttpResponse("<h1>dataflair<br>Session Data cleared</h1>")



