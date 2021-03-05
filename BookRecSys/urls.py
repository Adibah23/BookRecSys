from django.conf.urls import url
from BookRecSys_App import views
from django.contrib import admin
from BookRecSys_App.sessions import create_session, access_session, delete_session

urlpatterns = [

    url(r'^login_register', views.login_register, name='login_register'),
    url(r'^recommender', views.recommender, name='recommender'),
    url(r'^loading', views.loading, name='loading'),
    url(r'^homepage', views.homepage, name='homepage'),
    url(r'^navbar', views.navbar),
    url(r'^bookdb', views.booklist),
    url(r'^profile', views.profile, name='profile'),
    url(r'^updateprofile', views.updateprofile, name="updateprofile"),
    url(r'^myshelf', views.myshelf, name="myshelf"),
    url(r'^designtest', views.designtest, name="designtest"),
    url(r'^test', views.test),
    url(r'^admin', admin.site.urls),

    url(r'^search', views.searchbook, name='search'),

    url(r'^create/', create_session),
    url(r'^access', access_session),
    url(r'^delete', delete_session),


    url(r'^logout', views.logout, name='logout'),
]
