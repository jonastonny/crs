from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^room/create/$', views.CreateRoomView.as_view(), name='room_create'),
    url(r'^room/(?P<pk>[0-9]+)/$', views.RoomDetailView.as_view(), name='room_detail'),
    url(r'^room/(?P<room>[0-9]+)/edit/$', views.room_edit, name='room_edit'),
    url(r'^room/(?P<room>[0-9]+)/update/$', views.room_update, name='room_update'),
    url(r'^room/(?P<room>[0-9]+)/subscribe/$', views.room_subscribe, name='room_subscribe'),
    url(r'^room/(?P<room>[0-9]+)/question/(?P<pk>[0-9]+)/$', views.QuestionDetailView.as_view(), name='question_detail'),
]
