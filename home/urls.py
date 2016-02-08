from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^profile/$', views.profile_detail, name='profile'),
    url(r'^home/$', views.IndexView.as_view(), name='index'),
]
