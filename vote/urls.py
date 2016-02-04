from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^room/(?P<pk>[0-9]+)/$', views.RoomDetailView.as_view(), name='room_detail'),
    url(r'^question/(?P<pk>[0-9]+)/$', views.QuestionDetailView.as_view(), name='question_detail'),
]
