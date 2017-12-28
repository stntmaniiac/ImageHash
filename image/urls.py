from django.contrib import admin
from django.conf.urls import url, include
from . import views
app_name='image'
urlpatterns = [
    url(r'^upload/$', views.UploadImage.as_view(), name='upload'),
    url(r'^details/(?P<pk>[0-9]+)$', views.DetailView.as_view(), name='details'),
    url(r'^$', views.IndexView.as_view(), name='index'),

]
